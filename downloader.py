import os
import requests

BASE_URL = "https://www.canada.ca"

def download_pdfs(file_path: str, output_dir: str) -> None:
    """
    Downloads PDF files from a list of URLs provided in a text file.

    :param file_path: Path to the text file containing PDF URLs (one per line).
    :param output_dir: Directory where downloaded PDFs will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    for index, url in enumerate(urls):
        url = url.strip()
        if not url:
            continue
        
        try:
            response = requests.get(f"{BASE_URL}{url}", stream=True)
            response.raise_for_status()
            
            fn = url.split('/')[-1]
            filename = os.path.join(output_dir, fn)
            with open(filename, 'wb') as pdf_file:
                for chunk in response.iter_content(chunk_size=1024):
                    pdf_file.write(chunk)
            
            print(f"Downloaded: {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    file_path = "pdf_links.txt"  # Change to your file containing PDF URLs
    output_dir = "downloaded_pdfs"  # Change to your desired output directory
    download_pdfs(file_path, output_dir)
