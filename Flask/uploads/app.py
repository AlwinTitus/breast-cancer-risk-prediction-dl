from __future__ import division, print_function
import os
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates')

model = load_model(os.path.join(app.root_path, "breastcancer.h5"))
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('bcancer.html')

@app.route('/predict', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file uploaded", 400

    f = request.files['image']

    if f.filename == '':
        return "No selected file", 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
    f.save(file_path)

    img = image.load_img(file_path, target_size=(50, 50))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0 

    preds = model.predict(x)
    confidence = float(preds[0][0])

    if confidence > 0.7:  
        diagnosis = "It is a malignant tumor. Please consult a healthcare professional."
    else:
        diagnosis = "The tumor is benign. No need to worry!"

    text = f"{diagnosis} (Confidence: {confidence:.2f})"
    return text

if __name__ == '__main__':
    app.run(debug=True)
