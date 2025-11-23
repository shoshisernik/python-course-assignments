import os
import re
import json
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional, Tuple

BASE = "https://api.flybase.org/api/v1.0"
HDR_JSON = {"User-Agent": "FlyBaseFetcher/1.0", "Accept": "application/json"}
HDR_XML  = {"User-Agent": "FlyBaseFetcher/1.0", "Accept": "application/xml"}
TIMEOUT = 20

FB_ID_PAT = re.compile(r"^FB[a-z]{2}\d+$", re.IGNORECASE)  # FBgn, FBtr, FBpp, FBal, FBst, etc.


# -------------------------
# Small HTTP helpers
# -------------------------
def _get_json(url: str) -> Dict[str, Any]:
    r = requests.get(url, headers=HDR_JSON, timeout=TIMEOUT)
    if r.status_code != 200:
        raise Exception(f"FlyBase API error {r.status_code} for {url}\n{(r.text or '')[:300]}")
    try:
        return r.json()
    except json.JSONDecodeError:
        raise Exception(f"FlyBase returned non-JSON at {url}\n{(r.text or '')[:300]}")


def _get_text(url: str, expect_xml: bool = False) -> str:
    headers = HDR_XML if expect_xml else HDR_JSON
    r = requests.get(url, headers=headers, timeout=TIMEOUT)
    if r.status_code != 200:
        raise Exception(f"FlyBase API error {r.status_code} for {url}\n{(r.text or '')[:300]}")
    return r.text


# -------------------------
# Resolution: symbol → FBgn
# (Best-effort: try HitList; otherwise require a valid FB ID.)
# -------------------------
def resolve_to_fbgn(query: str) -> str:
    q = query.strip()
    if FB_ID_PAT.match(q):
        # Already a FlyBase ID (FBgn/FBtr/FBpp/..., we’ll lift to gene if needed)
        if q.lower().startswith("fbgn"):
            return q
        # If it’s a transcript/protein/etc, we can ask Sequence endpoint to return parent gene,
        # but simplest: ask ChadoXML and pull the gene. Here we just fail fast & guide the user:
        raise Exception("Please provide a gene FBgn ID or a gene symbol (e.g., 'wg', 'ap', 'so').")

    # Try HitList fetch with the free text; select first gene FBgn in the results.
    # (OpenAPI shows this endpoint and schema.)
    # If FlyBase doesn’t interpret free text here, this will return counts/results that may be empty.
    data = _get_json(f"{BASE}/hitlist/fetch/{requests.utils.quote(q)}")
    results = data.get("result", []) or []
    # Heuristic: look for id strings that look like FBgn
    fbgn = None
    def find_fbgn(obj):
        nonlocal fbgn
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and v.lower().startswith("fbgn") and FB_ID_PAT.match(v):
                    fbgn = v
                    return True
                if isinstance(v, (dict, list)) and find_fbgn(v):
                    return True
        elif isinstance(obj, list):
            for it in obj:
                if find_fbgn(it):
                    return True
        return False

    find_fbgn(results)
    if fbgn:
        return fbgn

    raise Exception(
        f"Could not resolve '{query}' to a FlyBase gene ID via HitList.\n"
        f"Tip: enter an FBgn (e.g., FBgn0000099) or a canonical gene symbol."
    )


# -------------------------
# Summaries / species / sequences / location / hitlists
# -------------------------
def get_auto_summary(fbgn: str) -> Optional[str]:
    url = f"{BASE}/gene/summaries/auto/{fbgn}"
    data = _get_json(url)
    # OpenAPI says: result is a list of {summary:'auto', type, id}; some deployments include text.
    result = data.get("result") or []
    if result and isinstance(result, list):
        entry = result[0]
        return entry.get("text") or entry.get("summary") or None
    return None


def get_species(fb_id: str) -> Optional[Dict[str, str]]:
    data = _get_json(f"{BASE}/species/lookup/{fb_id}")
    res = (data.get("result") or [])
    if res:
        return {
            "genus": res[0].get("genus", ""),
            "species": res[0].get("species", ""),
            "abbrev": res[0].get("abbreviation", "")
        }
    return None


def get_sequences_for_gene(fbgn: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Returns a dict with keys 'gene', 'transcripts', 'proteins' each being a list of FASTA dicts.
    """
    out: Dict[str, List[Dict[str, str]]] = {"gene": [], "transcripts": [], "proteins": []}

    def fetch_id(id_str: str, subtype: Optional[str] = None) -> List[Dict[str, str]]:
        if subtype:
            url = f"{BASE}/sequence/id/{id_str}/{subtype}"
        else:
            url = f"{BASE}/sequence/id/{id_str}"
        data = _get_json(url)
        fas = data.get("result") or []
        # Each item is {id, description, sequence}
        return [f for f in fas if isinstance(f, dict)]

    # gene-level sequence (FBgn)
    try:
        out["gene"] = fetch_id(fbgn, "FBgn")
    except Exception:
        out["gene"] = []

    # transcripts (FBtr)
    try:
        out["transcripts"] = fetch_id(fbgn, "FBtr")
    except Exception:
        pass

    # proteins (FBpp)
    try:
        out["proteins"] = fetch_id(fbgn, "FBpp")
    except Exception:
        pass

    return out


def get_location_from_chadoxml(fbgn: str) -> Dict[str, Any]:
    """
    Parse minimal coordinates from ChadoXML.
    """
    xml_text = _get_text(f"{BASE}/chadoxml/{fbgn}", expect_xml=True)
    root = ET.fromstring(xml_text)

    chrom = "Unknown"
    fmin = "Unknown"
    fmax = "Unknown"
    strand = "Unknown"

    for fl in root.findall(".//featureloc"):
        fmin_el = fl.find("fmin")
        fmax_el = fl.find("fmax")
        strand_el = fl.find("strand")
        src = fl.find("srcfeature")

        if fmin_el is not None and fmax_el is not None:
            fmin = fmin_el.text or fmin
            fmax = fmax_el.text or fmax
        if strand_el is not None and strand_el.text:
            strand = strand_el.text

        # Try to extract a source feature name (chrom arm or scaffold)
        if src is not None:
            name_el = src.find(".//name")
            uniq_el = src.find(".//uniquename")
            arm = (uniq_el.text if uniq_el is not None and uniq_el.text else
                   name_el.text if name_el is not None and name_el.text else None)
            if arm:
                chrom = arm

        if fmin != "Unknown" and fmax != "Unknown":
            break

    return {"Chromosome Arm": chrom, "Start Position": fmin, "End Position": fmax, "Strand": strand}


def get_hitlist(fbgn: str) -> Dict[str, Any]:
    """
    Fetch the HitList object and try to extract allele IDs (FBal) and stock IDs (FBst).
    Schema is generic, so we search for IDs in nested structures.
    """
    data = _get_json(f"{BASE}/hitlist/fetch/{fbgn}")
    result = data.get("result") or []
    counts = data.get("counts") or {}

    alleles: List[str] = []
    stocks: List[str] = []

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(v, str):
                    s = v.strip()
                    if s.lower().startswith("fbal") and FB_ID_PAT.match(s):
                        alleles.append(s)
                    elif s.lower().startswith("fbst") and FB_ID_PAT.match(s):
                        stocks.append(s)
                elif isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(x, list):
            for it in x:
                walk(it)

    walk(result)
    # De-duplicate while preserving order
    def uniq(seq): 
        seen=set(); out=[]
        for it in seq:
            if it not in seen:
                seen.add(it); out.append(it)
        return out

    return {
        "counts": counts,
        "alleles": uniq(alleles),
        "stocks": uniq(stocks),
        "raw": result,  # for transparency/debug (written to a JSON sheet preview)
    }


# -------------------------
# Main “do everything” entry
# -------------------------
def fetch_all_and_save(user_query: str, output_dir: str) -> Tuple[str, Optional[str]]:
    """
    Returns (excel_path, resolved_id_if_any)
    """
    if not os.path.isdir(output_dir):
        raise Exception(f"Output folder does not exist: {output_dir}")

    fbgn = resolve_to_fbgn(user_query)
    resolved_note = fbgn if user_query != fbgn else None

    # Species
    species = get_species(fbgn) or {"genus": "", "species": "", "abbrev": ""}

    # Summary (may be None for some IDs)
    summary = get_auto_summary(fbgn)

    # Location
    loc = get_location_from_chadoxml(fbgn)

    # Sequences
    seqs = get_sequences_for_gene(fbgn)

    # Alleles/stocks
    hits = get_hitlist(fbgn)

    # Build Excel
    # Sheet 1: Overview
    overview = {
        "FlyBase ID": [fbgn],
        "Genus": [species.get("genus", "")],
        "Species": [species.get("species", "")],
        "Abbrev": [species.get("abbrev", "")],
        "Chromosome Arm": [loc.get("Chromosome Arm")],
        "Start Position": [loc.get("Start Position")],
        "End Position": [loc.get("End Position")],
        "Strand": [loc.get("Strand")],
        "Auto Summary": [summary or "Not available"],
        "Allele count (if provided)": [hits.get("counts", {}).get("FBal", "")],
        "Stock count (if provided)": [hits.get("counts", {}).get("FBst", "")]
    }
    df_over = pd.DataFrame(overview)

    # Sheet 2–4: sequences
    def seq_df(lst: List[Dict[str, str]]) -> pd.DataFrame:
        if not lst:
            return pd.DataFrame(columns=["id", "description", "sequence"])
        return pd.DataFrame(lst)[["id", "description", "sequence"]]

    df_gene = seq_df(seqs.get("gene", []))
    df_tr   = seq_df(seqs.get("transcripts", []))
    df_pp   = seq_df(seqs.get("proteins", []))

    # Sheet 5–6: simple lists for alleles & stocks
    df_alleles = pd.DataFrame({"FBal": hits.get("alleles", [])})
    df_stocks  = pd.DataFrame({"FBst": hits.get("stocks", [])})

    # Sheet 7: (optional) raw hitlist JSON preview (first 10 top-level items stringified)
    raw = hits.get("raw", [])
    preview_rows = []
    for i, item in enumerate(raw[:10]):
        preview_rows.append({"index": i, "json": json.dumps(item)[:500]})
    df_hit_raw = pd.DataFrame(preview_rows)

    # Save
    safe_base = fbgn
    out_path = os.path.join(output_dir, f"{safe_base}_flybase_bundle.xlsx")
    try:
        with pd.ExcelWriter(out_path, engine="openpyxl") as xw:
            df_over.to_excel(xw, sheet_name="Overview", index=False)
            df_gene.to_excel(xw, sheet_name="Sequence_gene", index=False)
            df_tr.to_excel(xw, sheet_name="Sequence_transcripts", index=False)
            df_pp.to_excel(xw, sheet_name="Sequence_proteins", index=False)
            df_alleles.to_excel(xw, sheet_name="Alleles_FBal", index=False)
            df_stocks.to_excel(xw, sheet_name="Stocks_FBst", index=False)
            df_hit_raw.to_excel(xw, sheet_name="HitList_preview", index=False)
    except ModuleNotFoundError as e:
        if "openpyxl" in str(e):
            raise Exception("Writing .xlsx requires 'openpyxl'. Install with:\n  python -m pip install openpyxl")
        raise
    except PermissionError:
        raise Exception(f"Could not write Excel (is it open?):\n{out_path}")

    return out_path, resolved_note
