from flask import Flask, request, jsonify
import os, sys
from werkzeug.utils import secure_filename
import boto3
from datetime import datetime
import random

app = Flask(__name__)

# S3
s3 = boto3.client('s3')
BUCKET_NAME = 'classifai-backend'


@app.route('/')
def index():
    return "ClassifAI"

@app.route("/api/v1.0/classify", methods=['POST'])
def classify():
    image = request.files['file']
    image.save(os.path.join("./uploads", secure_filename(image.filename)))
    
    labels = ["A", "B", "C", "D"]
    values = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
    response = jsonify({
        "statusCode": 200,
        "headers": {},
        "body": {
            "labels": labels, 
            "values": values
        }
    })
    return response

@app.route("/api/v1.0/createDataset", methods=["POST"])
def create_dataset():
    image = request.files['file']
    dataset = request.form.get('dataset')
    label = request.form.get('label')

    timedelta = datetime.now() - datetime(1970, 1, 1)
    name = label + str((timedelta.days * 86400 + timedelta.seconds) * 1000 + timedelta.microseconds // 1000)
    key = "{}/{}/{}".format(dataset, label, name) # Uploads to path [BUCKET]/[DATASET_NAME]/[LABEL]/[LABEL_ID]

    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=image)

    labels = ["A", "B", "C", "D"]
    values = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
    response = jsonify({
        "statusCode": 200,
        "headers": {},
        "body": {
            "message": "Successfully added to S3 Bucket"
        }
    })
    return response

if __name__ == "__main__":
    app.run(debug=True)
