# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 20:47:31 2021

@author: SreeKeerthiGudipatiR
"""

import cv2
import numpy as np
import glob
import random
from flask import Flask, render_template

app=Flask(__name__)

x=10
num=0
net = cv2.dnn.readNet("yolov3_training_last.weights", "yolov3_testing.cfg")
# Name custom object
classes = ["apple"]
labe="Apple"

# Images path
images_path = glob.glob(r"C:\Users\SreeKeerthiGudipatiR\Downloads\1_iot\testt\*.jpg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
random.shuffle(images_path)

def detection():
    x=5
    count=0
    img_path=images_path[5]
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                print(class_id)
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    print(class_ids)        
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(indexes)
    #print("+++++++++++")
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            print(label)
            if(label=="apple"):
                count=count+1
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)
    
    #print("^^^^^^^^^^^^^")
    print(count)
    cv2.imshow("Image", img)
    key = cv2.waitKey(0)
    summ=count
    return count
    #cv2.destroyAllWindows()
    

@app.route("/home")
@app.route("/")

def home():
    summ= detection()
    link="https://www.bigbasket.com/ps/?q="+labe
    return render_template("check.html", data=summ, name= labe, link=link)


if __name__=="__main__":
    app.run(debug=True)