import profile
import random
from pyexpat import model
from bson import ObjectId
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import numpy as np
import PIL
from PIL import Image
import io
import matplotlib.pyplot as plt
from bson.binary import Binary
import base64
from YOLO_model.net import detect
import cv2
from wordle_log.wordle_logic import get_yg

labels = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", \
              "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", \
              "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", \
              "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", \
              "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", \
              "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", \
              "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", \
              "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", \
              "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", \
              "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]  

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://admin:avyukthisgay@cluster0.afemt.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient('mongodb+srv://admin:avyukthisgay@cluster0.afemt.mongodb.net/?retryWrites=true&w=majority')

db = client.rawImages
col = db.raw

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    try:
        fileStorage = request.files['profile_image']
        fileStorage.save('rawImage.jpg')
    except:
        pass

    im_zero = Image.open("rawImage.jpg")
    im = im_zero.convert('RGB')

    image_bytes = io.BytesIO()
    im.save(image_bytes, format='JPEG')

    image = {
        'data': image_bytes.getvalue()
    }

    image_id = col.insert_one(image).inserted_id
    print(image_id)
    
    image = col.find_one({"_id": ObjectId(image_id)})

    pil_img = Image.open(io.BytesIO(image['data']))

    boxes = detect(pil_img)
    print(boxes)

    det_labels = []
    for box in boxes:
        det_labels.append(labels[box.label])
    # cv2.imwrite('det_img.png', det_img)

    data = io.BytesIO()
    pil_img.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    with open('guessing.txt', 'r') as f:
        guess_num = f.read()
    
    wipe_data = False

    if guess_num == "0":
        new_word = det_labels[random.randint(0, len(det_labels)-1)]
        with open('word.txt', 'w') as f:
            f.write(new_word)

        guess_box = ' '.join(["_" for _ in new_word])

        final_str = [] 

        print(new_word)
    elif guess_num == "1":
        with open('word.txt', 'r') as f:
            word = f.read()
            guess_box = ' '.join(["_" for _ in word])

        for key, val in request.form.items():
            if key == 'guess':
                your_guess = val 
        
        yg = get_yg(word, your_guess)
        print(yg)

        with open('yg.txt', 'a') as f:
            f.write(yg + '\n')
        with open('guesses.txt', 'a') as f:
            f.write(your_guess+ '\n')

        with open('yg.txt', 'r') as f:
            ygs = f.read().split('\n')
        with open('guesses.txt', 'r') as f:
            guesses = f.read().split('\n')

        if your_guess == word:
            wipe_data = True

        final_str = []
        for i in range(len(guesses)):
            final_str.append(f"{' '.join(list(guesses[i]))} - {ygs[i]}")
    
    with open('guessing.txt', 'w') as f:
        f.write("1")

    # if wipe_data:
    #     with open()

    return render_template("pageTwo.html", img_data=encoded_img_data.decode('utf-8'), final_str=final_str, guess_box=guess_box)

if __name__ == '__main__':
    app.run(debug = True)
