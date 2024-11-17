import os
import zipfile
from collections import defaultdict


def extract_unique_protein_combinations(zip_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dictionary to store unique protein combinations
    unique_combinations = defaultdict(list)

    # Iterate over all files in the zip directory
    for filename in os.listdir(zip_dir):
        if filename.endswith(".zip"):
            parts = filename.split('_')
            if len(parts) >= 5:
                number = parts[2]
                protein1 = parts[3]
                protein2 = parts[4].replace('.zip', '')

                # Create sorted tuple for unique combination
                combination = tuple(sorted([protein1, protein2]))

                # Store the zip filename under the unique combination key
                if combination not in unique_combinations:
                    unique_combinations[combination] = filename


    # Extract each unique zip file to the output directory
    for combination, zip_filename in unique_combinations.items():
        zip_filepath = os.path.join(zip_dir, zip_filename)
        extract_dir = os.path.join(output_dir, "_".join(combination)) # if I want to keep the zip filename just replace with zip_filename

        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        print(f"Extracted {zip_filename} to {extract_dir}")


# Define your directories
zip_directory = "C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/alphafold3"
output_directory = "C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/alphafold3/unpacked_unique"

# Run the extraction process
extract_unique_protein_combinations(zip_directory, output_directory)
