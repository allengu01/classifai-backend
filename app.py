from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)

@app.route('/')
def index():
    return "ClassifAI"

@app.route("/api/v1.0/classify", methods=['POST'])
def classify():
    image = request.files['file']
    image.save(os.path.join("./uploads", secure_filename(image.filename)))
    
    #TENSORFLOW BACK END STUFF HERE
    labels = ["A", "B", "C", "D"]
    values = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
    
    return jsonify({"labels": labels, "values": values})

if __name__ == "__main__":
    app.run(debug=True)
