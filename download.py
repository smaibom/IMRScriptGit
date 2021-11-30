
import pandas
import requests
import PyPDF2
import os
import multiprocessing
from os.path import exists
import time
import tkinter as tk
import tkinter.filedialog

def import_excel_data(filename):
    """
    Imports excel data from a given file

    Input:
        filename : String path to the excel file

    Returns:
        arr : Pandas dataframe of all the excel data from the given path, None if file is not found or is wrong dataformat
    """
    try:
        df = pandas.read_excel(filename)
        return (True,df)
    except:
        return (False,None)


def save_excel_data(df,output_name):
    """
    Saves a pandas dataframe to an excel file

    Input:
        df: Pandas dataframe
        output_name: String of the path to be saved
    """
    try:
        df.to_excel(output_name,index=False)
    except:
        return





def get_urls_from_dataframe(df):
    """
    Gets the Id, MainUrl, BackupUrl from the pandas dataframe. Requires the following fields in the excel file:
        "BRnum", "Pdf_URL" and "Report Html Address"

    Input:
        pd : Pandas dataframe with the data loaded

    Returns:
        Pandas dataframe filtered for id,primaryUrl,backupUrl, 
        None if the required fields do not exists
    """
    id = "BRnum"
    primaryUrl = "Pdf_URL"
    backupUrl = "Report Html Address"
    try:
        return df[[id,primaryUrl,backupUrl]]
    except:
        return None


def check_pdf_file(filename):
    """
    Checks if a file is a valid pdf file

    Input:
        filename: String of the path to the file

    Returns:
        True on valid file, False otherwise
    """
    try:
        with open(filename,"rb") as fp:
            PyPDF2.PdfFileReader(fp,strict = False)
            return True
    except:
        return False



def download_pdf(url,filepath):
    """
    Downloads a pdffile from a given url. If successfull it returns True with the file name, else False with the error that occured


    Input:
        url : String to the url of the file
        filepath : String of the path to save the pdf file


    Returns:
        (Bool,String) : True on success with the 
    """

    try:
        with requests.get(url,stream=True,timeout=10) as req:
            if req.status_code != 200:
                return (False,"Error status code %s" %req.status_code)
            req.raise_for_status()
            with open(filepath,"wb") as f:
                for chunk in req.iter_content(chunk_size=16384):
                    f.write(chunk)
    except requests.exceptions.InvalidSchema:
        return (False,"Invalid url schema")
    except requests.exceptions.MissingSchema:
        return (False,"No url provided")
    except requests.exceptions.ReadTimeout:
        return (False,"Timeout")
    except requests.exceptions.ConnectionError:
        return (False,"Connection error")
    except requests.exceptions.TooManyRedirects:
        return (False,"Redirect error")
    except Exception as err:
        print(err.__str__)
        return (False,err.__str__)
    if check_pdf_file(filepath):
        return (True,filepath)

    os.remove(filepath)
    return (False, "Invalid pdf format downloaded")





def worker(id,url,url2,output_dir,allow_overwrite = False):
    """
    Worker that attempts to download a pdf file from url or a backup url

    input:
        id : String with the ID, used for the name of the file
        url : String of the main url
        url2 : String of the backup url if the main url fails
        allow_overwrite : Boolean of you allow want to overwrite files which are already present on disk, defaults to false

    return:
        (id,res,m1,m2) : Tuple of 4 strings, id is the provided ID, res is yes/no, m1,m2 is error messages from url and url2
    """
    filename = output_dir+"/%s.pdf" % id
    res = ("","","")
    if not allow_overwrite and exists(filename):
        res = ("yes","","")
    else:       
        (res,msg) = download_pdf(url,filename)
        #If first attempt fails, try 2nd download link
        if(res == False):
            (res,msg2) = download_pdf(url2,filename)
            if(res == True):
                res = ("yes","","")
            else:
                res = ("no",msg,msg2)
        else:
            res = ("yes","","")   
    (r,m1,m2) = res
    print("Finished %s, did pdf download: %s" %(id,r))
    return (id,r,m1,m2)

def master(num_proceses,data,output_dir):
    """
    Creates and 

    Input:
        num_processes : Int with amount of processes is spawned by the pool
        data : Pandas dataframe containing the filtered data (Column 1 id, column 2 primary url, column 3 backup url)
        output_dir : String path of where to save pdf files + the result excel file
    """

    #Data from excel
    ids = data.iloc[:,0]
    primaryUrls = data.iloc[:,1]
    backupUrls = data.iloc[:,2]

    #Results to be saved
    df = pandas.DataFrame(columns=['ID','Downloaded','Error message download link 1','Error message download link 2'])

    #Pack data
    args = [(ids[i],primaryUrls[i],backupUrls[i],output_dir) for i in range(len(data))]

    with multiprocessing.Pool(processes=num_proceses) as pool:
        ress = [pool.apply_async(worker,args[i]) for i in range(len(data))]
        for i in range(len(ress)):
            (id,res,msg1,msg2) = ress[i].get()
            df.loc[i] = [id,res,msg1,msg2]

    #
    save_excel_data(df,output_dir+'/results.xlsx')


    

def get_file_prompt():
    root = tk.Tk()  
    root.withdraw()
    path = tkinter.filedialog.askopenfilename()
    return path

def get_dir_prompt():
    root = tk.Tk()  
    root.withdraw()
    path = tkinter.filedialog.askdirectory()
    return path

def dialog(num_process):
    print("Hello please select the excel file")
    filepath = get_file_prompt()
    print("Where do you wish to save the files")
    output_dir = get_dir_prompt()
    if filepath == "" or output_dir == "":
        print("Filepath or Output dir not selected, closing down")
        return
    (suc,df) = import_excel_data(filepath)
    if suc == False:
        print("Invalid excel file")
        return
    df = get_urls_from_dataframe(df)
    master(num_process,df,output_dir)


if __name__ == '__main__':
    num_process = 4
    dialog(num_process)

