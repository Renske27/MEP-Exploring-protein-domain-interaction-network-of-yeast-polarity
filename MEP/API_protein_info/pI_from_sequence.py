import json
import requests
from bs4 import BeautifulSoup
from Data_to_file import *
import sys

inDir = sys.argv[1] # directory within data dir which contains domains_proteins_{proteinsetname}.json file
inFile = sys.argv[2]    # filename of domains_proteins_{proteinsetname}.json


#outFile = sys.argv[2]
inFile_path = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/'
# Function to calculate the isoelectric point (pI) of a protein sequence
def calculate_isoelectric_point(sequence):
    url = 'https://web.expasy.org/cgi-bin/protparam/protparam'
    params = {
        'sequence': sequence,
        'compute': 'Compute parameters'
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pI_element = soup.find('strong', text='Theoretical pI:')
        if pI_element:
            pI_text = pI_element.next_sibling.strip()
            return float(pI_text)
        else:
            raise Exception("Theoretical pI not found in the response from ExPASy ProtParam.")
    else:
        raise Exception(f"Failed to calculate pI using ExPASy ProtParam. Status code: {response.status_code}")


# Load the JSON file
file_path = f"{inFile_path}/{inDir}/{inFile}"
with open(file_path, 'r') as f:
    protein_data = json.load(f)

# Iterate over each protein in the JSON file
for protein in protein_data:
    protein_sequence = protein['sequence']

    # Calculate the pI for the whole protein
    try:
        protein_pI = calculate_isoelectric_point(protein_sequence)
        protein['protein_pI'] = protein_pI
        #print(f"{protein['input_name']} = {protein_pI}")
    except Exception as e:
        print(f"Error calculating pI for protein {protein['input_name']}: {e}")
        protein['protein_pI'] = None

    # Calculate the pI for each domain
    for domain in protein['domains']:
        domain_start = int(domain['domain_start']) - 1  # Convert to 0-based index
        domain_end = int(domain['domain_end'])  # Use 1-based end index
        domain_sequence = protein_sequence[domain_start:domain_end]

        try:
            domain_pI = calculate_isoelectric_point(domain_sequence)
            domain['domain_pI'] = domain_pI
        except Exception as e:
            print(f"Error calculating pI for domain {domain['domain_name']} in protein {protein['input_name']}: {e}")
            domain['domain_pI'] = None

# Save the modified JSON back to a file
outFile=output_filename(inFile, '_pI','json')
output_file_path = f"{inFile_path}/{inDir}/{inFile}"


with open(output_file_path, 'w+') as f:
    json.dump(protein_data, f, indent=4)

print(f"Updated JSON file saved to {output_file_path}")
