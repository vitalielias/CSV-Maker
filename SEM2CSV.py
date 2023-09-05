import zipfile
import pandas as pd
import hyperspy.api as hs
import os
import csv
import tempfile
from typing import Dict, Any

headFile   = sys.argv[1]
inputZip   = sys.argv[2]
outputFile = sys.argv[3]

def recursive_search(d: Dict[str, Any], target_key: str) -> Any:
    for key, value in d.items():
        if key == target_key:
            return value
        if isinstance(value, dict):
            found = recursive_search(value, target_key)
            if found is not None:
                return found
    return None

def extract_and_write_metadata(conversion_csv, input_path, output_csv):
    df = pd.read_csv(conversion_csv)
    hyperspy_names = df['hyperspy'].dropna().tolist()
    
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['filename'] + hyperspy_names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        if input_path.endswith('.zip'):
            # Create a temporary directory to extract files
            with tempfile.TemporaryDirectory() as tmpdirname:
                with zipfile.ZipFile(input_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)

                    for filename in os.listdir(tmpdirname):
                        if filename.endswith('.tif'):
                            file_path = os.path.join(tmpdirname, filename)
                            image = hs.load(file_path)
                            om = image.original_metadata.as_dictionary()
                            metadata_dict = {'filename': filename}
                            for hyperspy_name in hyperspy_names:
                                value = recursive_search(om, hyperspy_name)
                                if isinstance(value, tuple) and len(value) > 1:
                                    value = value[1]
                                metadata_dict[hyperspy_name] = value if value is not None else 'N/A'
                            writer.writerow(metadata_dict)
        else:
            for filename in os.listdir(input_path):
                if filename.endswith('.tif'):
                    image_path = os.path.join(input_path, filename)
                    image = hs.load(image_path)
                    om = image.original_metadata.as_dictionary()
                    metadata_dict = {'filename': filename}
                    for hyperspy_name in hyperspy_names:
                        value = recursive_search(om, hyperspy_name)
                        if isinstance(value, tuple) and len(value) > 1:
                            value = value[1]
                        metadata_dict[hyperspy_name] = value if value is not None else 'N/A'
                    writer.writerow(metadata_dict)
                    