import zipfile
import os
import uuid

def handle_upload(zip_file):
    extract_dir = f"uploaded_apps/{uuid.uuid4()}"
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    return extract_dir
