import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to extract interactions from a file
def extract_interactions(file_path):
    df = pd.read_csv(file_path, sep='\t')
    interactions = set(zip(df['Residue1_Number'], df['Residue2_Number']))
    return interactions

# Directories for comparison
dir_50 = '../data/list2_data/contacts_plDDT50unique'
dir_70 = '../data/list2_data/contactsAF2_plDDT50unique'

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
                'Num Interactions AF2': num_interactions_70,
                'Num Interactions AF3': num_interactions_50,
                'Percentage Overlap': percentage_overlap
            })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Capitalize protein names
results_df['Protein1'] = results_df['Protein1'].str.capitalize()
results_df['Protein2'] = results_df['Protein2'].str.capitalize()

# Load the score files for AF2 and AF3
scores_AF3 = 'scores_AF3_list2.tsv'
df_scoresAF3 = pd.read_csv(scores_AF3, sep='\t')

scores_AF2 = 'scores_AF2_list2_withoutduplicates.tsv'
df_scoresAF2 = pd.read_csv(scores_AF2, sep='\t')

# Capitalize protein names in the AlphaFold 3 score file
df_scoresAF3['protein1'] = df_scoresAF3['protein1'].str.capitalize()
df_scoresAF3['protein2'] = df_scoresAF3['protein2'].str.capitalize()


# Function to find the iPTM and PTM scores for a protein pair, accounting for possible name order swaps
def find_scores(df, protein1, protein2):
    scores = df[
        ((df['protein1'] == protein1) & (df['protein2'] == protein2)) |
        ((df['protein1'] == protein2) & (df['protein2'] == protein1))
    ]
    if not scores.empty:
        return scores['iPTM'].values[0], scores['PTM'].values[0]
    return None, None

# Add the iPTM and PTM scores to the results DataFrame
iptm_af2 = []
ptm_af2 = []
iptm_af3 = []
ptm_af3 = []

for i, row in results_df.iterrows():
    protein1 = row['Protein1']
    protein2 = row['Protein2']

    # Find scores for AF2
    iptm2, ptm2 = find_scores(df_scoresAF2, protein1, protein2)
    iptm_af2.append(iptm2)
    ptm_af2.append(ptm2)

    # Find scores for AF3
    iptm3, ptm3 = find_scores(df_scoresAF3, protein1, protein2)
    iptm_af3.append(iptm3)
    ptm_af3.append(ptm3)

# Add the scores to the results DataFrame
results_df['iPTM_AF2'] = iptm_af2
results_df['PTM_AF2'] = ptm_af2
results_df['iPTM_AF3'] = iptm_af3
results_df['PTM_AF3'] = ptm_af3


# Save the final DataFrame with interaction counts and iPTM/PTM scores
output_file_path = '../data/list2_data/interaction_overlap_AF2_AF3_with_scores_plDDT50_noscorethres.tsv.tsv'
results_df.to_csv(output_file_path, index=False, sep='\t')

print(f"Results with scores saved to {output_file_path}")

# Create the scatterplot of iPTM AF3 vs iPTM AF2 with a heatmap of percentage overlap
plt.figure(figsize=(10, 6))
sc = plt.scatter(results_df['iPTM_AF2'], results_df['iPTM_AF3'],
                 c=results_df['Percentage Overlap'], cmap='viridis', s=100, alpha=0.8, edgecolor="w") # cmap='coolwarm'

# Add a color bar for percentage overlap
cbar = plt.colorbar(sc)
cbar.set_label('Percentage Overlap')

# Add x=y line
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')

plt.title('iPTM AlphaFold3 vs iPTM AlphaFold2 with % Interacting Residue-pairs Overlap Heatmap')
plt.xlabel('iPTM AlphaFold2')
plt.ylabel('iPTM AlphaFold3')

plt.grid(True)
plt.tight_layout()
plt.savefig('iptm_af3_vs_af2_overlap_heatmap_plDDT50_noscorethres_viridis.png', dpi=300)
plt.show()