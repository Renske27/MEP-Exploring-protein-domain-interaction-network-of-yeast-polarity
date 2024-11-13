#### removing the proteins only which domains are interacting
import os
import pandas as pd
from collections import defaultdict



# Path to the output CSV file
input_file = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/interactionmap_data/domain_contacts_plDDT70_noscorethres.csv'
interaction_data = pd.read_csv(input_file, sep='\t')

outfile = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/interactionmap_data/domain_only_interactions_plDDT70_noscorethes_v2.csv'

# Dictionaries to hold interaction counts and occurrence counts
domain_interaction_counts = defaultdict(int)  # Dictionary to sum all interacting residues for each domain-domain interaction
domain_interaction_occurrences = defaultdict(int)  # Dictionary to count occurrences of each domain-domain interaction

# Process each interaction
for _, row in interaction_data.iterrows():
    domain1_name = row['Domain1_Name']
    domain1_accession = row['Domain1_Accession']
    domain2_name = row['Domain2_Name']
    domain2_accession = row['Domain2_Accession']
    count=row['Count']

    if pd.isnull(domain1_name):
        domain1_name = 'other'
        domain1_accession = 'None'
    if pd.isnull(domain2_name):
        domain2_name = 'other'
        domain2_accession = 'None'

    # Count the interaction directly without reordering
    if ((domain1_name, domain1_accession, domain2_name, domain2_accession) in domain_interaction_counts):
        interaction_key = (domain1_name, domain1_accession, domain2_name, domain2_accession)
    elif ((domain2_name, domain2_accession, domain1_name, domain1_accession) in domain_interaction_counts):
        interaction_key = (domain2_name, domain2_accession, domain1_name, domain1_accession)
    else:
        interaction_key = (domain1_name, domain1_accession, domain2_name, domain2_accession)


    # Sum the counts and track occurrences
    domain_interaction_counts[interaction_key] += int(count)
    domain_interaction_occurrences[interaction_key] += 1

# Convert the interaction data to a DataFrame and calculate the average interacting residues
interaction_df = pd.DataFrame([
    {
        'Domain1_Name': k[0],
        'Domain1_Accession': k[1],
        'Domain2_Name': k[2],
        'Domain2_Accession': k[3],
        'Count': v,
        'Occurrences': domain_interaction_occurrences[k],
        'Average_Interacting_Residues': v / domain_interaction_occurrences[k]  # Calculate the average number of interacting residues
    }
    for k, v in domain_interaction_counts.items()
])

# Save the DataFrame to a TSV file
interaction_df.to_csv(outfile, sep='\t', index=False)

print(f"Saved data to {outfile}")

