setup.py must be run before running download.py to ensure required packages are installed for the script to run. Python 3 is required

Run download.py, first you will have a file selection prompt appear. Select the location of the excel file
After this another prompt will appear for selecting a directory. This is for selecting the output directory of the pdf files.

PDF files will be saved under the name of ID.pdf, where the ID is the BRnum in the excel sheet.

If a pdf file of a given ID is already present in the download directory it will not be redownloaded, 
files that failed to download in previous runs will be attempted again

The result excel file will be put in the downloads folder, which contains the ID, if it was downloaded, and the error messages if the file failed to download

