import json
from flask import Flask, request, send_from_directory, render_template
import os
import mimetypes
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = None
    if request.method == 'POST':
        file = request.files['file']
        if file and is_audio_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            message = "Upload successfully"
        else:
            message = "Non-audio file detected"
    files = sorted(os.listdir(UPLOAD_FOLDER))
    accept = request.headers.get('Accept', '')
    if 'application/json' in accept:
        return json.dumps({'message': message, 'files': files}).encode('utf-8')
    else:
        return render_template('index.html', files=files, message=message)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


def is_audio_file(filename):
    file_type = None
    if '.' in filename:
        file_type = mimetypes.guess_type(filename)[0]
    return file_type and file_type.startswith('audio')


if __name__ == '__main__':
    app.run(port=8888)
