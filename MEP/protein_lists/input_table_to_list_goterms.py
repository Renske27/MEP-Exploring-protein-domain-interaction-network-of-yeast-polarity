import pandas as pd
import os

protein_table=pd.read_csv('c:/Users/rensk/OneDrive/Documenten/studie/afstuderen/info pipeline/expanded protein list data/go terms list/QuickGO-annotations-all-polarity-GOprocesses.tsv', sep='\t', header=0)

#if protein_table['GENE PRODUCT DB'].str.contains('UniProtKB'):
protein_table = protein_table[protein_table['GENE PRODUCT DB']  != 'ComplexPortal']
protein_list = protein_table['SYMBOL'].drop_duplicates().tolist()

outputpath = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/allGoterm_data'

# Check whether the specified path exists or not
isExist = os.path.exists(outputpath)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(outputpath)
   print("The new directory is created!")

outputfile = 'proteins_allGOterms.txt'

with open(f"{outputpath}/{outputfile}", 'w') as fo:
    fo.write(', '.join([str(n) for n in protein_list]))

print(protein_list)