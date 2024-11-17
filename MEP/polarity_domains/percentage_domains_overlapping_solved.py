import json
import pandas as pd
from Data_to_file import *
import sys

inDir = sys.argv[1] # directory within data dir which contains json file with protein domain info
inFile = sys.argv[2] # inputfile as argument in terminal domains_proteins_[name].json

file_path = '../data/'
inFile_path = f"{file_path}/{inDir}/{inFile}"

def calculate_domain_percentage(protein_data, output_file):
    # Open the JSON file
    global percentage_covered
    with open(protein_data) as f:
        # Load JSON data
        data = json.load(f)

    # Create an empty list to store data
    data_rows = []

    for protein in data:
        if "length" in protein:
            sequence_length = int(protein["length"])
            covered_regions = []  # List to store covered regions

            # Iterate through domains
            for domain in protein["domains"]:
                domain_start = int(domain["domain_start"])
                domain_end = int(domain["domain_end"])
                domain_coverage = domain_end - domain_start + 1

                # Check for overlap with existing covered regions
                overlapping_regions = []
                for region_start, region_end in covered_regions:
                    if domain_start <= region_end and domain_end >= region_start:
                        # Calculate overlapping region
                        overlap_start = max(domain_start, region_start)
                        overlap_end = min(domain_end, region_end)
                        overlapping_regions.append((overlap_start, overlap_end))

                # Add non-overlapping part of the domain to covered regions
                non_overlapping_regions = []
                for region_start, region_end in covered_regions:
                    if not any(overlap_start <= region_end and overlap_end >= region_start for overlap_start, overlap_end in
                               overlapping_regions):
                        non_overlapping_regions.append((region_start, region_end))
                non_overlapping_regions.append((domain_start, domain_end))
                covered_regions = non_overlapping_regions

            # Update domain coverage
            total_coverage = sum(region_end - region_start + 1 for region_start, region_end in covered_regions)
            percentage_covered = (total_coverage / sequence_length) * 100

            # Append data to the list
            data_rows.append(
                [protein['accession_protein'], protein['input_name'], sequence_length, f"{percentage_covered:.2f}"])

    # Create a DataFrame from the list of data
    df = pd.DataFrame(data_rows, columns=['accession_protein', 'input_name', 'protein_length', '%_domain'])

    # Write DataFrame to TSV file
    df.to_csv(output_file, sep='\t', index=False)
    print(f"percentage domains saved to {output_file}")


# Test usage:
#protein_data = "relevant_domains_yeast_all.json"
#output_file = "protein_domain_coverage_yeast.tsv"
#calculate_domain_percentage(protein_data, output_file)

# Making an output file name and calling the function with input and outputfile.
output_file = output_file_frontextension('percentage',inFile, 'tsv')
outfile_path = f"{file_path}/{inDir}/{output_file}"
calculate_domain_percentage(inFile_path,outfile_path)
