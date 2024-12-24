from flask import Flask,render_template,request,redirect,send_from_directory
from werkzeug.utils import secure_filename
from pdfwithpython.encryption import encryptPDF
import os
from file_uploads import clear_uploads
from pdfwithpython.decryption import decryptPDF
from pdfwithpython.pdfmerger import PDFmerger
import json

app = Flask(__name__)
app.secret_key=b"f\\xf1;\\xb3\\xcbG\\xee\\x8a<\\x95\\x9e\\xb4\\x1db\\xabu\\xf5I\\xfe\\xc5\\xde%\\xba\\x80"
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home_page():
    clear_uploads()
    return render_template('index.html')

@app.route('/get-started')
def getStarted():
    clear_uploads()
    return render_template('get-started.html')

@app.route('/<string:page_name>',methods=["GET","POST"])
def page(page_name,PDFfile=None,operation=None):
    if request.method == "POST":
        file_path = os.path.join(app.instance_path, 'response-params.json')
        with open(file_path, 'r') as f:
            response_params_data = json.load(f)
        if page_name == "encryption":
            clear_uploads()
            file=request.files['filename']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            password = request.form["password"]
            status=encryptPDF(filepath,password)
            if status == 0:
                response_data = response_params_data["encryption"]["success"]
                response_data["file_to_download"] = filename.rsplit('.',1)[0]+"_encrypted.pdf"
            elif status == 1:
                response_data = response_params_data["encryption"]["failure_already_encrypted"]

        if page_name == "decryption":
            clear_uploads()
            file=request.files['filename']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            password = request.form["password"]
            status=decryptPDF(filepath,password)
            if status == 0:
                response_data = response_params_data["decryption"]["failure_incorrect_password"]
            elif status == -1:
                response_data = response_params_data["decryption"]["failure_not_encrypted"]
            else:
                response_data = response_params_data["decryption"]["success"]
                response_data["file_to_download"] = filename.rsplit('.',1)[0]+"_decrypted.pdf"

        if page_name == "password-change":
            clear_uploads()
            file = request.files['filename']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"],filename)
            file.save(filepath)
            password = request.form["password"]
            status=decryptPDF(filepath,password)
            if status == 0:
                response_data = response_params_data["password-change"]["failure_incorrect_password"]
            elif status == -1:
                response_data = response_params_data["password-change"]["failure_not_encrypted"]
            new_password = request.form["new_password"]
            head,tail = os.path.split(filepath)
            new_filepath = os.path.join(app.config["UPLOAD_FOLDER"],tail.rsplit('.',1)[0]+"_decrypted.pdf")
            status=encryptPDF(new_filepath,new_password)
            head,tail=os.path.split(new_filepath)
            encryptedFilename= tail.rsplit('.',1)[0]+"_encrypted.pdf"
            encryptedFilePath = os.path.join(head,encryptedFilename)
            new_filename=filename.rsplit('.',1)[0]+"_updated.pdf"
            new_filepath = os.path.join(head,new_filename)
            os.rename(encryptedFilePath,new_filepath)
            if status == 0:
                response_data = response_params_data["password-change"]["success"]
                response_data["file_to_download"]=new_filename
            elif status == 1:
                response_data = response_params_data["password-change"]["failure_already_encrypted"]

        if page_name == "merge":
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
                response_data = response_params_data["merge"]["failure_already_encrypted"]
            elif status == 0:
                response_data = response_params_data["merge"]["success"]
                response_data["file_to_download"]=merged_filename
        file_to_download = response_data.get("file_to_download",None)
        return render_template("response-view.html",file_to_download=file_to_download,status=response_data["status"],operation=response_data["operation"],txt=response_data["txt"],subtext=response_data["subtext"])

    return render_template(page_name+".html",PDFfile=None)

app.config["DOWNLOAD_FOLDER"] = "uploads"
@app.route('/download/<string:PDFfile>')
def get_pdf(PDFfile):

    try:
        return send_from_directory(app.config["DOWNLOAD_FOLDER"], PDFfile, as_attachment=True)
    except FileNotFoundError:
        abort(404)
