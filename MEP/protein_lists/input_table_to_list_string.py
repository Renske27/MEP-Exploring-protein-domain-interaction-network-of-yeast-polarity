import pandas as pd
import os

protein_table=pd.read_csv('c:/Users/rensk/OneDrive/Documenten/studie/afstuderen/info pipeline/expanded protein list data/string/full around Cdc42-same settings as others/string_protein_annotations_fullCdc42.tsv', sep='\t', header=0)

# make protein list from protein_table collumn #node
protein_list = protein_table['#node'].drop_duplicates().tolist()

outputpath = 'C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/fullstr_Cdc42_settings'

# Check whether the specified path exists or not
isExist = os.path.exists(outputpath)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(outputpath)
   print("The new directory is created!")

outputfile = 'proteins_fullstrCdc42.txt'

with open(f"{outputpath}/{outputfile}", 'w') as fo:
    fo.write(', '.join([str(n) for n in protein_list]))

