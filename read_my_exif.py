import exifread
import pathlib as pl
from itertools import chain
import json


def extract_metadata(file_path: pl.Path) -> dict:
    """
    Extracts EXIF metadata from a given DNG or NEF file.

    Args:
        file_path (Path): A pathlib.Path object pointing to the image file.

    Returns:
        dict: A dictionary containing the metadata tags. Keys are tag names
              (e.g., 'EXIF DateTimeOriginal') and values are the tag content.
              Returns None or raises FileNotFoundError if the file is inaccessible.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with file_path.open("rb") as f:
        # process_file returns a dictionary of tags
        # details=False skips extracting thumbnail data (faster)
        tags = exifread.process_file(f, details=False)

    return tags

def extract_and_clean_metadata(file_path: pl.Path) -> dict:
    """
    Extracts metadata and converts all values to clean strings.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open('rb') as f:
        # Get raw tags
        raw_tags = exifread.process_file(f, details=False)

    clean_tags = {}
    for key, val in raw_tags.items():
        # Filter out binary thumbnail data if it slipped through
        if 'Thumbnail' in key:
            continue
            
        # Convert the IFDTag object to a simple string
        # str(val) uses the library's internal formatting to make it human-readable
        clean_tags[key] = str(val).strip()

    return clean_tags


# --- Example Usage ---
if __name__ == "__main__":
    import sqlite3

    top_dir = pl.Path(r"W:\NELSON\photo-current\2025")
    # top_dir = pl.Path(r"W:\NELSON\photo-current\2025\2025_12\21-carolling")

    itr = [f for f in chain(
        top_dir.glob("**/*.nef"),
        top_dir.glob("**/*.dng"),
        top_dir.glob("**/*.NEF"),
        top_dir.glob("**/*.DNG"),
    )]

    file_ct = len(itr)

    times = []
    dat = []
    for j, img_fn in enumerate(itr):
        # metadata = extract_metadata(img_fn)
        metadata = extract_and_clean_metadata(img_fn)
        dat.append((str(img_fn), str(metadata)))

        if not (j%1000):
            print(f'{j/file_ct:.4%}  ({j:>6} of {file_ct})')
        # t = metadata['EXIF DateTimeOriginal']
        # print(t)
        # for k, v in metadata.items():
        #     print(f'{k}: {v}')

    dst = 'test2.db'
    with sqlite3.connect(':memory:', autocommit=True) as conn:
        cur = conn.cursor()
        sql = """CREATE TABLE pyextract_metadata(path TEXT, metadata TEXT);"""
        cur.execute(sql)
        
        cur.executemany("INSERT INTO pyextract_metadata VALUES(?, ?)", dat)

        with sqlite3.connect(dst) as dst_db:
            conn.backup(dst_db)