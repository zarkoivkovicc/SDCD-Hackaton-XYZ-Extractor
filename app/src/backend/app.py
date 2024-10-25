from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import zipfile
from pathlib import Path

app = Flask(__name__)
CORS(app)

print(os.getcwd())

UPLOAD_FOLDER = 'app/src/uploads'
PROCESSED_FOLDER = 'app/src/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Mock processing function for PDFs
def process_pdf(file_path):
    # Generate multiple processed files as an example
    processed_files = []
    for i in range(3):  # Simulating multiple output files per input file
        processed_filename = f"processed_{i}_{os.path.basename(file_path)}"
        processed_file_path = os.path.join(PROCESSED_FOLDER, processed_filename)
        with open(file_path, 'rb') as f_in, open(processed_file_path, 'wb') as f_out:
            f_out.write(f_in.read())
        processed_files.append(processed_file_path)
    return processed_files

@app.route('/upload', methods=['POST'])
def upload():
    # # clean_up directories
    # [f.unlink() for f in Path(UPLOAD_FOLDER).glob("*") if f.is_file()]
    # [f.unlink() for f in Path(PROCESSED_FOLDER).glob("*") if f.is_file()]
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    uploaded_files = request.files.getlist('file')  # Get multiple files
    if not uploaded_files:
        return jsonify({'error': 'No files selected'}), 400

    processed_file_urls = []
    
    for file in uploaded_files:
        if file.filename == '':
            return jsonify({'error': 'One of the files has no name'}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Process the file and get a list of processed file paths
        processed_files = process_pdf(file_path)

        # Create URLs for each processed file
        processed_file_urls.extend([
            {
                'url': f"/download/{os.path.basename(processed_file)}",
                'filename': os.path.basename(processed_file)
            }
            for processed_file in processed_files
        ])

    # Return a list of processed file URLs
    return jsonify({'processed_files': processed_file_urls})

# Endpoint to serve processed files
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

@app.route('/download_zip', methods=['GET'])
def download_zip():
    zip_filename = 'processed_files.zip'
    zip_path = os.path.join(PROCESSED_FOLDER, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_STORED) as zip_file:
        for filename in os.listdir(PROCESSED_FOLDER):
            if filename.endswith('.pdf'):  # Adjust this condition to include only PDFs
                file_path = os.path.join(PROCESSED_FOLDER, filename)
                zip_file.write(file_path, os.path.relpath(file_path, PROCESSED_FOLDER))  # Maintain folder structure
                print(f'Added {file_path} to {zip_path}')

    return send_from_directory(PROCESSED_FOLDER, zip_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)
