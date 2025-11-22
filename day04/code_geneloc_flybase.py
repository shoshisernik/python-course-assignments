# code_geneloc_flybase.py
import os
import requests
import pandas as pd

def search_flybase_gene(gene_symbol):
    """
    Search FlyBase for a gene symbol using the REST API.
    """
    # Try the direct gene lookup endpoint
    url = f"https://flybase.org/api/v2.0/feature/{gene_symbol}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    r = requests.get(url, headers=headers)
    
    print(f"Status Code: {r.status_code}")
    print(f"Response Text: {r.text[:500]}")

    if r.status_code != 200:
        raise Exception(f"Failed to contact FlyBase API. Status code: {r.status_code}")

    data = r.json()
    print(f"Response Data: {data}")
    
    return data


def fetch_gene_info_and_save(gene_symbol, output_folder):
    """
    Gets first gene match on FlyBase, extracts coordinates, and saves to Excel.
    """
    gene = search_flybase_gene(gene_symbol)

    fbgn = gene.get("uniquename", "Unknown")
    symbol = gene.get("name", gene_symbol)
    location = gene.get("location", {})
    chrom = location.get("arm", "Unknown")
    start = location.get("fmin", "Unknown")
    end = location.get("fmax", "Unknown")
    strand = location.get("strand", "Unknown")

    df = pd.DataFrame([{
        "Gene Symbol": symbol,
        "FlyBase ID": fbgn,
        "Chromosome Arm": chrom,
        "Start Position": start,
        "End Position": end,
        "Strand": strand
    }])

    if not os.path.exists(output_folder):
        raise Exception(f"Output folder does not exist: {output_folder}")

    output_file = os.path.join(output_folder, f"{symbol}_flybase_info.xlsx")

    df.to_excel(output_file, index=False)

    return output_file
