import cv2
import numpy as np
import glob
import random
import os
from twilio.rest import Client

# Load Yolo

account_sid = 'xxxxxxxxxxxxxxxxxxx'
auth_token = 'xxxxxxxxxxxxxx'
client = Client(account_sid, auth_token)

net = cv2.dnn.readNet("yolov3_training_last.weights", "yolov3_testing.cfg")

# Name custom object
classes = ["apple"]

# Images path
images_path = glob.glob(r"C:\Users\SreeKeerthiGudipatiR\Downloads\1_iot\testt\*.jpg")

'''for i in images_path:
    img=cv2.imread(i)
    cv2.imshow('apple',img)'''
    
    

layer_names = net.getLayerNames()
#print("111111111")
#print(layer_names)
#print("111111111")

output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
print(output_layers)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Insert here the path of your images
random.shuffle(images_path)
# loop through all the images
for img_path in images_path:
    # Loading image
    count=0
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    #cv2.imshow('img',img)
    height, width, channels = img.shape
    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    #print(blob)
    net.setInput(blob)
    outs = net.forward(output_layers)
    #print(len(outs))
    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    num=1
    for out in outs:
        for detection in out:
            scores = detection[5:]
            #print(detection)
            #print("33333333333")
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                #print(class_id)
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
    #print(class_ids)        
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            ''' print("****")
            print(x)
            print(y)
            print(x+w)
            print(y+h)
            print("*******")'''
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            print(label)
            if(label=="apple"):
                count=count+1
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)
    
    print(count)
    if(count==1):
        message = client.messages \
         .create(
         body='There is one apple in fridge',
         from_='11111111111111',
         to='+1111111111'
         )
        print("message sent")
     
    
    print("_________________________________________________")
    cv2.imshow("Image", img)
    key = cv2.waitKey(0)

cv2.destroyAllWindows()
