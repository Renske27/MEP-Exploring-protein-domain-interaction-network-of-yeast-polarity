import os
import json
import pandas as pd
from Bio.PDB import MMCIFParser, NeighborSearch


# Function to get domain information for a given residue number in a protein
def get_domain_info(protein, residue_num, domains_json):
    # Convert the protein name to lower case for case-insensitive comparison
    protein_lower = protein.lower()
    # Iterate through the data to find the specified protein
    for protein in domains_json:
        if protein['input_name'].lower() == protein_lower:
            protein_accesion = protein['accession_protein']

            # Iterate through the domains to check if the residue is within any domain
            for domain in protein['domains']:
                if int(domain['domain_start']) <= residue_num <= int(domain['domain_end']):
                    return domain['domain_name'], domain['domain_accession'], protein['accession_protein'] #domain['domain_shortname']
            # Return None if no domain is found
            return None, None, protein_accesion


# Function to save contacts data to a TSV file
def save_contacts_to_tsv(output_file, contacts_data):
    # Create a DataFrame from the contacts data
    df = pd.DataFrame(contacts_data, columns=[
        'Protein1','Protein1_Accession', 'Atom1', 'Atom1_Number', 'Residue1', 'Residue1_Number', 'Domain1_Name', 'Domain1_Accession',
        'Protein2', 'Protein2_Accession', 'Atom2', 'Atom2_Number', 'Residue2', 'Residue2_Number', 'Domain2_Name', 'Domain2_Accession'
    ]) # can add domain shortnames to this...
    # Save the DataFrame to a TSV file
    df.to_csv(output_file, sep='\t', index=False)

    print(f"Contact information saved to {output_file}")



# Function to find interacting domains and generate output files
def find_interacting_domains(input_dir, output_dir, json_file,plDDT):
    # Load relevant domains from JSON file
    with open(json_file, 'r') as f:
        relevant_domains = json.load(f)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    parser = MMCIFParser(QUIET=True)

    # Iterate through each file in the input directory and only use the cif files which end with _model_0
    for dirpath, dirnames, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith("_model_0.cif"):
                try:
                    # Extract protein names from the filename
                    protein1, protein2 = filename.split('_')[3:5]
                    cif_path = os.path.join(dirpath, filename)

                    # Parse the CIF file to get the structure
                    structure = parser.get_structure(protein1 + '_' + protein2, cif_path)
                    model = structure[0]  # Assuming we are dealing with the first model

                    # Get the chains from the model
                    chains = list(model.get_chains())
                    if len(chains) < 2:
                        print(f"Error: Expected at least 2 chains in {filename}, but found {len(chains)}")
                        continue

                    chain1 = chains[0]
                    chain2 = chains[1]

                    # Get atoms from the chains
                    atoms1 = list(chain1.get_atoms())
                    atoms2 = list(chain2.get_atoms())

                    # Initialize NeighborSearch with atoms from both chains
                    ns = NeighborSearch(atoms1 + atoms2)
                    contacts = ns.search_all(4.0)  # 4.0 Ångström cutoff

                    contacts_data = []
                    for atom1, atom2 in contacts:
                        if atom1 in atoms1 and atom2 in atoms2:
                            residue1 = atom1.get_parent()
                            residue2 = atom2.get_parent()

                            # Check plDDT (B-factor) scores
                            plddt1 = atom1.get_bfactor()
                            plddt2 = atom2.get_bfactor()
                            if plddt1 < plDDT or plddt2 < plDDT:
                                continue  # Skip this interaction if either score is below threshold

                            # Get domain info for the residues
                            domain1 = get_domain_info(protein1, residue1.get_id()[1], relevant_domains)
                            domain2 = get_domain_info(protein2, residue2.get_id()[1], relevant_domains)

                            # Append contact information to the list
                            contacts_data.append([
                                protein1, domain1[2],
                                atom1.get_name(), atom1.get_serial_number(),
                                residue1.get_resname(),residue1.get_id()[1],
                                domain1[0], domain1[1],
                                protein2, domain2[2],
                                atom2.get_name(), atom2.get_serial_number(),
                                residue2.get_resname(), residue2.get_id()[1],
                                domain2[0], domain2[1]
                            ])

                    # Define the output file path
                    output_file = os.path.join(output_dir, f"{protein1}_{protein2}_contacts.tsv")
                    save_contacts_to_tsv(output_file, contacts_data)
                    #print(f"saved contacts to {output_file}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")



# Paths AF3
data_dir = "C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/alphafold3/unpacked_unique"
output_dir_plDDT50 = "C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/contacts_plDDT50"
output_dir_plDDT70 = "C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/contacts_plDDT70"
json_file = "C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/domains_protein_list2.json"



# Find interacting domains
find_interacting_domains(data_dir, output_dir_plDDT50, json_file,50)
find_interacting_domains(data_dir, output_dir_plDDT70, json_file,70)
