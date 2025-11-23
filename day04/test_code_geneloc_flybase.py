import sys
sys.path.insert(0, r'c:\python_course\python-course-assignments\day04')

from code_geneloc_flybase import fetch_gene_data_by_id, fetch_gene_info_and_save
import tempfile

def test_fetch_gene_data():
    """Test the fetch_gene_data_by_id function"""
    print("=" * 50)
    print("Testing fetch_gene_data_by_id()")
    print("=" * 50)
    
    # FlyBase IDs for common test genes
    test_genes = {
        'ap': 'FBgn0000099',
        'wg': 'FBgn0003848',
        'so': 'FBgn0005561',
        'dpp': 'FBgn0000490'
    }
    
    for gene_name, fbgn_id in test_genes.items():
        print(f"\nFetching data for gene: {gene_name} ({fbgn_id})")
        try:
            result = fetch_gene_data_by_id(fbgn_id)
            print(f"Success! Gene data retrieved")
            print(f"Response type: {type(result)}")
        except Exception as e:
            print(f"Error: {e}")


def test_fetch_and_save():
    """Test the full fetch_gene_info_and_save function"""
    print("\n" + "=" * 50)
    print("Testing fetch_gene_info_and_save()")
    print("=" * 50)
    
    fbgn_id = 'FBgn0000099'  # ap gene
    
    # Use a temporary folder for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\nFetching gene '{fbgn_id}' and saving to {temp_dir}")
        try:
            output_file = fetch_gene_info_and_save(fbgn_id, temp_dir)
            print(f"Success! File saved at: {output_file}")
            
            # Read and display the file contents
            import pandas as pd
            df = pd.read_excel(output_file)
            print(f"\nFile contents:\n{df}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    test_fetch_gene_data()
    # test_fetch_and_save()