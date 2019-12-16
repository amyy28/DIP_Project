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

    def image_segmentation(image_name):
    # reading the image
    image = cv2.imread(image_name)

    # converting the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # threshold to convert the image to pure black and white
    thresh = cv2.threshold(gray, 0,255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]


    # find the contours (continous blob of pixels ) in the image 
    contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Hack for compatibility with different OpenCV versions
    contours = contours[0] if imutils.is_cv2() else contours[1]

    letter_image_regions = []

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