import os
import sys
import shutil
import requests
import argparse
import zipfile
from datetime import datetime

# Default Configuration
DEFAULT_SERVER_URL = "http://localhost:8000"
DEFAULT_TOKEN = "admin-secret-token"

def zip_directory(source_dir, output_filename):
    """Zips a directory excluding common ignore patterns."""
    print(f"Zipping {source_dir} to {output_filename}...")
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Filter ignored directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'dist', 'archives', '__pycache__']]
            
            for file in files:
                if file == output_filename or file.endswith('.zip') or file.endswith('.pyc'):
                    continue
                
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
    print("Zip created.")

def upload_file(file_path, server_url, token):
    """Uploads the file to the server."""
    url = f"{server_url}/api/v1/admin/upload_version"
    filename = os.path.basename(file_path)
    
    print(f"Uploading {filename} to {url}...")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f)}
            data = {'token': token}
            response = requests.post(url, files=files, data=data)
            
        if response.status_code == 200:
            print("Upload successful!")
            print("Server response:", response.json())
            return response.json().get("filename")
        else:
            print(f"Upload failed with status {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Pack and Publish Plugin Version")
    parser.add_argument("source", help="Source directory to pack (e.g., ./Designer) or existing zip file")
    parser.add_argument("--url", default=DEFAULT_SERVER_URL, help="Server Base URL")
    parser.add_argument("--token", default=DEFAULT_TOKEN, help="Admin Token")
    parser.add_argument("--name", help="Custom name for the zip file (optional)")
    
    args = parser.parse_args()
    
    source_path = args.source
    file_to_upload = source_path
    
    # If source is directory, zip it
    if os.path.isdir(source_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if args.name:
            zip_name = f"{args.name}.zip"
        else:
            # Use 'core' prefix if packing dist_core, otherwise directory name
            dir_name = os.path.basename(os.path.abspath(source_path))
            if dir_name == "dist_core":
                base_name = "core"
            else:
                base_name = dir_name
            zip_name = f"{base_name}_{timestamp}.zip"
            
        zip_directory(source_path, zip_name)
        file_to_upload = zip_name
    elif not os.path.isfile(source_path):
        print(f"Error: Source {source_path} not found.")
        sys.exit(1)
        
    # Upload
    uploaded_filename = upload_file(file_to_upload, args.url, args.token)
    
    # Cleanup generated zip if we created it
    if os.path.isdir(source_path) and uploaded_filename:
        # Optional: remove the local zip after upload? 
        # For now, let's keep it or ask user. 
        # I'll keep it for safety but print message.
        print(f"Local package saved as: {file_to_upload}")

if __name__ == "__main__":
    main()
