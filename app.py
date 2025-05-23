from flask import Flask, request, render_template, jsonify
from process import process_document
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    file = request.files['file']
    lang = request.form.get('lang', 'en')
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    summary = process_document(path, target_language=lang)
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
