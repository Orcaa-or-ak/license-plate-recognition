import cv2
import os
from ultralytics import YOLO
import numpy as np
import uuid
import ctypes

# load a pretrained YOLOv8n model
model = YOLO("best.pt", "v8")

inp_path = os.getcwd() + "/result/vehicle"

save_path = os.getcwd() + "/result/plate"
if not os.path.exists(save_path): #Check if path exists
    os.mkdir(save_path)

#check if folder exists
if os.path.exists(inp_path) and os.path.isdir(inp_path):
    os.chdir(inp_path)
    folders = [item for item in os.listdir(inp_path) if os.path.isdir(os.path.join(inp_path, item))]
    
    if folders: #if folder exists
        for folder_name in folders:
            print("Current folder:", folder_name)
            folder_path = os.getcwd() + '/' + folder_name
            os.chdir(folder_path)
            present_path = os.getcwd()

            files = [item for item in os.listdir(present_path) if os.path.isfile(os.path.join(present_path, item))]
            if files:
                for file_name in files:
                    #start detecting
                    for result in model.track(source=file_name, conf=0.45, save=False, show=False, stream=False):
                        frame = result.orig_img
                        det = result.boxes

                        if len(det) > 0:
                            try:
                                for i in range(len(det)):

                                    xmin = int(det[i].cpu().xyxy[0, 0])
                                    ymin = int(det[i].cpu().xyxy[0, 1])
                                    xmax = int(det[i].cpu().xyxy[0, 2])
                                    ymax = int(det[i].cpu().xyxy[0, 3])


                                    #Save
                                    temp_save = save_path +'/'+ folder_name
                                    if not os.path.exists(temp_save): #Check if folder exists
                                        os.mkdir(temp_save)
                                    os.chdir(temp_save)

                                    #Crop
                                    cropframe = frame[ymin:ymax,xmin:xmax] #Start y : end y, start x : end x
                                    cv2.imwrite(file_name,cropframe)
                                    os.chdir(folder_path)
                    

                            except Exception as e: 
                                print(e)
                                continue

            else:
                print("No files found in this folder.")
            
            print()
            os.chdir(inp_path)                 
    else:
        print("No folders found.")
else:
    print("The directory does not exist.")

print("Done")