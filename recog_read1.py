from easyocr import Reader
import cv2


# Load image, convert to grayscale, and find edges
image = cv2.imread('trimm.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

# Find contour and sort by contour area
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

# Find bounding box and extract ROI
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    img = gray[y:y+h, x:x+w]
    break

#---------------------------------------------------------------------
img = cv2.resize(img, (500, 500))

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
    while i in range(len(detection)):
        text = f"{detection[i][1]} {detection[i][2] * 100:.2f}%"
        print(text)
        i+=1

cv2.imshow("img",th)
cv2.waitKey(0)
cv2.destroyAllWindows()