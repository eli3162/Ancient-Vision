from flask import *
from subprocess import *
from werkzeug.utils import secure_filename
import os
import json
import subprocess
from pathlib import Path


app = Flask(__name__)

@app.route('/.well-known/acme-challenge/<challenge_key>')
def acme_challenge(challenge_key):
	return challenge_key

@app.route('/artifacts/view/<filename>')
def view(filename):
	return f'''
		<!DOCTYPE html>
		<html lang="en">
		<html>
			<body>
				<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js"></script>
				<model-viewer src="/artifacts/data/{filename}" alt="A 3D model" auto-rotate camera-controls ar ar-modes="webxr scene-viewer quick-look" style="width: 100%; height: 100vh;">
			</body>
		</html>
	'''


@app.route('/artifacts/data/<filename>')
def glb_fetch(filename):
	directory = os.path.join('fll', 'artifacts')
	return send_from_directory(directory, filename, as_attachment=False)

@app.route('/artifacts/metadata/<filename>')
def metadata_fetch(filename):
	root = os.path.dirname(__file__)
	directory = os.path.join(root, 'fll', 'artifacts')
	filepath = os.path.join(directory, filename)
	with open(filepath, "r", encoding="utf-8") as f:
		text = f.read()
	return '''
				<!doctype html>
				<html>
					<head>
						<meta charset="utf-8">
						<title>Iframe Sender</title>
						<meta name="viewport" content="width=device-width,initial-scale=1">
					</head>
					<body>
						<p>{}</p>
						<script>
							const MESSAGE = {};

							function sendPreset() {
								try {
									window.parent.postMessage(MESSAGE, '*');
								} catch (err) {
									console.warn('postMessage failed', err);
								}
							}

							document.addEventListener('DOMContentLoaded', () => {
								sendPreset();
							});

							document.querySelector('.send').addEventListener('click', (e) => {
								document.querySelector('.input').value = '';
									sendPreset();
							});
						</script>
					</body>
				</html>
			'''.format(text, text)

@app.route('/assets/<filename>')
def asset_file(filename):
	directory = 'assets'
	return send_from_directory(directory, filename, as_attachment=False)

@app.route('/fll/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return 'No file selected'
            
            file = request.files['file']
            if file.filename == '':
                return 'No file selected'
            
            if file:
                upload_dir = os.path.join(os.path.dirname(__file__), 'fll', 'artifacts')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_dir, filename)

                file.save(file_path)

                return f'File {filename} uploaded successfully!'
        
        except Exception as e:
            return f'An error occurred: {e}'
    
    return render_template('upload.html')


@app.route('/code/upload', methods=['GET', 'POST'])
def uploadblock():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return 'No file selected'
            
            file = request.files['file']
            if file.filename == '':
                return 'No file selected'
            
            if file:
                upload_dir = os.path.join(os.path.dirname(__file__), 'code', 'block')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_dir, filename)

                file.save(file_path)

                return f'File {filename} uploaded successfully!'
        
        except Exception as e:
            return f'An error occurred: {e}'
    
    return render_template('block.html')

@app.route('/fll/uploads/metadata', methods=['GET', 'POST'])
def handle_json_metadata():
	metadata = request.get_json()
	return

@app.route('/download/assets/<filename>')
def download_assets(filename):
	directory = 'assets'
	return send_from_directory(directory, filename, as_attachment=True)

@app.route('/download/uploads/<filename>')
def download_uploads(filename):
	directory = 'uploads'
	return send_from_directory(directory, filename, as_attachment=True)

@app.route('/assets/uploads/<filename>')
def assets_uploads(filename):
	directory = 'uploads'
	return send_from_directory(directory, filename, as_attachment=False)

@app.route('/music/<filename>')
def music(filename):
	directory = 'music'
	return send_from_directory(directory, filename, as_attachment=False)
    
@app.route('/download/music/<filename>')
def download_music(filename):
	directory = 'music'
	return send_from_directory(directory, filename, as_attachment=True)
    
@app.route('/<file>')
def index(file):
	if file not in ['favicon.ico']:
		try:
			root = os.path.dirname(__file__)
			file_path = os.path.join(root, file)
			with open(file_path, 'r', encoding='utf-8') as file:
				return file.read()
		except Exception as e:
			print(f"Error: {e}")
			return send_from_directory('', file, as_attachment=False)
	else:
		return send_from_directory('', file, as_attachment=False)

@app.route('/')
def home():
	root = os.path.dirname(__file__)
	file_path = os.path.join(root, 'index.html')
	with open(file_path, 'r', encoding='utf-8') as file:
		return file.read()

	
@app.route('/files')
def files():
	root = os.path.dirname(__file__)
	file_path = os.path.join(root, 'files.txt')
	with open(file_path, 'r', encoding='utf-8') as file:
		return file.read()

@app.route('/fll')
def fll():
	root = os.path.join(os.path.dirname(__file__), 'fll')
	file_path = os.path.join(root, 'index.html')
	with open(file_path, 'r', encoding='utf-8') as file:
		return file.read()

@app.route('/fll/<filename>')
def fetch_fll(filename):
	root = os.path.join(os.path.dirname(__file__), 'fll')
	file_path = os.path.join(root, filename)
	with open(file_path, 'r', encoding='utf-8') as file:
		return file.read()




if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
