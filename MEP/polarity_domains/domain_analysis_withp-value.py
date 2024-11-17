import json
import pandas as pd
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import hypergeom
from Data_to_file import *

# Input and output file paths
data_yeast = pd.read_csv('../data/fullyeast_data/count_relevant_domains_yeast_all.tsv', sep='\t')
# inDir = sys.argv[1]  # directory within data dir which contains json file with protein domain info
# inFile = sys.argv[2]  # should be JSON file with all protein info
# Input for testing
inDir = "combined_set"
inFile = "domains_proteins_combinedset.json"

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


# Function to read the domain data from JSON file and return the domain count DataFrame and total number of unique domain accession numbers
def count_domains(inputfile):
    with open(inputfile) as f:
        data = json.load(f)

    domain_count = {}
    domains_protein = {}
    domain_names = {}
    domains_protein_accession = {}
    unique_domain_accessions = set()

    for entry in data:
        if 'domains' in entry:
            protein_name = entry['input_name']
            protein_accession = entry['accession_protein']
            domains = entry['domains']

            for domain in domains:
                if 'domain_accession' in domain:
                    domain_accession = domain['domain_accession']
                    domain_name = domain['domain_shortname']

                    unique_domain_accessions.add(domain_accession)

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
    domain_accession_amount = len(unique_domain_accessions)
    return domain_info, domain_accession_amount


# Function to perform hypergeometric test
def hypergeometric_test(count_list, count_yeast, total_domains_in_list, total_domains_in_yeast):
    # M: Total number of domains in the reference set (yeast_all)
    M = total_domains_in_yeast
    # n: Number of domains of a specific type in the reference set
    n = count_yeast
    # N: Total number of domains in the protein set
    N = total_domains_in_list
    # k: Number of domains of a specific type in the protein set
    k = count_list

    # Hypergeometric test (calculating the p-value)
    p_value = hypergeom.sf(k - 1, M, n, N)
    return p_value


# Add enrichment score, ratios, and hypergeometric test p-values
def add_calculations(df_list, df_yeast, total_domains_in_list):
    enrichment_scores = []
    ratio_list_counts = []
    ratio_yeast_counts = []
    p_values = []

    total_domains_in_yeast = df_yeast['Count'].sum()

    for ind in df_list.index:
        accession = df_list.at[ind, 'Domain Accession']
        count_list = df_list.at[ind, 'Count']

        count_yeast = search_string_in_dataframe(df_yeast, accession)
        p_value = hypergeometric_test(count_list, count_yeast, total_domains_in_list, total_domains_in_yeast)

        # Enrichment Score Calculation
        enrichment_score = (count_list / total_domains_in_list) / (
                    count_yeast / total_domains_in_yeast) if count_yeast != 0 else math.inf

        # Ratio calculations
        ratio_list_count = count_list / total_domains_in_list
        ratio_yeast_count = count_yeast / total_domains_in_yeast

        enrichment_scores.append(enrichment_score)
        ratio_list_counts.append(ratio_list_count)
        ratio_yeast_counts.append(ratio_yeast_count)
        p_values.append(p_value)

    df_list['Enrichment Score'] = enrichment_scores
    df_list['Ratio in Protein Set'] = ratio_list_counts
    df_list['Ratio in Yeast Set'] = ratio_yeast_counts
    df_list['Hypergeometric p-value'] = p_values
    return df_list


# Count domains and retrieve domain information
info, amount_domain_accessions_in_list = count_domains(inFile_path)

outFile = output_file_frontextension('count', inFile, 'tsv')
# Write domain information to a TSV file
info.to_csv(f"{file_path}/{inDir}/{outFile}", sep='\t', header=True)

print(f"Total number of unique domain accession numbers in set: {amount_domain_accessions_in_list}")
print(f"Saved domain occurrence to {outFile}")

# Add enrichment score, ratios, and hypergeometric test p-values
data_incl_calculations = add_calculations(info, data_yeast, amount_domain_accessions_in_list)

# Save the results including the enrichment score, ratios, and p-values to a TSV file
data_incl_calculations.to_csv(f"{file_path}/{inDir}/{outFile}", sep='\t', index=False)

print(f"Saved ratio-data with enrichment scores and hypergeometric test p-values to {outFile}")

# Visualize the p-value distribution
plt.figure(figsize=(10, 6))
sns.histplot(data_incl_calculations['Hypergeometric p-value'], bins=50, kde=True, color='blue')
plt.title('P-Value Distribution from Hypergeometric Test')
plt.xlabel('P-Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Scatterplot of Enrichment Score vs. -log10(p-value)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Enrichment Score', y=-np.log10(data_incl_calculations['Hypergeometric p-value']),
                data=data_incl_calculations, hue='Enrichment Score', palette="viridis", edgecolor="w", s=100,   alpha=0.6)

# plt.figure(figsize=(10, 6))
# sns.kdeplot(
#     x=data_incl_calculations['Enrichment Score'],
#     y=-np.log10(data_incl_calculations['Hypergeometric p-value']),
#     fill=True, thresh=0, levels=100, cmap="viridis"
# )
# sns.scatterplot(
#     x='Enrichment Score',
#     y=-np.log10(data_incl_calculations['Hypergeometric p-value']),
#     data=data_incl_calculations,
#     hue='Enrichment Score',
#     palette="viridis",
#     edgecolor="w",
#     s=100,
#     alpha=0.6
# )

# Add labels to the points in the upper right quadrant
for i in range(len(data_incl_calculations)):
    enrichment_score = data_incl_calculations['Enrichment Score'].iloc[i]
    p_value_log = -np.log10(data_incl_calculations['Hypergeometric p-value'].iloc[i])
    if p_value_log > 5:  # Adjust threshold as needed
        plt.text(enrichment_score, p_value_log, data_incl_calculations['Domain name'].iloc[i], fontsize=9)


plt.title('Enrichment Score vs. Significance (-log10(p-value))')
plt.xlabel('Enrichment Score')
plt.ylabel('-log10(p-value)')

plt.grid(True)
plt.savefig(f"scatter_enrichment_pvalue_{inFile}.png")
plt.show()

# Scatterplot of Ratio in Yeast Set vs. Ratio in Protein Set with p-value heatmap
plt.figure(figsize=(10, 6))

# Plotting the scatterplot with the p-value heatmap (c is the p-value)
sc = plt.scatter(data_incl_calculations['Ratio in Yeast Set'],  # x-axis: Yeast Set
                 data_incl_calculations['Ratio in Protein Set'],  # y-axis: Protein Set
                 c=-np.log10(data_incl_calculations['Hypergeometric p-value']),  # Heatmap for p-values
                 cmap='viridis', s=100, alpha=0.6, edgecolor="w")

# Add color bar for p-value heatmap
cbar = plt.colorbar(sc)
cbar.set_label('-log10(p-value)')

# Add x=y line (diagonal)
x_y_line, = plt.plot([0, 0.1], [0, 0.2], linestyle='--', color='red', label='x=y')

# Set x-axis limit from 0 to 0.2
plt.xlim(0, 0.02)
plt.ylim(0,0.1)

# Adding title, labels, and grid
plt.title('Ratio in Yeast proteome vs. Ratio in combined protein set')
plt.xlabel('Ratio in Yeast proteome')  # x-axis
plt.ylabel('Ratio in combined protein set')  # y-axis
plt.grid(True)

# Add labels to the points in the upper left corner (where Ratio in Protein Set is much higher than Ratio in Yeast Set)
for i in range(len(data_incl_calculations)):
    ratio_protein = data_incl_calculations['Ratio in Protein Set'].iloc[i]
    ratio_yeast = data_incl_calculations['Ratio in Yeast Set'].iloc[i]

    # Define condition for upper left corner, where the domain is more enriched in the protein set than in yeast
    if ratio_protein > 0.04:
        # Get the domain name and remove '_dom' or '_domain' if present
        domain_name = data_incl_calculations['Domain name'].iloc[i]
        domain_name = domain_name.replace('_domain', '').replace('_dom', '')

        # Add the label to the plot
        plt.text(ratio_yeast, ratio_protein, domain_name, fontsize=9)

# Add legend for x=y line
plt.legend(handles=[x_y_line])

# Save and show the plot
plt.savefig(f"scatter_ratio_protein_yeast_{inFile}.png")
plt.show()
