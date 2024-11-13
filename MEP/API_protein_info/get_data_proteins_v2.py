# %%
# run this script using following command in terminal: python get_data_proteins_v2.py inputfile.txt outputfile.json
# input file is comma separated list of proteins: Cdc42, Cdc24, ...
# output file is json format of relevant domains, filename = relevant_domains_inputfile.json
# importing self created functions.
from gene_to_accession import *
from protein_accession_to_domain_v3 import *
from getting_PDB import *
from Data_to_file import *

import sys
inDir = sys.argv[1] # directory within data dir which contains proteinlist.txt file
inFile = sys.argv[2]    # filename of proteinlist.txt


#outFile = sys.argv[2]
inFile_path = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/'

# open the text file with the list of proteins in following format: Cdc42, Cdc24,
with open(f"{inFile_path}/{inDir}/{inFile}", 'r') as f:
#with open('../protein_list2.txt') as f:
    proteins = f.read().split(', ')

# putting a destination path were files will be saved
destination_path='C:/Users/rensk/Documents/studie/afstuderen/data/'
# Check whether the specified path exists or not
isExist = os.path.exists(destination_path)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(destination_path)
   print("The new directory is created!")

#gene_name = 'CDC42'  # your_gene_name_here
organism_id = '559292'  # your_organism_id_here, strain ATCC 204508 / S288c


# create empty lists for protein and domain info. Maybe better to store this info into a file which is saved in data directory.
protein_domain_info =[]
#domain_info_per_protein = []
alphafold_info =[]
errors = []
# this loop takes the first protein in the list and calls the function to get accession and other info of the protein.
# this info is stored in  protein_info list.
# The accession is used to get the domain info with the accession_to_domain function
# the domain info is stored in domain_info_per_protein
# the pdb files are stored in the specified directory.
# I run now all functions within one for loop, but could also separate these parts,maybe thats better
for index, item in enumerate(proteins):
   #gene_name = item
    data = get_accession_from_gene_and_organism(item, organism_id)
    #print(item)
    #protein_info.append(data) # store data
    #print(index)

    if data == None:
        errors.append(f"For protein {item} no protein info is found on Uniprot")

        data ={
            "input_name": f"{item}",
            "accession_protein": "None",
            "domains": []
        }

    else:
        accession = data['accession_protein'] # getting the accession number from data
        data2=accession_to_domain(accession)
        if not data2[2]:
            errors.append(f"Protein {item} gives error: {data2}")
            rel_domains = [] # moet info full protein dan op zelfde manier opslaan als de domains opsla
        elif data2[1] == "No domain information found, used family instead.":
            errors.append(f"Protein {item} gives error: {data2[0]} {data2[1]}")
            rel_domains = find_relevant_domains(data2)
        else:
            rel_domains=find_relevant_domains(data2)



        data.update({"domains": rel_domains})

    protein_domain_info.append(data)
    #domain_info_per_protein.append(rel_domains) #store data2

   # next two lines get the alphafold pdb files for an accession number and store it in the desirate location.
# accession, alphafold id and date of model are saved in alphafold_info

    # data3 =accession_to_PDB(accession)
    # alphafold_info.append(data3)



# %%
# The following creates a file and stores the info from protein_domain_ info in json format in the file with name as listed after the open commend
outFile=output_file_frontextension('domains', inFile,'json')

#with open('protein_domain_info_list2.json', 'w+') as outfile:
with open(f"{inFile_path}/{inDir}/{outFile}", 'w+') as outfile:
    # Convert dictionary to JSON string
     json.dump(protein_domain_info, outfile, indent=2)

# The following stores all errors to a text file
outF_errors = 'errors.txt'
with open(f"{inFile_path}/{inDir}/{outF_errors}",'w') as f:
    f.write('\n'.join([str(n) for n in errors]))

print(f"Saved protein and domain info to {outFile}")