"""
Business-logic module
---------------------
Fetches orthologs for a Drosophila gene (FBgn…) using DIOPT and writes them
to an Excel file.  Requires: requests, pandas, openpyxl
"""

from __future__ import annotations
import os, re, html
from typing import Dict
import requests, pandas as pd

DIOPT_URL = "https://www.flyrnai.org/cgi-bin/DRSC_orthologs.pl"

# NCBI taxonomy IDs keyed by user-friendly names
SPECIES2TAX: Dict[str, str] = {
    "human":        "9606",
    "mouse":        "10090",
    "rat":          "10116",
    "zebrafish":    "7955",
    "yeast":        "559292",
    "c. elegans":   "6239",
    "arabidopsis":  "3702",
}

# Looser pattern: “FBgn” + ≥5 digits, internal whitespace OK
FBGN_RE = re.compile(r"^fbgn\s*\d{5,}$", re.IGNORECASE)

# ---------------------------------------------------------------------------

def _clean_fbgn(text: str) -> str:
    """Strip whitespace inside/outside and uppercase the prefix."""
    clean = re.sub(r"\s+", "", text)          # remove all spaces/CR/LF/TAB
    if not clean.lower().startswith("fbgn"):
        clean = "FBgn" + clean.lstrip("fbgn")
    return clean

def _fetch_table(fbgn: str, taxid: str) -> pd.DataFrame:
    params = {
        "gene_list": fbgn,
        "input_species": "7227",          # D. melanogaster
        "output_species": taxid,
        "search_datasets": "All (max score = 10)",
        "search_fields": "FLYBASE",
        "additional_filter": "None",
    }
    resp = requests.get(DIOPT_URL, params=params, timeout=20)
    resp.raise_for_status()

    tables = pd.read_html(resp.text)
    if not tables:
        raise RuntimeError("No table found in DIOPT response.")

    df = tables[0]

    # Skip blank header rows / promote real header
    while df.iloc[0].isna().all():
        df = df.iloc[1:]
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    return df.applymap(lambda x: html.unescape(x) if isinstance(x, str) else x)

# ---------------------------------------------------------------------------

def fetch_and_save(fbgn_raw: str, organism: str, out_dir: str) -> str:
    fbgn = _clean_fbgn(fbgn_raw)

    if not FBGN_RE.match(fbgn):
        raise ValueError("That doesn’t look like a FlyBase gene ID (example: FBgn0000099).")

    taxid = SPECIES2TAX.get(organism.lower())
    if not taxid:
        raise ValueError(f"Unsupported organism: {organism}")

    if not os.path.isdir(out_dir):
        raise FileNotFoundError(f"Output folder not found: {out_dir}")

    df = _fetch_table(fbgn, taxid)
    if df.empty:
        raise RuntimeError(f"No orthologs returned for {fbgn} → {organism}.")

    out_path = os.path.join(
        out_dir,
        f"{fbgn}_orthologs_{organism.replace(' ', '_')}.xlsx"
    )
    df.to_excel(out_path, index=False)   # swap to .csv if you prefer

    return out_path
