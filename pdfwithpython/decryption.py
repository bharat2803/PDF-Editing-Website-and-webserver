import PyPDF2
from pikepdf import Pdf
from getpass import getpass
import os
#import PDFfilepaths as pdf

#To decrypt PDF
def decryptPDF(filepath,password):
    head,tail = os.path.split(filepath) #tail contains the filename and head contains the rest of the path
    tempFilePath = os.path.join(head,"decrypted.pdf")
    with open(filepath, mode='rb') as file:
        decrypt_file=PyPDF2.PdfReader(file)
        if decrypt_file.is_encrypted:
            key=decrypt_file.decrypt(password)
            if key == 0:
                return key
            else:
                with Pdf.open(filepath, password=password) as temp:
                    temp.save(tempFilePath)
        else:
            return -1
    os.remove(filepath)
    decryptedFilename = tail.rsplit('.',1)[0]+"_decrypted.pdf"
    decryptedFilePath = os.path.join(head,decryptedFilename)
    os.rename(tempFilePath,decryptedFilePath)
    return 1

if __name__ =="__main__":
    decryptPDF(pdf.fetchpath("Resume.pdf"))
