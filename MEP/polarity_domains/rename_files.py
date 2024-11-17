import os

# Load protein names from the FASTA file
def load_protein_names(fasta_file):
    protein_names = {}
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                parts = line.split('|')
                uniprot_id = parts[1]
                protein_name = parts[2].split(' ')[0]
                protein_names[uniprot_id] = protein_name
    return protein_names

# Rename PDB files
def rename_pdb_files(pdb_dir, protein_names):
    for filename in os.listdir(pdb_dir):
        if filename.startswith('AF-') and filename.endswith('.pdb'):
            parts = filename.split('-')
            uniprot_id = parts[1]
            if uniprot_id in protein_names:
                new_filename = f"{protein_names[uniprot_id]}.pdb"
                os.rename(os.path.join(pdb_dir, filename), os.path.join(pdb_dir, new_filename))
                print(f"Renamed {filename} to {new_filename}")

# Paths
pdb_dir = "'C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/SH3_pdbs/"  # Change to your PDB directory
fasta_file = "proteins_SH3.fasta"  # Change to your FASTA file

# Load protein names and rename PDB files
protein_names = load_protein_names(fasta_file)
rename_pdb_files(pdb_dir, protein_names)
