import json
import os
import pyrebase

from flask import Flask
from flask import request
from flask_cors import CORS

firebaseConfig = {
    "apiKey": "AIzaSyA7_Vtd1KtxTNsVphWKB6MmU1uOrR1LPU8",
    "authDomain": "eyephone-51d80.firebaseapp.com",
    "projectId": "eyephone-51d80",
    "storageBucket": "eyephone-51d80.appspot.com",
    "messagingSenderId": "745363148986",
    "appId": "1:745363148986:web:286daba9bf395f0f3f7283",
    "measurementId": "G-3GXCPPEFC8",
    "databaseURL": "gs://eyephone-51d80.appspot.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)

# define storage
storage = firebase.storage()
app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/metrics/', methods=['POST'])
def process_audio():
    FILE_OUTPUT = 'output.avi'

    data = request.get_data()
    data_length = request.content_length

    if data_length > 1024 * 1024 * 10:
        return 'File too large!', 400

    # process data here:
    print("Processing data: ", data)

    # Checks and deletes the output file
    # You cant have a existing file or it will through an error
    if os.path.isfile(FILE_OUTPUT):
        os.remove(FILE_OUTPUT)

    # opens the file 'output.avi' which is accessible as 'out_file'
    with open(FILE_OUTPUT, "wb") as out_file:  # open for [w]riting as [b]inary
        out_file.write(data)

    storage.child("output.avi").put("output.avi")

    return json.dumps({"diameter": 50, "constriction_velocity": 30}), 200
