from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from main import main
dirPath = '/home/walkiiiy/Zensplit/back/pics'
inputPath = '/home/walkiiiy/Zensplit/back/pics/input.jpg'

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/uploadPic', methods=['POST'])
def upload_file():
    uploaded_file = request.files['files']
    if uploaded_file.filename != '':
        file_path = inputPath
        uploaded_file.save(file_path)
        return jsonify({'message': 'File has been uploaded successfully'})
    return jsonify({'message': 'No file was uploaded'})


@app.route('/inputPic', methods=['GET'])
def get_input():
    return send_from_directory(dirPath, 'input.jpg')


@app.route('/outputPic', methods=['GET'])
def get_output():
    ordinates = main()
    return send_from_directory(dirPath, 'output.jpg')


if __name__ == '__main__':
    app.run(port=5000)
