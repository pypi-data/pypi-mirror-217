import os
import requests
from tqdm import tqdm

def download_large_file(url, local_filename):
    # Check if the file is already downloaded
    if os.path.exists(local_filename):
        return

    # Send a HTTP request to the URL of the file
    response = requests.get(url, stream=True)

    # Get the total size of the file
    total_size = int(response.headers.get('content-length', 0))

    # Progress bar with `tqdm`
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(local_filename, 'wb') as f:
        for data in response.iter_content(chunk_size=1024):
            # Write data read to the file
            f.write(data)

            # Update the progress bar
            progress_bar.update(len(data))

    progress_bar.close()

    if total_size != 0 and progress_bar.n != total_size:
        print("ERROR, something went wrong")
