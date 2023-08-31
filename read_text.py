from easyocr import Reader
import cv2

# load the image and resize it
imgg = 'C:/Users/ADMIN/Desktop/code/python/TTS/testt/trimm.jpg'
img = cv2.imread(imgg, cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (800, 800))

# threshold on A-channel
r,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# initialize the reader object
reader = Reader(['en'])
# detect the text from the license plate
detection = reader.readtext(th)

if len(detection) == 0:
    # if the text couldn't be read, show a custom message
    text = "Impossible to read the text from the license plate"
    print(text)
else:
    i = 0
    text = ''
    while i in range(len(detection)):
        text = text + f"{detection[i][1]}"
        i+=1
    print(text)

cv2.imshow("img",th)
cv2.waitKey(0)
cv2.destroyAllWindows()