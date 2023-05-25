import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import subprocess
import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "dsjsdsosdjsddsaasdjadsj"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/separated/htdemucs/<piosenka>/<instrument>.mp3')
def download_file(piosenka, instrument):
    directory = __file__.replace('musplitter/__init__.py', '')+f"separated/htdemucs/{piosenka}/"
    print(directory)
    instrument = f"{instrument}.mp3"
    return send_from_directory(directory, instrument, as_attachment=True)


@app.route('/result')
def show_results():
    file = request.args['file']
    instruments = ['bass', 'drums', 'vocals', 'other']
    return render_template('result.html', instruments=instruments, file=file.replace('.mp3', ''))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            subprocess.run(['demucs', '--mp3', 'uploads/'+filename])
            return redirect(url_for('show_results', file=filename))
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(debug=True)