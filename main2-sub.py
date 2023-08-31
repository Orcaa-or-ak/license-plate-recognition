import cv2
from easyocr import Reader
from ultralytics import YOLO
import numpy as np

# load a pretrained YOLOv8n model
model = YOLO("best.pt", "v8")

# Video's path
vid = 'C:/Users/ADMIN/Desktop/code/python/TTS/testt/trim.mp4'

for result in model.track(source=vid, conf=0.45, save=False, show=False, stream=True):
    frame = result.orig_img
    det = result.boxes

    if len(det) > 0:
        try:
            for i in range(len(det)):
                id = int(det[i].cpu().id)
                xmin = int(det[i].cpu().xyxy[0, 0])
                ymin = int(det[i].cpu().xyxy[0, 1])
                xmax = int(det[i].cpu().xyxy[0, 2])
                ymax = int(det[i].cpu().xyxy[0, 3])

                cv2.rectangle(
                    frame,
                    (xmin, xmax),
                    (ymin, ymax),
                    (0,0,255),
                    3,
                )
                
                # OCR
                img = frame[ymin:ymax,xmin:xmax]
                
                # grayscale
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img, (800, 800))

                # threshold on A-channel
                r,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # initialize the reader object
                reader = Reader(['en'])
                # detect the text from the license plate
                detection = reader.readtext(th)

                if len(detection) == 0:
                    # if the text couldn't be read, show a custom message
                    text = "???"
                    print(text)
                else:
                    i = 0
                    text = ''
                    while i in range(len(detection)):
                        text = text + f"{detection[i][1]} "
                        text = text.replace(".",'')
                        text = text.replace(",",'')
                        text = text.replace(" ",'')
                        i+=1
                    print(text)

                # Display 
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(
                    frame,
                    text,
                    (xmin, ymin - 10),
                    font,
                    1,
                    (0, 0, 255),
                    2,
                )
                

        except: 
            continue

    cv2.imshow("Detect", frame)
    

# When everything done, release the capture
cv2.destroyAllWindows()