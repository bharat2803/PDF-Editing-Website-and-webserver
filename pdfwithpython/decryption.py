import PyPDF2
from pikepdf import Pdf
from getpass import getpass
import os
#import PDFfilepaths as pdf

#To decrypt PDF
def decryptPDF(filepath,password):
    head,tail = os.path.split(filepath) #tail contains the filename and head contains the rest of the path
    with open(filepath, mode='rb') as file:
        decrypt_file=PyPDF2.PdfFileReader(file)
        if decrypt_file.isEncrypted:
            key=decrypt_file.decrypt(password)
            if key == 0:
                return key
            else:
                with Pdf.open(filepath, password=password) as temp:
                    temp.save(head+"\\decrypted.pdf")
        else:
            return -1
    os.remove(filepath)
    os.rename(head+"\\decrypted.pdf",head+"\\"+tail.rsplit('.',1)[0]+"_decrypted.pdf")
    return 1

if __name__ =="__main__":
    decryptPDF(pdf.fetchpath("Resume.pdf"))
