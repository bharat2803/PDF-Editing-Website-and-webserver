import PyPDF2
import os

# This program merges 2 or more PDFs

def PDFmerger(filepaths):

    totalpdfs = len(filepaths)
    merger = PyPDF2.PdfFileMerger()
    fname = filepaths[0].split('.')[0]
    for i in range(totalpdfs):
        with open(filepaths[i],mode="rb") as file:
            if PyPDF2.PdfFileReader(file).isEncrypted:
                return 1  #Checking if the file is encrypted or not.
                #print(f"{os.path.split(filepaths[i])[1]} is encrypted.\n")
                #decryption.decryption(filepaths[i]) #To create its clone named temp.pdf.
                #merger.append("temp.pdf")
            else:
                merger.append(filepaths[i])

    #decryption.blank_temp() #To delete all the data from temp.
    merger.write(f"{fname}_merged.pdf")
    #print("\n \nAll files are merged.")
    #os.startfile(f"{fname}(1).pdf")
    return 0


if __name__ == "__main__":
    PDFmerger(["Resume.pdf","cloned.pdf"])
