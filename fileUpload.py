import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']
    file1.save(f'./uploads/{file1.filename}')
    file2.save(f'./uploads/{file2.filename}')
    file3.save(f'./uploads/{file3.filename}')
    print(file1)
    print(file2)
    print(file3)
    return "done"

if __name__ == '__main__':  
    app.run(debug=True,host="0.0.0.0",port= 5000 ,use_reloader=False)
