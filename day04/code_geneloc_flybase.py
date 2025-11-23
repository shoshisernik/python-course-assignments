# code_geneloc_flybase.py
import os
import requests
import pandas as pd

def fetch_gene_data_by_id(fbgn_id):
    """
    Fetch gene summary information from FlyBase using the FlyBase ID.
    
    Args:
        fbgn_id: FlyBase gene ID (e.g., 'FBgn0000099')
    
    Returns:
        Dictionary containing gene information
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Try different URL formats for the FlyBase API
    urls_to_try = [
        f"https://api.flybase.org/v1.0/gene/summaries/auto/{fbgn_id}",
        f"https://api.flybase.org/api/v1.0/gene/summaries/auto/{fbgn_id}",
        f"https://flybase.org/api/v1.0/gene/summaries/auto/{fbgn_id}",
    ]
    
    gene_data = None
    for url in urls_to_try:
        print(f"Trying URL: {url}")
        r = requests.get(url, headers=headers)
        
        print(f"Status Code: {r.status_code}")
        print(f"Response (first 500 chars): {r.text[:500]}")
        
        if r.status_code == 200 and r.text:
            try:
                gene_data = r.json()
                print(f"Success! Gene data retrieved")
                print(f"Response keys: {gene_data.keys() if isinstance(gene_data, dict) else 'Not a dict'}")
                break
            except Exception as e:
                print(f"Could not parse JSON: {e}")
                continue
    
    if gene_data is None:
        raise Exception(f"Failed to fetch gene data from any endpoint")
    
    return gene_data


def fetch_gene_info_and_save(fbgn_id, output_folder):
    """
    Gets gene info from FlyBase using FlyBase ID, extracts coordinates, and saves to Excel.
    
    Args:
        fbgn_id: FlyBase gene ID (e.g., 'FBgn0000099')
        output_folder: Path to folder where Excel file will be saved
    
    Returns:
        Path to the created Excel file
    """
    gene_data = fetch_gene_data_by_id(fbgn_id)

    # Extract data from the response
    # The exact field names depend on the API response structure
    fbgn = gene_data.get("uniquename", fbgn_id)
    symbol = gene_data.get("name", "Unknown")
    
    # Get location data - structure may vary depending on API response
    location_data = gene_data.get("location", {})
    if isinstance(location_data, dict):
        chrom = location_data.get("arm", "Unknown")
        start = location_data.get("fmin", "Unknown")
        end = location_data.get("fmax", "Unknown")
        strand = location_data.get("strand", "Unknown")
    else:
        chrom = "Unknown"
        start = "Unknown"
        end = "Unknown"
        strand = "Unknown"

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
