import cv2
import os
from ultralytics import YOLO
import numpy as np
import uuid
import ctypes


class DynamicArray(object):
    #DYNAMIC ARRAY CLASS (Similar to Python List)

    def __init__(self):
        self.n = 0  # Count actual elements (Default is 0)
        self.capacity = 1  # Default Capacity
        self.A = self.make_array(self.capacity)
    
    def __len__(self):
        #Return number of elements stored in array
        return self.n

    def __getitem__(self, k):
        #Return element at index k
        if not 0 <= k < self.n:
            # Check it k index is in bounds of array
            return IndexError('K is out of bounds !')
        return self.A[k]  # Retrieve from the array at index k

    def append(self, ele):
        #Add element to end of the array
        if self.n == self.capacity:
            # Double capacity if not enough room
            self._resize(2 * self.capacity)

        self.A[self.n] = ele  # Set self.n index to element
        self.n += 1

    def _resize(self, new_cap):
        #Resize internal array to capacity new_cap
        B = self.make_array(new_cap)  # New bigger array
        for k in range(self.n):  # Reference all existing values
            B[k] = self.A[k]
        self.A = B  # Call A the new bigger array
        self.capacity = new_cap  # Reset the capacity

    def make_array(self, new_cap):
        #Returns a new array with new_cap capacity
        return (new_cap * ctypes.py_object)()


def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1

        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1

        # means x is present at mid
        else:
            return mid

    # If we reach here, then the element was not present
    return -1

# load a pretrained YOLOv8n model
model = YOLO("yolov8n.pt", "v8")

# Video's path
vid = 'C:/Users/ADMIN/Desktop/code/python/TTS/testt/sample_trim.mp4'


# Crop path
path = './result/input'
if not os.path.exists(path): #Check if path exists
    os.mkdir(path)
os.chdir(path)
default_path = str(os.getcwd())

fr = 0 #number of frames

c = 0 #count the number of images

k = 0 #count the number of id
maxid = 0
iid = DynamicArray()
ud = DynamicArray()

for result in model.track(source=vid, conf=0.45, save=False, show=False, stream=False):
    frame = result.orig_img
    det = result.boxes
    fr += 1
    print("Frame:", fr)

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
                if id > maxid:
                    maxid = id
                    iid.append(id)
                    ud.append(uuid.uuid4())


                #Save path
                save_path = './' + str(ud[binary_search(iid,id)])
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
print("Done")
cv2.destroyAllWindows()