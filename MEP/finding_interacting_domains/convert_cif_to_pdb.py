from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.PDBIO import PDBIO


def convert_cif_to_pdb(cif_file, pdb_file):
    # Initialize the parser and the structure object
    parser = MMCIFParser()
    structure = parser.get_structure('structure_id', cif_file)

    # Initialize the PDBIO object
    io = PDBIO()
    io.set_structure(structure)

    # Save the structure in PDB format
    io.save(pdb_file)


# Replace 'input.cif' with the path to your CIF file
# Replace 'output.pdb' with the desired output PDB file path
convert_cif_to_pdb('input.cif', 'output.pdb')