import json

from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/audio', methods=['POST'])
def process_audio():
    data = request.get_data()
    data_length = request.content_length

    if data_length > 1024 * 1024 * 10:
        return 'File too large!', 400

    # process data here:
    print("Processing data: ", data)

    return json.dumps({"text": "Audio successfully processed!"}), 200
