import json
import pandas as pd
import sys
import math
from Data_to_file import *

# Input and output file paths
data_yeast=pd.read_csv('../data/fullyeast_data/count_relevant_domains_yeast_all.tsv', sep='\t')
inDir = sys.argv[1]  # directory within data dir which contains json file with protein domain info
inFile = sys.argv[2]  # should be Json file with all protein info
# Input for testing
#inDir= "list2_data"
#inFile= "domains_protein_list2.json"

file_path = '../data/'
inFile_path = f"{file_path}/{inDir}/{inFile}"


# Function to search for a string in the first column of DataFrame
def search_string_in_dataframe(df, string):
    row_values = df[df['Domain Accession'] == string]['Count'].values
    if len(row_values) > 0:
        return row_values[0]
    else:
        print(f"Accession {string} not found in yeast data")
        return 0

# Function to read the domain data from JSON file and return the domain count DataFrame and total number of unique proteins
def count_domains(inputfile):
    with open(inputfile) as f:
        data = json.load(f)

    domain_count = {}
    domains_protein = {}
    domain_names = {}
    domains_protein_accession = {}
    unique_proteins = set()

    for entry in data:
        unique_proteins.add(entry['accession_protein'])
        if 'domains' in entry:
            protein_name = entry['input_name']
            protein_accession = entry['accession_protein']
            domains = entry['domains']

            for domain in domains:
                if 'domain_accession' in domain:
                    domain_accession = domain['domain_accession']
                    domain_name = domain['domain_shortname']

                    if domain_accession in domain_count:
                        domain_count[domain_accession] += 1
                        domains_protein[domain_accession].append(protein_name)
                        domains_protein_accession[domain_accession].append(protein_accession)
                    else:
                        domain_count[domain_accession] = 1
                        domains_protein[domain_accession] = [protein_name]
                        domain_names[domain_accession] = domain_name
                        domains_protein_accession[domain_accession] = [protein_accession]

    domain_info = pd.DataFrame({
        'Domain Accession': list(domain_count.keys()),
        'Domain name': list(domain_names.values()),
        'Count': list(domain_count.values()),
        'Proteins': list(domains_protein.values()),
        'Accession proteins': list(domains_protein_accession.values())
    })

    domain_info.set_index('Domain Accession', inplace=False)
    protein_amount = len(unique_proteins)
    return domain_info, protein_amount

def ratio_domain_count(df_list, df_yeast):
    ratio_count = []
    for ind in df_list.index:
        accession = df_list.at[ind, 'Domain Accession']
        count_list = df_list.at[ind, 'Count']

        count_yeast = search_string_in_dataframe(df_yeast, accession)
        ratio = count_list / count_yeast if count_yeast != 0 else math.inf

        ratio_count.append(ratio)

    df_list['Ratio'] = ratio_count
    return df_list

def domain_occurance(df_list, df_yeast, no_proteins):
    ratio_list_count = []
    ratio_yeast_count = []
    ratio_ratio = []
    for ind in df_list.index:
        accession = df_list.at[ind, 'Domain Accession']
        count_list = df_list.at[ind, 'Count']

        count_yeast = search_string_in_dataframe(df_yeast, accession)
        ratio_list = count_list / no_proteins
        ratio_yeast = count_yeast / 6766
        ratio_from_ratio = ratio_list / ratio_yeast if ratio_yeast != 0 else math.inf

        ratio_list_count.append(ratio_list)
        ratio_yeast_count.append(ratio_yeast)
        ratio_ratio.append(ratio_from_ratio)

    df_list['N_dl/N_pl / N_dy/N_py'] = ratio_ratio
    df_list['N_d_list/N_p_list'] = ratio_list_count
    df_list['N_d_yeast/N_p_yeast'] = ratio_yeast_count

    return df_list

# Count domains and retrieve domain information
info, amount_proteins_in_list = count_domains(inFile_path)

outFile = output_file_frontextension('count', inFile, 'tsv')
# Write domain information to a TSV file
info.to_csv(f"{file_path}/{inDir}/{outFile}", sep='\t', header=True)

print(f"total amount of proteins in set: {amount_proteins_in_list}")
print(f"saved domain occurrence to {outFile}")


data_incl_ratios = domain_occurance(info, data_yeast, amount_proteins_in_list)
data_incl_ratios.to_csv(f"{file_path}/{inDir}/{outFile}", sep='\t', index=False)

print(f"saved ratio-data to {outFile}")
