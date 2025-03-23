# Libreries Section
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

os.makedirs('uploads/', exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(f'uploads/{filename}')
        return 'File uploaded successfully'

    return 'No file uploaded'

if __name__ == '__main__':
    app.run()