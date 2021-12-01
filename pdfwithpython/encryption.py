import PyPDF2
import os

def encryptPDF(filepath,password):
    head,tail=os.path.split(filepath) #tail contains the file name
    with open(filepath, mode='rb') as file:
        file_to_encrypt=PyPDF2.PdfFileReader(file)
        if file_to_encrypt.isEncrypted:
            return 1
        else:
            writer=PyPDF2.PdfFileWriter()
            writer.cloneReaderDocumentRoot(file_to_encrypt)
            writer.encrypt(password)
            with open(head+"\\clone.pdf", mode='wb') as file:
                writer.write(file)
    os.rename(head+"\\clone.pdf",head+"\\"+tail.rsplit('.',1)[0]+"_encrypted.pdf")
    #print(head+"\\"+tail.rsplit('.',1)[0]+"_encrypted.pdf")
    os.remove(filepath)
    return 0

if __name__ == "__main__":
    encryptPDF(pdf.fetchpath("Resume.pdf"))
