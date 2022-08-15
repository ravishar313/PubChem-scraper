# PubChem-scraper
Drug discovery is a very long and cumbersome process. With the advent of computational methods like molecular docking and simulations, the burden has been reduced to some extent. But the process of creating, dowloading and coverting files required for docking is very repititive. 

In most cases, when a lead compound for a drug is found, we search for other similar compounds to see if they show any increase affinity towards the protein of interest. Databases like PubChem, ChEMBL, etc are used to search for compounds that are similar to the lead compound. PubChem is very famous and commonly used database of chemical molecules and their activities. It is maintained by National Center for Biotechnology Information (NCBI) under National Institute of Health (NIH), USA. PubChem is a very useful database for searching chemcial structures. The searching process using these databases can be very manual and take a lot of human efforts. To automate the searching process, I have created this tool as an extension of the previous PDBQGT extractor. This tool searches the PubChem database for compounds similar to the input compounds and extracts the sdf files of ligand molecules from PubChem. For docking, Autodock files known as PDBQT files are required, so the sdf files downloaded from PubChem needs to be converted to PDBQT files to make them ready for docking against protein of interest. This conversion is achieved through OpenBabel. OpenBabel is a widely used molecule file format convereter software. It is available as a linux command line tool. NOTE: The conversion should not be trusted blindly. A manual check may be required to see if the 3D structure and bond orders are correct.

For using this tool, You only need to either have the structure of the compound as a pqb, pqbqt, sdf file, or the SMILE or the CID of the compound.

You may need to install the following python packages:
1. sys
2. subprocess
3. wget
4. pandas
5. csv
6. os

The script needs to be run as follows on your linux terminal:
$ython Pubchem_scrapper.py molecule.file SMILE CID_of_the_compound
Where molecule.file is the structure file of the compound, SMILE is the SMILE (Simplified Molecular Input Line Entry System) of the compound and CID_of_the_compound is the CID of the compound of interest. Giving only one argument is required, for the rest, the value should be set to 0.

Future prospects: To include more databases into the search and creating non-redundant search results.
