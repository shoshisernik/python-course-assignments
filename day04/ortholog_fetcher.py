"""
Backend for fetching orthologs through the DIOPT web service.

Dependencies:
    pip install requests pandas openpyxl  # (openpyxl only needed for .xlsx)

The DIOPT service is hosted at flyrnai.org and can be queried with URLs of the form:

  https://www.flyrnai.org/cgi-bin/DRSC_orthologs.pl
      ?gene_list=FBgn0000099
      &input_species=7227        # D. melanogaster
      &output_species=9606       # Homo sapiens
      &search_datasets=All+(max+score+=+10)
      &search_fields=FLYBASE
      &additional_filter=None

…which returns an HTML page whose first table contains the ortholog matches :contentReference[oaicite:0]{index=0}
"""

from __future__ import annotations
import os, re, html
from typing import Dict
import requests, pandas as pd

DIOPT_URL = "https://www.flyrnai.org/cgi-bin/DRSC_orthologs.pl"

# --- NCBI taxonomy IDs for common model organisms --------------------------
SPECIES2TAX: Dict[str, str] = {
    "human": "9606",
    "mouse": "10090",
    "rat": "10116",
    "zebrafish": "7955",
    "yeast": "559292",
    "c. elegans": "6239",
    "arabidopsis": "3702",
}

# quick FlyBase FBgn sanity check
FBGN_RE = re.compile(r"^FBgn\d{7}$", re.IGNORECASE)


def fetch_ortholog_table(fbgn: str, target_taxid: str) -> pd.DataFrame:
    """Return a DataFrame of ortholog matches for *fbgn* → *target_taxid* using DIOPT."""
    params = {
        "gene_list": fbgn,
        "input_species": "7227",          # D. mel
        "output_species": target_taxid,   # chosen by user
        "search_datasets": "All (max score = 10)",
        "search_fields": "FLYBASE",
        "additional_filter": "None",
    }
    resp = requests.get(DIOPT_URL, params=params, timeout=20)
    resp.raise_for_status()

    # DIOPT delivers plain HTML; easiest is pandas.read_html
    tables = pd.read_html(resp.text)
    if not tables:
        raise RuntimeError("No result table found in DIOPT response.")
    df = tables[0]

    # DIOPT’s first 3 header rows are filler – keep the single header row that has real column names
    while df.iloc[0].isna().all():
        df = df.iloc[1:]
    df.columns = df.iloc[0]          # promote first real row to header
    df = df.iloc[1:].reset_index(drop=True)

    # Unescape any HTML entities in string cells
    df = df.applymap(lambda x: html.unescape(x) if isinstance(x, str) else x)
    return df


def fetch_and_save(fbgn: str, organism: str, out_dir: str) -> str:
    """Driver called by the GUI – fetch orthologs and save to .xlsx."""
    if not FBGN_RE.match(fbgn):
        raise ValueError("FBgn looks malformed. Example: FBgn0000099")

    taxid = SPECIES2TAX.get(organism.lower())
    if not taxid:
        raise ValueError(f"Unsupported organism: {organism}")

    if not os.path.isdir(out_dir):
        raise FileNotFoundError(f"Output folder not found: {out_dir}")

    df = fetch_ortholog_table(fbgn, taxid)
    if df.empty:
        raise RuntimeError(f"No orthologs returned for {fbgn} → {organism}.")

    out_path = os.path.join(out_dir, f"{fbgn}_orthologs_{organism.replace(' ','_')}.xlsx")
    df.to_excel(out_path, index=False)  # change to .csv if preferred

    return out_path
