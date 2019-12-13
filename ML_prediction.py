# importing dependencies
import numpy as np
import keras
import os
import cv2
import imutils
import os.path
import importlib
from os import listdir
from keras import backend as k
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

y_train = []
# to get the name of the folder
for name_folder in os.listdir("extracted_letter_images") :
    name = 'extracted_letter_images/' + name_folder
    for f in listdir(name):
        # name of the folder is the name of the output
        y_train.append(np.asarray(name_folder))
y_train = np.asarray(y_train)
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(y_train)


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

    # now loop through each of the letter in the image 
    for contour in contours:
        # get the rectangle that contains the contour
        x,y,w,h = cv2.boundingRect(contour)
        # compare the width and height of the contour to detect if it
        # has one letter or not
        if w/h >1.25:
            # this is too wide for a single letter
            continue
        elif w<3 or h<3:
            # this is a very small image probably a noise
            continue
        else:
        # this is a normal letter by itself
            letter_image_regions.append((x,y,w,h))

    return letter_image_regions

    # loading the trained model
model = load_model('models/model.h5')

# a function to resize the image into appropriate dimensions
def resize(img):
    img = cv2.resize(img,(20,20))
    return img

# now we will read images from the folder segment the images and will produce the output
for image_name in listdir('images'):
    counter = 1
    # constructing the name of the file 
    file_name = 'images/' + image_name

    # getting segmented images 
    letters_in_image = image_segmentation(file_name)
    
    # sorting the letters so that letters that appear before is addressed first 
    letters_in_image = sorted(letters_in_image, key=lambda x: x[0])
    
    ans = ""
    for (x,y,w,h) in letters_in_image:
        image = cv2.imread(file_name,0)
        letter = image[y - 2:y + h + 2, x - 2:x + w + 2]
        
        cv2.imwrite(str(counter)+'.jpg', letter)
        counter = counter + 1
        
        letter  = resize(letter)/255
        X_test = np.asarray(letter)
        X_test = np.reshape(X_test, [-1,20,20,1])
        output = np.argmax(model.predict(X_test, verbose = 0))
        output = label_encoder.inverse_transform(output)
        ans +=output
    print("image no: ", ans)