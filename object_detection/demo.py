import os
import numpy as np 
import cv2
import config
from yolo_backend import YOLOv4

net = YOLOv4()
cam = cv2.VideoCapture(config.PATH.VIDEO)
writer = None

while True:
    ret, frame = cam.read()

    if not ret:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    frame = cv2.resize(frame, config.INPUT_SIZE)

    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter('output.avi', fourcc, 30, (frame.shape[1], frame.shape[0]), True)
    
    net.detect(frame)
    writer.write(frame)

writer.release()
cam.release()