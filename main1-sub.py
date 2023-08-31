import cv2
import os
from ultralytics import YOLO
import numpy as np
import uuid

# load a pretrained YOLOv8n model
model = YOLO("best.pt", "v8")

# Video's path
vid = 'C:/Users/ADMIN/Desktop/code/python/TTS/testt/trim.mp4'

# Crop path
path = './crop'
if not os.path.exists(path): #Check if path exists
    os.mkdir(path)
os.chdir(path)
default_path = str(os.getcwd())

c = 0
ud = [''] * 100
for result in model.track(source=vid, conf=0.45, save=False, show=False, stream=False):
    frame = result.orig_img
    det = result.boxes

    if len(det) > 0:
        try:
            for i in range(len(det)):
                os.chdir(default_path)

                id = int(det[i].cpu().id)
                xmin = int(det[i].cpu().xyxy[0, 0])
                ymin = int(det[i].cpu().xyxy[0, 1])
                xmax = int(det[i].cpu().xyxy[0, 2])
                ymax = int(det[i].cpu().xyxy[0, 3])

                #check if the plate has uuid before
                if ud[id] == '':
                    ud[id] = uuid.uuid4()

                #Save path
                save_path = './' + str(ud[id])
                if not os.path.exists(save_path): #Check if folder exists
                    os.mkdir(save_path)
                os.chdir(save_path)

                #Crop
                c = c + 1
                cropframe = frame[ymin:ymax,xmin:xmax] #Start y : end y, start x : end x
                savestr = str(c) + ".jpg"
                cv2.imwrite(savestr,cropframe)

        except Exception as e: 
            print(e)
            continue

# When everything done, release the capture
cv2.destroyAllWindows()