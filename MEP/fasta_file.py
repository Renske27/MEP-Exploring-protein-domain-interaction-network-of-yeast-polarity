import json
import sys
inFile = sys.argv[1]
outFile = sys.argv[2]

def fasta(inputfile,outputfile):
    data = json.load(inputfile)

    for indx, i in enumerate(data):
        protein_name = data[indx]['input_name']
        seq= data[indx]['sequence']
        outputfile.write(
            f">{protein_name} \n"
            f"{seq} \n"
        )



inf=open(inFile)
outf=open(outFile,'w')
fasta(inf,outf)

inf.close()
outf.close()