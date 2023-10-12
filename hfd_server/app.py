import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'Server Works!'


@app.route('/greet')
def say_hello():
    return 'Hello from Server'


@app.route('/api/predict', methods=['POST'])
def predict():
    print('Api Hit')
    try:

        if 'uploadedFiles' not in request.files:
            return 'No File Part'

        uploaded_files = request.files.getlist('uploadedFiles')

        # print(uploaded_files)

        for file in uploaded_files:
            if file.filename == '':
                return 'No Selected File'
            print(file)
            print(file.filename)

            file.save('uploads/' + file.filename)

        subprocess.run(['python', 'Test.py'] + ['uploads/' +
                       file.filename for file in uploaded_files])

        finale = {'total_cnt': 1353, 'non_fraud_cnt': 1253,
                  'fraud_cnt': 100, 'fraud_prcnt': 7.39}

        return jsonify(finale), 200, {"Content-Type": "application/json"}

    except Exception as e:
        return jsonify({"error": str(e)}), 500, {"Content-Type": "application/json"}


if __name__ == '__main__':
    app.run(debug=True)
