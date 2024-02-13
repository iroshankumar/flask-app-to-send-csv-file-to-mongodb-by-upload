from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
import csv

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['csv_data2']
collection = db['csv_collection']

def save_uploaded_file(file):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return file.filename

def parse_csv(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

def save_to_mongodb(data):
    collection.insert_many(data)

@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = save_uploaded_file(file)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            data = parse_csv(file_path)
            save_to_mongodb(data)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload_csv.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'The file {filename} has been uploaded successfully.'

if __name__ == '__main__':
    app.run(debug=True)
