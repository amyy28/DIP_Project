import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
from flask import Flask, render_template
import time

app = Flask(__name__)

@app.route('/')
def index():
    #image = input("Enter the image file name: ")

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'apikey.json'
    client = vision.ImageAnnotatorClient()

    FOLDER_PATH = r'C:\GoogleCloud'
    IMAGE_FILE = 'text.jpg'
    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    docText = response.full_text_annotation.text
    # print(docText)
    return render_template("index.html", value=docText)

time.sleep(30)
if __name__ == "__main__":
    app.run()