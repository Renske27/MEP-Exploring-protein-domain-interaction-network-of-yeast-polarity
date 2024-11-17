import json
import pandas as pd
from matplotlib import pyplot as plt


# Function to read protein accessions from a JSON file
def read_protein_accessions_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract protein accessions from each JSON structure
    protein_accessions = {entry['accession_protein'] for entry in data}

    return protein_accessions


# Load the JSON files with protein accessions
protein_sets = {
    "All GO Terms": read_protein_accessions_from_json('../data/allGoterm_data/domains_proteins_allGOterms.json'),
    "Daalman": read_protein_accessions_from_json('../data/Daalman_data/domains_Daalman_proteinlist.json'),
    "String full Cdc42 Bem1 Cdc24": read_protein_accessions_from_json(
        '../data/fullstrCdc42Bem1Cdc24_data/domains_proteins_fullstrCdc42Bem1Cdc24.json'),
    "List2": read_protein_accessions_from_json('../data/list2_data/domains_protein_list2.json'),
    "String physical Cdc42 Bem1 Cdc24": read_protein_accessions_from_json(
        '../data/physstrCdc42Bem1Cdc24_data/domains_proteins_physstrCdc42Bem1Cdc24.json'),
    "Fullyeast": read_protein_accessions_from_json("../data/fullyeast_data/relevant_domains_yeast_all.json")
}

# Create a set of all unique protein accessions
all_proteins = set()
for proteins in protein_sets.values():
    all_proteins.update(proteins)

# Create a DataFrame to hold the comparison table
df = pd.DataFrame(index=sorted(all_proteins))

# Fill the DataFrame with presence/absence data
for set_name, proteins in protein_sets.items():
    df[set_name] = df.index.map(lambda protein: 1 if protein in proteins else 0)

# Save the comparison table as a CSV file
df.to_csv('protein_set_comparison_accession.csv')

# Optional: Visualize with a Venn diagram if comparing fewer sets
# If comparing more than 3 sets, Venn diagrams may not be ideal; consider heatmaps instead.
if len(protein_sets) <= 3:
    set_labels = list(protein_sets.keys())
    set_values = [proteins for proteins in protein_sets.values()]

    if len(set_values) == 2:
        venn2(subsets=(set_values[0], set_values[1]), set_labels=(set_labels[0], set_labels[1]))
    elif len(set_values) == 3:
        venn3(subsets=(set_values[0], set_values[1], set_values[2]),
              set_labels=(set_labels[0], set_labels[1], set_labels[2]))

    plt.show()



