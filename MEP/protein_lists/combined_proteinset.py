def read_protein_list(file_path):
    with open(file_path, 'r') as file:
        proteins = file.read().split(', ')
    # Normalize protein names to have the first letter uppercase and the rest lowercase
    proteins = {protein.strip().capitalize() for protein in proteins}
    return proteins

# Load protein sets
protein_files = [
    '../data/combined_set/proteins_fullstrCdc42Bem1Cdc24.txt',
    '../data/combined_set/proteins_allGOterms.txt',
    '../data/combined_set/Daalman_proteinlist.txt'
]

# Combine protein sets without duplicates
all_proteins = set()
for file in protein_files:
    all_proteins.update(read_protein_list(file))

# Write combined protein list to a new file
with open('../data/combined_set/proteins_combinedset.txt', 'w') as output_file:
    output_file.write(', '.join(sorted(all_proteins)))

print(f"Combined protein list saved to ../data/combined_set/proteins_combinedset.txt with {len(all_proteins)} unique proteins.")
