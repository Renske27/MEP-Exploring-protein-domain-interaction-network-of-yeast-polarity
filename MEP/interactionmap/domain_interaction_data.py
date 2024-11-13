import os
import pandas as pd
from collections import defaultdict

# Directory containing the interaction files
interaction_files_dir = "C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/contacts_plDDT70unique"

scores_docking = "C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/scores_AF3_list2.tsv"

# Directory for output tsv files
output_dir = "C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/interactionmap_data"
# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
# outputfile
output_file = "domain_contacts_plDDT70_noscorethres.csv"
outfile_path = os.path.join(output_dir, output_file)

# Dictionary to hold interaction counts
interaction_counts = defaultdict(int)

# Load all interaction files
for filename in os.listdir(interaction_files_dir):

    if filename.endswith("_contacts.tsv"):
        file_path = os.path.join(interaction_files_dir, filename)
        interaction_data = pd.read_csv(file_path, sep='\t')
        scores = pd.read_csv(scores_docking,sep='\t')
        # Process each interaction
        for _, row in interaction_data.iterrows():
            protein1_name = row['Protein1']
            protein1_accession = row['Protein1_Accession']
            protein2_name = row['Protein2']
            protein2_accession = row['Protein2_Accession']
            for _, score_row in scores.iterrows():
                if protein1_name == score_row['protein1'] and protein2_name== score_row['protein2']:
                    # if score_row['iPTM']<0.2 and score_row['PTM']>0.5:
                    #     pass
                    # else:
                    if pd.isnull(row['Domain1_Name']):
                        domain1_name = 'other'
                        domain1_accession = 'None'
                    else:
                        domain1_name = row['Domain1_Name']
                        domain1_accession = row['Domain1_Accession']


                    if pd.isnull(row['Domain2_Name']):
                        domain2_name = 'other'
                        domain2_accession = 'None'
                    else:
                        domain2_name = row['Domain2_Name']
                        domain2_accession = row['Domain2_Accession']

                    # Count the interaction directly without reordering
                    if (protein1_name, protein1_accession, domain1_name, domain1_accession,
                        protein2_name, protein2_accession, domain2_name, domain2_accession) in interaction_counts:
                        interaction_counts[(protein1_name, protein1_accession, domain1_name, domain1_accession,
                            protein2_name, protein2_accession, domain2_name, domain2_accession)] += 1
                    else:
                        interaction_counts[(protein1_name, protein1_accession, domain1_name, domain1_accession,
                                protein2_name, protein2_accession, domain2_name, domain2_accession)] = 1
        print(f"Processed {filename}")

# Convert the interaction counts to a DataFrame
interaction_df = pd.DataFrame([
    {'Protein1': k[0], 'Protein1_Accession': k[1], 'Domain1_Name': k[2], 'Domain1_Accession': k[3],
    'Protein2': k[4], 'Protein2_Accession': k[5], 'Domain2_Name': k[6], 'Domain2_Accession': k[7],
     'Count': v}
     for k, v in interaction_counts.items()
])

# Save the DataFrame to a TSV file
interaction_df.to_csv(outfile_path, sep='\t', index=False)

print(f"Saved data to {output_file}")


