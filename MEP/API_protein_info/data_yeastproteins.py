from IPython.core.display import display
from unipressed import UniprotkbClient

def get_accession_and_gene_from_organism(organism):
    info=[]
    for record in UniprotkbClient.search(
            query=f"(organism_id:{organism})",
            format="json", #"json" is also possible
            fields=["accession", "gene_names", "protein_name", "length", "sequence","mass"]
    ).each_record():
        #accession = (record["primaryAccession"])
        #display(record)
        if 'genes' in record and 'geneName' in record['genes'][0] and 'recommendedName' in record["proteinDescription"]:
            inputname= record['genes'][0]['geneName']['value']
            gene_name=record['genes'][0]
            protein_name= record['proteinDescription']['recommendedName']['fullName']['value']
        else:
            inputname= []
            gene_name= []
            protein_name= []
        data = {
            "input_name": f"{inputname}",
            "accession_protein": f"{record['primaryAccession']}",
            "gene names": f"{gene_name}", # hier wil ik eigenlijk alleen values van geneName en synonyms maar hoe weet ik niet
            "protein name": f"{protein_name}",
            "sequence": f"{record['sequence']['value']}",
            "length": f"{record['sequence']['length']}",
            "mass": f"{record['sequence']['molWeight']}"
        }
        info.append(data)
    return info

#organism_id = '559292'
#dat=get_accession_and_gene_from_organism(organism_id)

