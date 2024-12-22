import PyPDF2
import os

def encryptPDF(filepath,password):
    head,tail=os.path.split(filepath) #tail contains the file name
    cloneFilePath = os.path.join(head,"clone.pdf")
    with open(filepath, mode='rb') as file:
        file_to_encrypt=PyPDF2.PdfReader(file)
        if file_to_encrypt.is_encrypted:
            return 1
        else:
            writer=PyPDF2.PdfWriter()
            for page in file_to_encrypt.pages:  # Changed from 'clone_reader_document_root'
                writer.add_page(page)
            writer.encrypt(password)
            with open(cloneFilePath, mode='wb') as file:
                writer.write(file)
    encryptedFilename = tail.rsplit('.',1)[0]+"_encrypted.pdf"
    encryptedFilePath = os.path.join(head,encryptedFilename)
    os.rename(cloneFilePath,encryptedFilePath)
    os.remove(filepath)
    return 0

if __name__ == "__main__":
    encryptPDF(pdf.fetchpath("Resume.pdf"))
