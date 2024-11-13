# %%
# run this script using following command in terminal: python get_data_proteins_v2.py inputfile.txt outputfile.json
# input file is comma separated list of proteins: Cdc42, Cdc24, ...
# output file is json format of relevant domains, filename = relevant_domains_inputfile.json
# importing self created functions.
from data_yeastproteins import *
from protein_accession_to_domain_v3 import *
from getting_PDB import *

#import sys
#inFile = sys.argv[1]
#outFile = sys.argv[1]





#gene_name = 'CDC42'  # your_gene_name_here
organism_id = '559292'  # your_organism_id_here, strain ATCC 204508 / S288c (deze had ik eerst)
#organism_id = '4932'  # your_organism_id_here, bakers yeast

# create empty lists for protein and domain info. Maybe better to store this info into a file which is saved in data directory.
protein_domain_info =[]
#domain_info_per_protein = []
alphafold_info =[]
info=[]
# this loop takes the first protein in the list and calls the function to get accession and other info of the protein.
# this info is stored in  protein_info list.
# The accession is used to get the domain info with the accession_to_domain function
# the domain info is stored in domain_info_per_protein
# the pdb files are stored in the specified directory.
# I run now all functions within one for loop, but could also separate these parts,maybe thats better
#for index, item in enumerate(proteins): ### ik loop hier over de list maar nu is er geen list.

data = get_accession_and_gene_from_organism(organism_id)

for index, item in enumerate(data):
    protein_info=data[index]
    print(index)
    if 'accession_protein' in protein_info:
        accession = protein_info['accession_protein'] # getting the accession number from data

        data2=accession_to_domain(accession)
        if not data2[2]:
            rel_domains = [] # moet info full protein dan op zelfde manier opslaan als de domains opsla
        else:
            rel_domains=find_relevant_domains(data2)

       #print(rel_domains)

        protein_info.update({"domains": rel_domains})

    protein_domain_info.append(protein_info)
    #print(protein_domain_info)
    #domain_info_per_protein.append(rel_domains) #store data2

   # next two lines get the alphafold pdb files for an accession number and store it in the desirate location.
# accession, alphafold id and date of model are saved in alphafold_info
# I commented out these 2 lines for now, because I have already all files now.
    # data3 =accession_to_PDB(accession)
    # alphafold_info.append(data3)



# %%
# The following creates a file and stores the info from protein_domain_ info in json format in the file with name as listed after the open commend
outputdir= "../data/fullyeast_data"
outFile='relevant_domains_yeast_all.json'

#with open('protein_domain_info_list2.json', 'w+') as outfile:
with open(f"{outputdir}/{outFile}", 'w+') as outfile:
    # Convert dictionary to JSON string
     json.dump(protein_domain_info, outfile, indent=2)