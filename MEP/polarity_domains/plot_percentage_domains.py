import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend
import matplotlib.pyplot as plt
import sys
from Data_to_file import *
import numpy as np

# Read the TSV file into a DataFrame
inDir = sys.argv[1] # directory within data dir which contains json file with protein domain info
inFile = sys.argv[2] # inputfile as argument in terminal percentage_domains_[name].tsv

file_path = '../data/'
inFile_path = f"{file_path}/{inDir}/{inFile}"
df = pd.read_csv(inFile_path, sep='\t')


# Extract the domain coverage percentages as a list
coverage_percentages = df['%_domain'].astype(float)

# Calculate the frequency distribution
frequency_distribution, bins = np.histogram(coverage_percentages, bins=20)

# Calculate the total number of proteins
total_proteins = len(df)

# Calculate the frequency divided by the total number of proteins
frequency_normalized = frequency_distribution / total_proteins

# Plot the histogram
plt.bar(bins[:-1], frequency_normalized, width=bins[1]-bins[0], color='skyblue', edgecolor='black')
plt.title('Normalized Protein Domain Coverage Distribution')
plt.xlabel('Percentage of Protein Covered by Domains')
plt.ylabel('Frequency (Normalized)')
plt.ylim(0,0.55)
plt.xlim(0,100)
#plt.grid(True)

# # Extract the domain coverage percentages as a list
# coverage_percentages = df['%_domain'].astype(float)
#
# # Plot the histogram
# plt.hist(coverage_percentages, bins=20, color='skyblue', edgecolor='black')
# plt.title(f'Protein Domain Coverage Distribution')
# plt.xlabel('Percentage of Protein Covered by Domains')
# plt.ylabel('Frequency')
# plt.grid(True)
# plt.xlim(0, 100)


# Save the figure
output_file = output_file_frontextension('plot_nor',inFile, 'png')
outfile_path = f"{file_path}/{inDir}/{output_file}"
plt.savefig(outfile_path, dpi=300,bbox_inches='tight')  # dpi argument sets the resolution (dots per inch)
#plt.show()