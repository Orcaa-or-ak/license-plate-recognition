# Load YOLOv8n-cls, train it on mnist160 for 3 epochs and predict an image with it
from ultralytics import YOLO

model = YOLO('yolov8n-cls.pt')  # load a pretrained YOLOv8n classification model
model.train(data='C:/Users/ADMIN/Desktop/code/python/TTS/testt/datasets/animals', epochs=100)  # train the model
model('inference/images/img0.JPG')  # predict on an image