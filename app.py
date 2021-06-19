from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return "ClassifAI"

@app.route("/api/v1.0/classify", methods=['POST'])
def classify():
    image = request.files['file']
    image.save(os.path.join("./uploads", secure_filename(image.filename)))
    return jsonify({"label": "A", "value": 1 })

if __name__ == "__main__":
    app.run(debug=True)
