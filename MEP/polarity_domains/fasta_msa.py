# this file searches for the domain sequences of proteins with this specific domain,
# and then saves these in fasta format

import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# inputfiles
# data_yeast = pd.read_csv('../data/fullyeast_data/count_relevant_domains_yeast_all.tsv', sep='\t')
# data_str_full = pd.read_csv('../data/Stringfull_data/count_relevant_domains_str_full_559292.tsv', sep='\t')
# json_file= ('../data/Stringfull_data/relevant_domains_str_full_559292.json')

# inputfiles
data_yeast = pd.read_csv('../data/fullyeast_data/count_relevant_domains_yeast_all.tsv', sep='\t')
data_str_full = pd.read_csv('../data/combined_set/count_domains_proteins_combinedset.tsv', sep='\t')
json_file= ('../data/combined_set/domains_proteins_combinedset.json')

# Open the JSON file
with open(json_file) as f:
    # Load JSON data
    data_json_str_full = json.load(f)

# this functions searches in the dataframe df for the domain_accession and gives the proteins that have this domain
def search_domain_in_dataframe(df, domain_accession):
    row_values = df[df['Domain Accession'] == domain_accession]['Accession proteins'].values
    if len(row_values) > 0:
        return row_values[0]
    else:
        print(f"Accession {domain_accession} not found in {df} data")
        return

def search_accession_domain(data, accession_domain, outputfile):
    output_content= open(outputfile, 'w+')

    for protein in data:
        alphafold_info = []
        if 'domains' in protein:
            for domain in protein['domains']:
                if domain['domain_accession'] == accession_domain:
                    accession_protein= protein['accession_protein']
                    print(f"Domain {accession_domain} found in {accession_protein} ")
                    protein_domain = f"{protein['input_name']}_{domain['domain_shortname']}"
                    sequence = protein['sequence']
                    domain_start = int(domain["domain_start"]) - 1
                    domain_end = int(domain['domain_end']) - 1
                    domain_sequence = sequence[domain_start:domain_end]

                    # Reset the file pointer to the beginning before searching
                    output_content.seek(0)

                    # Check if protein domain already exists in the output content
                    if f">{protein_domain} \n" in output_content.read():
                        protein_domain_name = f"2_{protein_domain}"
                        print(protein_domain_name)
                    else:
                        protein_domain_name = protein_domain

                    output_content.write(
                        f">{protein_domain_name} - {protein['accession_protein']}- {domain_start} - {domain_end} \n"
                        f"{domain_sequence} \n"
                    )
            #else:
                #print(f"Domain {accession_domain} not found ")



outfSH3 = 'proteins_SH3_combined.fasta'
domain_accesion_SH3 = "IPR001452"
proteins_SH3 = search_accession_domain(data_json_str_full,domain_accesion_SH3,outfSH3)
#outfSH3.close()

outfPH = 'proteins_PH_combined.fasta'
domain_accesion_PH = "IPR001849"
proteins_PH = search_accession_domain(data_json_str_full,domain_accesion_PH,outfPH)
#outfPH.close()
#%%