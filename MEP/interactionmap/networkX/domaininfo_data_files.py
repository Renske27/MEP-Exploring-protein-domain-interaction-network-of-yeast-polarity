import json
import csv

# Path to the JSON file
json_file_path = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/domains_protein_list2_with_pI.json'

# Path to the output CSV file
csv_file_path = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/interactionmap_data/domains_info_2.csv'

# Load the JSON data
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Prepare the CSV data
csv_data = []

for protein in data:
    protein_input_name = protein['input_name']
    protein_accession = protein['accession_protein']
    protein_length = protein['length']
    protein_name = protein['protein name']
    protein_pI = protein['protein_pI']
    if any(protein['domains']):
        for domain in protein['domains']:
            domain_name = domain['domain_name']
            domain_shortname = domain['domain_shortname']
            domain_accession = domain['domain_accession']
            domain_pI = domain['domain_pI']
            domain_start = domain['domain_start']
            domain_end = domain['domain_end']
            csv_data.append([
                protein_input_name,
                protein_name,
                protein_accession,
                protein_pI,
                protein_length,
                domain_name,
                domain_shortname,
                domain_accession,
                domain_pI,
                domain_start,
                domain_end

            ])
    else:
        domain_name = 'Other'
        domain_shortname= domain_name
        domain_accession ='0000'
        domain_pI = None
        domain_end = protein_length
        domain_start ='1'
        csv_data.append([
            protein_input_name,
            protein_name,
            protein_accession,
            protein_pI,
            protein_length,
            domain_name,
            domain_shortname,
            domain_accession,
            domain_pI,
            domain_start,
            domain_end
        ])


# Write the CSV data to a file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['protein_input_name', 'protein fullname','protein_accession', 'protein_pI', 'protein_length', 'domain_name', 'domain_shortname','domain_accession', 'domain_pI','domain_start', 'domain_end'])
    csv_writer.writerows(csv_data)

print(f"Data successfully written to {csv_file_path}")
