# This function takes a gene nane and organism_id and searches uniprot,
# to find and return accession, gene names, length of protein and sequence of protein
from IPython.core.display import display
from unipressed import UniprotkbClient
import json
def get_accession_from_gene_and_organism(gene_name, organism):
    for record in UniprotkbClient.search(
            query=f"(gene:{gene_name}) AND (organism_id:{organism})",
            format="json", #"json" is also possible
            fields=["accession", "gene_names", "protein_name", "length", "sequence","mass"]
    ).each_record():
        # accession = (record["primaryAccession"])
        # display("input:",  record)
        data = {
            "input_name": f"{gene_name}",
            "accession_protein": f"{record['primaryAccession']}",
            "gene names": f"{record['genes'][0]}", # hier wil ik eigenlijk alleen values van geneName en synonyms maar hoe weet ik niet
            "protein name": f"{record['proteinDescription']['recommendedName']['fullName']['value']}",
            "sequence": f"{record['sequence']['value']}",
            "length": f"{record['sequence']['length']}",
            "mass": f"{record['sequence']['molWeight']}"
        }
        return data



# %% dit is hoe ik de data van dictonary to json file kan opslaan.
# info= get_accession_from_gene_and_organism('Bem1','559292')
# print(info)
# with open('relevant_domains.json', 'w') as outfile:
#     # Convert dictionary to JSON string
#      json.dump(info, outfile)

