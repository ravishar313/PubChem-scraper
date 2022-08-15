#the person running the code needs to run it as follows:
#command is as follows: python Pubchem_scrapper.py molecule.file SMILE CID_of_the_compound
#giving only one argument is required, for the rest, the value should be set to 0

import sys
import subprocess
import wget
import pandas as pd
import csv
import os

SMILE=''
Input_CID=''

#converting the input strings to terms that can be added into the url. Replacing certain characters with others.

if sys.argv[1] != str(0):
    print('first argument taken') #confirming input selected
    print(type(sys.argv[1]))
    inputfile=sys.argv[1]
    subprocess.run('obabel ' + inputfile + ' -O molecule.smi',shell=True,stdout=subprocess.PIPE,check=True,universal_newlines=True) #running commands  on the linux subsytem as obabel package is available for linux. Obabel will convert the file formats.
    data=[]
    with open('molecule.smi','r') as mol:
        for i in mol:
            data.append(i)
    SMILE_string=data[0]        
    Molecule=SMILE_string.split('\t')[0] #changing characters
    SMILE=Molecule.replace('=','%3D')
    SMILE=SMILE.replace('[','%5B')
    SMILE=SMILE.replace('@','%40')
    SMILE=SMILE.replace(']','%5D')
    
elif sys.argv[2] != str(0):
    print('second argument taken') #confirming input
    Molecule=sys.argv[2]
    SMILE=Molecule.replace('=','%3D') #changing characters
    SMILE=SMILE.replace('[','%5B')
    SMILE=SMILE.replace('@','%40')
    SMILE=SMILE.replace(']','%5D')
    
elif sys.argv[3] != str(0):
    print('third argument taken') #confirming input
    Molecule=sys.argv[3]
    Input_CID=Molecule+'%20structure' #


#link for SMILE as input
if SMILE!='':
    url='https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?infmt=json&outfmt=csv&query={%22download%22:%22*%22,%22collection%22:%22compound%22,%22where%22:{%22ands%22:[{%22input%22:{%22type%22:%22netcachekey%22,%22idtype%22:%22cid%22,%22key%22:%2276hJLaw3yYv-pUG8w8QIkNVN-i0XmzzoRs0npF3cNaVdxQk%22}}]},%22order%22:[%22relevancescore,desc%22],%22start%22:1,%22limit%22:10000000,%22downloadfilename%22:%22PubChem_compound_smiles_similarity_'+SMILE+'%22}' 

#link for CID as input
elif Input_CID!='':
    url='https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?infmt=json&outfmt=csv&query={%22download%22:%22*%22,%22collection%22:%22compound%22,%22where%22:{%22ands%22:[{%22input%22:{%22type%22:%22netcachekey%22,%22idtype%22:%22cid%22,%22key%22:%22UBf2k99HuvuN0bjIOrDx5CwxdVF7nDZdTHgtEVdpPxBXcAM%22}}]},%22order%22:[%22relevancescore,desc%22],%22start%22:1,%22limit%22:10000000,%22downloadfilename%22:%22PubChem_compound_structure_by_cid_similarity_CID'+Input_CID+'%22}'

print(url)

#downloading the csv files containing details of the similar compounds
respone=wget.download(url,'data.csv')

#getting the path of the downloaded csv file
path=os.getcwd()
path = path + '\data.csv'

#cleaning the datafiles and extracting the CIDs
df=pd.read_csv(path) #saving the csv file as panda dataframe

#Making more uniform column labels
df=df.rename(columns={'cid':'CID','cmpdname':'Compound Name','mw':'Molecular Weight','mf':'Molecular Formula','iupacname':'IUPAC Name'})

#cleaning the data and keeping the required data only
df_clean=df[['CID','Compound Name','Molecular Weight','Molecular Formula','IUPAC Name']]
print(df_clean)

#saving the CIDs as a list
CIDs=df_clean['CID']


#downloading the SDF files for the CIDs
for i in CIDs:
    SDF_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/240/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID_'+str(i)
    filename= str(i)+'.sdf'
    download_CID=wget.download(SDF_url, filename)
    print(filename+ ' downloaded') #confirming download
    
#making a folder in the cwd and moving all the sdf file there
subprocess.run('mkdir sdffiles',shell=True,stdout=subprocess.PIPE,check=True,universal_newlines=True)
subprocess.run('mv *.sdf sdffiles',shell=True,stdout=subprocess.PIPE,check=True,universal_newlines=True)

#since for docking pdbqt files are required, we convert the downloaded sdf files to pdbqt files
#coverting the sdf files to pdbqt files
for i in CIDs:
    input_file=str(i)+'.sdf'
    output_file=str(i)+'.pdbqt'
    subprocess.run('obabel '+input_file+' -O '+output_file+' --gen3d',shell=True,stdout=subprocess.PIPE,check=True,universal_newlines=True)
    print(input_file + ' coverted')

print('SUCCESS!')