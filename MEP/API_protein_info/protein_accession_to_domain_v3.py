# This function takes the accession number of a protein and uses the api of interpro
# to retrieve domain entries and info of the protein and return this info.
# This file also contains a function which decides which overlapping domains are relevant
# and returns the relevant info form these domains.
# This file is different from v2 in how domains that occur multiple times in a protein are stored.
# Every fragment is stored as a separate domain. I think this is easier to use later on.

import requests
import json
import os
def accession_to_family(accession_number):
    # Define the InterPro API endpoint and your accession number
    api_url = "https://www.ebi.ac.uk:443/interpro/api/entry/InterPro/protein/UniProt"
    # accession_number = "P29366"  # "P11433" # your_accession_number_here
    url_add_type = "?type=family&page_size=200&extra_fields=short_name"

    "https://www.ebi.ac.uk:443/interpro/api/entry/InterPro/protein/UniProt/P29366/?type=family&page_size=200&extra_fields=short_name"

    # Make the API request
    response = requests.get(f"{api_url}/{accession_number}/{url_add_type}")

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract and print domain information
        if 'results' in data and len(data['results']) > 0:
            number_entries = data['count']
            entries = data['results']
            return f"Accession number protein: {accession_number}", "No domain information found, used family instead.", entries
        else:
            return  f"Accession number protein: {accession_number}", "No domain and no family information found.", []
    elif response.status_code == 204:

        return f"Accession number protein: {accession_number}", "No domain and no family information found.", []
    else:  # if request gives an error code it returns error code.
        return f"Accession number protein: {accession_number}", f"Error: {response.status_code} - Unable to retrieve data.", []


def accession_to_domain(accession_number):
    # Define the InterPro API endpoint and your accession number
    api_url = "https://www.ebi.ac.uk:443/interpro/api/entry/InterPro/protein/UniProt"
    #accession_number = "P29366"  # "P11433" # your_accession_number_here
    url_add_type = "?type=domain&page_size=200&extra_fields=short_name"

    # Make the API request
    response = requests.get(f"{api_url}/{accession_number}/{url_add_type}")

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract and print domain information
        if 'results' in data and len(data['results']) > 0:
            number_entries = data['count']
            entries = data['results']
            # print(f"Protein:' {accession_number}")
            # print(f"Number of domain entries: {data['count']}")
            # print("------")
            # for entry in entries:
            #     print(f"InterPro ID: {entry['metadata']['accession']}")
            #     print(f"InterPro Name: {entry['metadata']['name']}")
            #     print(f"Type: {entry['metadata']['type']}")
            #     print(f"Protein Accession: {entry['proteins'][0]['accession']}")
            #     print(
            #         f"Domain Start: {entry['proteins'][0]['entry_protein_locations'][0]['fragments'][0]['start']}")  # Adjust as needed
            #     print(
            #         f"Domain End: {entry['proteins'][0]['entry_protein_locations'][0]['fragments'][0]['end']}")  # Adjust as needed
            #     print("------")
            return f"Accession number protein: {accession_number}", f"Number of domain entries: {number_entries}", entries
        else:
            data = accession_to_family(accession_number)
            return data
    elif response.status_code ==204:
        data = accession_to_family(accession_number)
        return data
    else: # if request gives an error code it returns error code.
        return f"Accession number protein: {accession_number}", f"Error: {response.status_code} - Unable to retrieve data.", []

def overlap_percentage(xlist,ylist): # this function calculates the average overlap ratio between two ranges.
    new_xlist=[float(i) for i in xlist] # this changes list of str in list of floats, which is needed to do calculations
    new_ylist= [float(j) for j in ylist] # this changes list of str in list of floats
    #print(f"floats of lists: {new_xlist,ylist}")
    min1=min(new_xlist)
    max1 = max(new_xlist)
    min2 = min(new_ylist)
    max2 = max(new_ylist)


    overlap = max(0, min(max1, max2) - max(min1, min2))
    length = max1-min1 + max2-min2
    lengthx = max1-min1
    lengthy = max2-min2

    return (overlap/lengthy)
    #2*overlap/length, overlap/lengthx  , overlap/lengthy)
#
# list= [100, 200]
# list2= [210,350]
# list3 = [60, 360]
# d4=[400, 600]
# d5= [500,580]
# d6=[300,600]
# print(overlap_percentage(list,list3))
# print(overlap_percentage(list2,list3))
# print(overlap_percentage(d4,d5))
# print(overlap_percentage(d5,d6))
# think I should take overlap/lengthy (so take overlap compared to domain lowest in hierarchy)

# %%

# putting a destination path were files will be saved
destination_path='C:/Users/rensk/Documents/studie/afstuderen/data/'
# Check whether the specified path exists or not
isExist = os.path.exists(destination_path)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(destination_path)
   print("The new directory is created!")


def find_relevant_domains(data):

    bib= []
    relevant_domains= []
    #z = open("relevant_domains.json", "w")

    for indx, d in enumerate(data[2]): #This loops over all domains within a protein
        domain= data[2][indx]
        total_overlap =[]
        count=0
        #print(domain)
        if domain["proteins"][0]["entry_protein_locations"] != None: # there are domains of which the database doesn't have info on location, we don't take these domains into account
            for index, l in enumerate(domain["proteins"][0]["entry_protein_locations"]):
                domain_name= domain["metadata"]["name"]
                #print(domain_name)
                for f in (l["fragments"]): # this loop iterates over all fragments that a domain has.
                    total_overlap.append(0)
                    locations=[(f"{f['start']}", f"{f['end']}")]

                    for item in bib: # this loop calcultates the overlap between next domain within a protein and the domain fragments already in bib
                        overlap= overlap_percentage(item,locations[0])
                        total_overlap[index]= total_overlap[index]+overlap



                    if total_overlap[index] < 0.75:
                        bib.append(locations[0])
                        #print(f"domain relevant ")
                        rel_data = {
                            'domain_name': f"{domain['metadata']['name']}",
                            'domain_shortname': f"{domain['extra_fields']['short_name']}",
                            'domain_accession': f"{domain['metadata']['accession']}",
                            'domain_start': f"{f['start']}",  # op deze manier doet het alleen 1 fragment toevoegen en niet allemaal...
                            'domain_end': f"{f['end']}"
                        }
                        count+=1
                        relevant_domains.append(rel_data)  # hier wil je eigenlijk dat alleen de relevante info wordt gepakt van het domain
                    #else:
                        #print(f"domain NOT relevant")
        #else:
            #print(f"domain NOT relevant, no location info")

        # # following statement adds domain when any of fragments has overlap of less than 0.75
        # # and stores the domain in relevant_domains
        # if any(x < 0.75 for x in total_overlap):
        #     print(f"domain relevant ")
        #
        #
        # else:
        #     print(f"domain NOT relevant")
        # print("----------")
    return relevant_domains #, count


## I will return relevant_domains. I can save them in the function to a file or in the code were I call the function.
# also something to think about is: do I want all domains of all proteins in 1 file or for every protein separate?
# At the moment I think per protein and then start with protein info; name, accession, length and sequence. Then the relevant domains.
    # the following I can use to write a dict to json.
    # with open('relevant_domains.json', 'w') as outfile:
    #     json.dump(relevant_domains, outfile)
            # with open('data.json', 'w') as f:
            #     json.dump(data, f)
            # z.write(domain)
            # save domain to relevant_domain json file


            # elif total_overlap[index] == []: # dit kan er uit total_overlap geeft dan 0.0 dus if statement geldt ook daarvoor.
            #     bib.append(locations)
        #     return True # dan in andere functie neer zetten if True then save entry in file. of gewoon hier. Beter gewoon hier opslaan in doc
        # else:
        #     return False # add to other function if False don't save entry in file. of gewoon hier. Beter gewoon hier doen

#data2= accession_to_domain('P36022')
#domains=find_relevant_domains(data2)
