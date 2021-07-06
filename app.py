from flask import Flask, request, jsonify
import os, sys
from werkzeug.utils import secure_filename
import boto3
from datetime import datetime
import random
import json

app = Flask(__name__)

# S3
s3 = boto3.client('s3')
sagemaker = boto3.client('sagemaker-runtime')
BUCKET_NAME = 'classifai-backend'


@app.route('/')
def index():
    return "ClassifAI"

@app.route("/api/v1.0/classify", methods=['POST'])
def classify():
    image = request.files['file']
    image.save(os.path.join("./uploads", secure_filename(image.filename)))
    
    custom_attributes = "c000b4f9-df62-4c85-a0bf-7c525f9104a4" 
    endpoint_name = "image-classification-2021-07-06-20-31-59-656"    # Your endpoint name.
    content_type = "application/x-image"                              # The MIME type of the input data in the request body.
    accept = "application/json"                                       # The desired MIME type of the inference in the response.
    payload = None                                                   # Payload for inference.
    with open("./uploads/file.jpg", "rb") as f:
        payload = f.read()
        payload = bytearray(payload)
    response = sagemaker.invoke_endpoint(
        EndpointName=endpoint_name, 
        CustomAttributes=custom_attributes, 
        ContentType=content_type,
        Accept=accept,
        Body=payload
    )

    labels = ["clip", "mouse", "pen"]
    values = json.loads(response['Body'].read().decode())
    results = sorted(zip(labels, values), key=lambda p: -p[1]) # order by value
    response_labels, response_values = zip(*results)

    print(response_labels)
    print(response_values)

    response = jsonify({
        "statusCode": 200,
        "headers": {},
        "body": {
            "labels": response_labels, 
            "values": response_values
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
    key = "public/{}/{}/{}.jpg".format(dataset, label, name) # Uploads to path [BUCKET]/[DATASET_NAME]/[LABEL]/[LABEL_ID]

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
