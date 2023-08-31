from easyocr import Reader
import cv2
import numpy as np
from ultralytics import YOLO
import time
import threading

# load a pretrained YOLOv8n model
model = YOLO("best.pt", "v8")

# Vals to resize video frames | small frame optimise the run
frame_wid = 640
frame_hyt = 480

vid = 'C:/Users/ADMIN/Desktop/code/python/TTS/testt/trim.mp4'
cap = cv2.VideoCapture(vid)


# Display text function
def txt():
    global detection, frame, bb
    text = ''
    if len(detection) == 0:
        # if the text couldn't be read, show a custom message
        text = "???"
        print(text)
    else:
        i = 0
        while i in range(len(detection)):
            text = text + f"{detection[i][1]} "
            text = text.replace(".",'')
            text = text.replace(",",'')
            text = text.replace(" ",'')
            i+=1
        print(text)

    # Display class name and confidence
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(
        frame,
        text,
        (int(bb[0]), int(bb[1]) - 10),
        font,
        1,
        (0, 0, 255),
        2,
    )


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # resize the frame | small frame optimise the run
    frame = cv2.resize(frame, (frame_wid, frame_hyt))

    # Predict on image
    detect_params = model.predict(source=[frame], conf=0.45, save=False)

    # Convert tensor array to numpy
    DP = detect_params[0].cpu().numpy()
    print(DP)

    if len(DP) != 0:
        for i in range(len(detect_params[0])):
            print(i)
            
            boxes = detect_params[0].boxes
            box = boxes[i]  # returns one box
            conf = box.conf.cpu().numpy()[0]
            bb = box.xyxy.cpu().numpy()[0]

            # border
            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                (0,0,255),
                3,
            )
            
            # OCR
            img = frame[int(bb[1]):int(bb[3]),int(bb[0]):int(bb[2])]

            # grayscale
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (800, 800))

            # threshold on A-channel
            r,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # initialize the reader object
            reader = Reader(['en'])
            # detect the text from the license plate
            detection = reader.readtext(th)

            # recognize and display text
            txt()

    #Display the resulting frame
    cv2.imshow("ObjectDetection", frame)

    # Terminate run when "q" pressed
    if cv2.waitKey(1) == ord("q"):
        break
    time.sleep(0.03)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
