# Libreries Section
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

# Variable Section
app = Flask(__name__)

# Check id the folder exist
os.makedirs('uploads/', exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file comes with teh request
    if 'file' in request.files:
        # Catch file
        file = request.files['file']
        # Secure the name of the file
        filename = secure_filename(file.filename)
        # Save the file in the folder that was checked before
        file.save(f'uploads/{filename}')
        return 'File uploaded successfully'

    # Returns if the file has not been uploaded
    return 'No file uploaded'

# call to the program 
if __name__ == '__main__':
    app.run()