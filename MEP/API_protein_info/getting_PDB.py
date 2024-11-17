import wget
import requests, sys, json
import ipywidgets as wgt
from urllib.request import urlopen
import os


# putting a destination path were files will be saved
destination_path='C:/Users/rensk/Documents/studie/afstuderen/data/alphafold_pdb'
# Check whether the specified path exists or not
isExist = os.path.exists(destination_path)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(destination_path)
   print("The new directory is created!")


# Function to download a file from a given URL and save it to chosen destination path
# I want to add that when file is already there it overwrites it I think
def download_file(url):
    os.chdir(destination_path)
    filename = wget.download(url)


def accession_to_PDB(accession_number):
    # Define the InterPro API endpoint and your accession number
    api_url = "https://alphafold.ebi.ac.uk/api/prediction"
    #accession_number = "P29366"  # "P11433" # your_accession_number_here
    url_add_type = "?key=AIzaSyCeurAJz7ZGjPQUtEaerUkBZ3TaBkXrY94"

    # Make the API request
    response = requests.get(f"{api_url}/{accession_number}{url_add_type}")

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract and print domain information
        #if 'results' in data and len(data['results']) > 0:
        if len(data) > 0:
            entryID= data[0]["entryId"]
            modelcreationdate= data[0]["modelCreatedDate"]
            #if 'pdbUrl' in data: # when I add this if statement it doesn't work without it, it does. Think I can leave this if-statement out.
            url_pdb= data[0]["pdbUrl"]
            download_file(url_pdb)

            return f"Accession number protein: {accession_number}", f"entry ID: {entryID}", f"Creation date model: {modelcreationdate}", f"url_pdb: {url_pdb}"

        else:
            return f"Accession number protein: {accession_number}", "No information found."
    else: # if request gives an error code it returns error code.
        return f"Accession number protein: {accession_number}", f"Error: {response.status_code} - Unable to retrieve data."

