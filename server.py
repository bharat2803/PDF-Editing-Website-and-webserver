from flask import Flask,render_template,request,redirect,send_from_directory
from werkzeug.utils import secure_filename
from pdfwithpython.encryption import encryptPDF
import os
from file_uploads import clear_uploads
from pdfwithpython.decryption import decryptPDF
from pdfwithpython.pdfmerger import PDFmerger

app = Flask(__name__)
app.secret_key=b"f\\xf1;\\xb3\\xcbG\\xee\\x8a<\\x95\\x9e\\xb4\\x1db\\xabu\\xf5I\\xfe\\xc5\\xde%\\xba\\x80"
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home_page():
    clear_uploads()
    return render_template('test.html')

@app.route('/<string:page_name>',methods=["GET","POST"])
def page(page_name,PDFfile=None,operation=None):
    if request.method == "POST":
        if page_name == "encrypt":
            clear_uploads()
            file=request.files['filename']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            password = request.form["password"]
            status=encryptPDF(filepath,password)
            if status == 0:
                return render_template("downloaded.html",PDFfile=filename.rsplit('.',1)[0]+"_encrypted.pdf",operation="The file is Encrypted Successfully.")
            elif status == 1:
                return render_template("encrypted.html",txt="This file is already Encrypted.")

        if page_name == "decrypt":
            clear_uploads()
            file=request.files['filename']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            password = request.form["password"]
            status=decryptPDF(filepath,password)
            if status == 0:
                return render_template("Wrong_pass.html")
            elif status == -1:
                return render_template("not_encrypted.html")
            return render_template("downloaded.html",PDFfile=filename.rsplit('.',1)[0]+"_decrypted.pdf",operation="The file is Decrypted Successfully.")

        if page_name == "change_pass":
            clear_uploads()
            file = request.files['filename']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"],filename)
            file.save(filepath)
            password = request.form["password"]
            status=decryptPDF(filepath,password)
            if status == 0:
                return render_template("Wrong_pass.html")
            elif status == -1:
                return render_template("not_encrypted.html")
            new_password = request.form["new_password"]
            head,tail = os.path.split(filepath)
            new_filepath = os.path.join(app.config["UPLOAD_FOLDER"],tail.rsplit('.',1)[0]+"_decrypted.pdf")
            status=encryptPDF(new_filepath,new_password)
            head,tail=os.path.split(new_filepath)
            os.rename(head+"\\"+tail.rsplit('.',1)[0]+"_encrypted.pdf",head+"\\"+filename.rsplit('.',1)[0]+"_updated.pdf")
            new_filename=filename.rsplit('.',1)[0]+"_updated.pdf"
            if status == 0:
                return render_template("downloaded.html",PDFfile=new_filename,operation="The Password is Changed Successfully.")
            elif status == 1:
                return render_template("encrypted.html",txt="This file is already Encrypted.")

        if page_name == "merger":
            clear_uploads()
            files = request.files.getlist("filenames")
            filepaths = list()
            flag = 1
            for file in files:
                filename = secure_filename(file.filename)
                if flag == 1:
                    merged_filename = filename.rsplit('.',1)[0]+"_merged.pdf"
                    flag = 0
                filepath = os.path.join(app.config["UPLOAD_FOLDER"],filename)
                filepaths.append(filepath)
                file.save(filepath)
            status=PDFmerger(filepaths)
            if status == 1:
                return render_template("encrypted.html",txt="One or more Files are Encrypted. Kindly decryt them first.")
            elif status == 0:
                return render_template("downloaded.html",PDFfile=merged_filename,operation="The Files are Merged Successfully.")

    return render_template(page_name+".html",PDFfile=None)

app.config["DOWNLOAD_FOLDER"] = "uploads"
@app.route('/download/<string:PDFfile>')
def get_pdf(PDFfile):

    try:
        return send_from_directory(app.config["DOWNLOAD_FOLDER"], PDFfile, as_attachment=True)
    except FileNotFoundError:
        abort(404)
