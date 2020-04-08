import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file2 = request.files['file2']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename.replace("_", " ")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename.replace("_", " ")))
            image1 = UPLOAD_FOLDER + file.filename
            if file2 and allowed_file(file2.filename):
                filename2 = secure_filename(file2.filename)
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2.replace("_", " ")))
                image2 = UPLOAD_FOLDER + file2.filename
                process_file(image1, image2, filename.replace("_", " "))
                return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')


def process_file(image1, image2, filename):
    get_concat_v(image1, image2).save(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))


def get_concat_v(image1, image2):
    btn1 = Image.open(image1)
    btn2 = Image.open(image2)
    dst = Image.new('RGB', (btn1.width, btn1.height + btn2.height))
    dst.paste(btn1, (0, 0))
    dst.paste(btn2, (0, btn1.height))
    return dst


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename.replace("_", " "), as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)