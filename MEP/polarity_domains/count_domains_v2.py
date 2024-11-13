import json
import pandas as pd
import sys
from Data_to_file import *

# Input and output file paths
inDir = sys.argv[1]  # directory within data dir which contains json file with protein domain info
inFile = sys.argv[2]  # should be Json file with all protein info

file_path = '../data/'
inFile_path = f"{file_path}/{inDir}/{inFile}"

def count_domains(inputfile):
    # Open the JSON file
    with open(inputfile) as f:
        # Load JSON data
        data = json.load(f)

    # Initialize dictionaries to store domain counts, associated proteins, and domain names
    domain_count = {}
    domains_protein = {}
    domain_names = {}
    domains_protein_accession = {}

    # Iterate through each entry in the JSON data
    for indx, entry in enumerate(data):
        if 'domains' in entry:
            protein_name = entry['input_name']
            protein_accession = entry['accession_protein']
            domains = entry['domains']

            # Iterate through each domain in the entry
            for domain in domains:
                if 'domain_accession' in domain:
                    domain_accession = domain['domain_accession']
                    domain_name = domain['domain_name']

                    # Update domain count and associated proteins
                    if domain_accession in domain_count:
                        domain_count[domain_accession] += 1
                        domains_protein[domain_accession].append(protein_name)
                        domains_protein_accession[domain_accession].append(protein_accession)
                    else:
                        domain_count[domain_accession] = 1
                        domains_protein[domain_accession] = [protein_name]
                        domain_names[domain_accession] = domain_name
                        domains_protein_accession[domain_accession] = [protein_accession]

    # Create DataFrame to organize domain information
    domain_info = pd.DataFrame({
        'Domain Accession': list(domain_count.keys()),
        'Domain name': list(domain_names.values()),
        'Count': list(domain_count.values()),
        'Proteins': list(domains_protein.values()),
        'Accession proteins': list(domains_protein_accession.values())
    })

    # Set 'Domain Accession' as the index of the DataFrame
    domain_info.set_index('Domain Accession', inplace=True)

    return domain_info

# Count domains and retrieve domain information
info = count_domains(inFile_path)

outFile = output_file_frontextension('count', inFile, 'tsv')
# Write domain information to a TSV file
info.to_csv(f"{file_path}/{inDir}/{outFile}", sep='\t', header=True)

#print(info)
