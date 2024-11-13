# this file will test how often the domains within the protein lists (protein lists specific for polarity)
# occur in comparison with how often the same domains occur in the whole yeast proteome.
import pandas as pd
import sys
from Data_to_file import *
import math

# inputfiles
data_yeast=pd.read_csv('../data/fullyeast_data/count_relevant_domains_yeast_all.tsv', sep='\t')
inDir = sys.argv[1] # directory within data dir which contains json file with protein domain info
file = sys.argv[2] # count_...
amount_proteins_in_list= int(sys.argv[3])


file_path = '../data/'
inFile_path = f"{file_path}/{inDir}/{file}"


data_list = pd.read_csv(inFile_path,sep='\t')


# Function to search for a string in the first column of DataFrame
# and return corresponding entry from the third column
def search_string_in_dataframe(df, string):
    row_values = df[df['Unnamed: 0'] == string]['Count'].values
    if len(row_values) > 0:
        return row_values
    else:
        print(f"Accession {string} not found in yeast data")
        return 0





def ratio_domain_count(df_list, df_yeast,):
    ratio_count=[]
    for ind in df_list.index:
        accession= df_list['Unnamed: 0'][ind]
        count_list= df_list['Count'][ind]

        # Search for the domain count in the yeast DataFrame
        count_yeast = search_string_in_dataframe(df_yeast, accession)
        ratio=count_list/count_yeast

        ratio_count.append(ratio)


    # Using DataFrame.insert() to add a column
    df_list.insert(3, "Ratio", ratio_count, True)
    return df_list

def domain_occurance(df_list, df_yeast,no_proteins):
    ratio_list_count=[]
    ratio_yeast_count=[]
    ratio_ratio=[]
    for ind in df_list.index:
        accession= df_list['Unnamed: 0'][ind]
        count_list= df_list['Count'][ind]

        # Search for the domain count in the yeast DataFrame
        count_yeast = search_string_in_dataframe(df_yeast, accession)
        ratio_list = count_list / (no_proteins)  # amount of proteins in list
        ratio_yeast = count_yeast / 6766  # amount of proteins full_yeast list
        if ratio_yeast != 0:
            ratio_from_ratio = ratio_list / ratio_yeast
        else:
            ratio_from_ratio = math.inf

        ratio_list_count.append(ratio_list)
        ratio_yeast_count.append(ratio_yeast)
        ratio_ratio.append(ratio_from_ratio)

    # Using DataFrame.insert() to add a column
    df_list.insert(3, "N_dl/N_pl / N_dy/N_py", ratio_yeast_count, True)
    df_list.insert(4, "N_d_list/N_p_list", ratio_list_count, True)
    df_list.insert(5, "N_d_yeast/N_p_yeast", ratio_yeast_count, True)

    return df_list

data_list2= domain_occurance(data_list,data_yeast,amount_proteins_in_list)


# %%
#Save the updated DataFrame to a new file
output_file = output_filename(file,'with_ratios','tsv')
outfile_path = f"{file_path}/{inDir}/{output_file}"
data_list2.to_csv(outfile_path, sep='\t', index=False)

print(f"saved data to {output_file}")




