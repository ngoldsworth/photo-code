import zipfile
import os
import shutil
import pathlib as pl

def extract_all_zips(zip_files: list, output_directory: str):
    """
    Extracts the contents of multiple zip files into a single, common output directory.

    Args:
        zip_files (list): A list of paths to the zip files to be processed.
        output_directory (str): The path to the directory where all extracted 
                                contents will be placed.
    """
    # 1. Create the output directory if it doesn't exist
    print(f"Ensuring output directory '{output_directory}' exists...")
    os.makedirs(output_directory, exist_ok=True)
    
    # 2. Process each zip file
    print(f"Starting extraction of {len(zip_files)} zip files...")
    for i, zip_path in enumerate(zip_files, 1):
        if not os.path.exists(zip_path):
            print(f"⚠️ Warning: Zip file not found at '{zip_path}'. Skipping.")
            continue
            
        print(f"\n--- ({i}/{len(zip_files)}) Processing: {os.path.basename(zip_path)} ---")
        
        try:
            # Open the zip file in read mode
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # The core extraction command: extract all members to the output directory
                zf.extractall(output_directory)
                print(f"✅ Successfully extracted all contents to '{output_directory}'.")
                
        except zipfile.BadZipFile:
            print(f"❌ Error: The file '{zip_path}' is not a valid zip file.")
        except Exception as e:
            print(f"❌ An unexpected error occurred while processing '{zip_path}': {e}")
            
    print("\n====================================")
    print("✨ Extraction process complete. ✨")
    print(f"All data has been merged into: {os.path.abspath(output_directory)}")
    print("====================================")

# --- CONFIGURATION SECTION ---

# 1. List the paths to your zip files
#    NOTE: Replace these with the actual paths to your files.
top_dir = pl.Path(r'W:\NELSON\Downloads\photos-takeout')
list_of_zip_paths = [d for d in top_dir.glob('*.zip')]

# 2. Define the single folder where all extracted data will go
common_output_folder = top_dir / 'extracted'

# 3. Run the function
#    To test this, you should create a few dummy zip files in the same directory as this script.
if __name__ == "__main__":
    extract_all_zips(list_of_zip_paths, common_output_folder)