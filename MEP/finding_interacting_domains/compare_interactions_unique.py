import os
import pandas as pd


# Function to extract interactions from a file
def extract_interactions(file_path):
    df = pd.read_csv(file_path, sep='\t')
    interactions = set(zip(df['Residue1_Number'], df['Residue2_Number']))
    return interactions


# Directories for comparison
dir_50 = '../data/list2_data/contactsAF2_unique'
dir_70 = '../data/list2_data/contacts2_unique'

# Initialize a list to store the results
results = []

# Iterate over files in the plDDT50unique directory
for filename_50 in os.listdir(dir_50):
    if filename_50.endswith('_contacts.tsv'):
        protein1, protein2 = filename_50.replace('_contacts.tsv', '').split('_')
        file_path_50 = os.path.join(dir_50, filename_50)

        # Find the corresponding file in plDDT70unique directory
        possible_filenames = [
            f"{protein1}_{protein2}_contacts.tsv",
            f"{protein2}_{protein1}_contacts.tsv"
        ]

        file_path_70 = None
        for possible_filename in possible_filenames:
            if os.path.exists(os.path.join(dir_70, possible_filename)):
                file_path_70 = os.path.join(dir_70, possible_filename)
                break

        # If a matching file is found in both directories, compare the interactions
        if file_path_70:
            interactions_50 = extract_interactions(file_path_50)
            interactions_70 = extract_interactions(file_path_70)

            num_interactions_50 = len(interactions_50)
            num_interactions_70 = len(interactions_70)

            overlap = interactions_50.intersection(interactions_70)
            num_overlap = len(overlap)

            if num_interactions_50 > 0:
                percentage_overlap = (num_overlap / num_interactions_50) * 100
            else:
                percentage_overlap = 0

            # Store the results
            results.append({
                'Protein1': protein1,
                'Protein2': protein2,
                'Num Interactions AF2': num_interactions_50,
                'Num Interactions AF3': num_interactions_70,
                'Percentage Overlap': percentage_overlap
            })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a TSV file
output_file_path = '../data/list2_data/interaction_overlap_AF2_AF3.tsv'
results_df.to_csv(output_file_path, index=False, sep='\t')

print(f"Results saved to {output_file_path}")

# Load the data from the uploaded TSV file
scores_AF3 = 'scores_AF3_list2.tsv'
df_scoresAF3 = pd.read_csv(scores_AF3, sep='\t')

scores_AF2 = 'scores_AF2_list2.tsv'
df_scoresAF2 = pd.read_csv(scores_AF2, sep='\t')


