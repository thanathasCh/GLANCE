import numpy as np
import cv2 
import config

class YOLOv4():
    def __init__(self):
        self.net = cv2.dnn.readNetFromDarknet(config.CONFIG_FILE, config.WEIGHTS_FILE)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.layerNames = self.net.getLayerNames()
        self.ln = [self.layerNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def getBlob(self, image):
        if type(image) is str:
            image = cv2.imread(image)
        
        blob = cv2.dnn.blobFromImage(image, 1/255., config.INPUT_SIZE, swapRB=True, crop=False)
        
        return blob


    def getLayerOutputs(self, image):
        if type(image) is str:
            image = cv2.imread(image)

        blob = self.getBlob(image)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.ln)

        return layerOutputs


    def getCoordinates(self, image):
        if type(image) is str:
            image = cv2.imread(image)

        boxes = []
        confidence = []
        W, H, _ = image.shape

        layerOutput = self.getLayerOutputs(image)

        for output in layerOutput:
            for detection in output:
                conf = detection[5]

                if conf > config.CONFIDENCE:
                    box = detection[0:4] * np.array([W, H, W, H])
                    centerX, centerY, width, height = box.astype('int')

                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidence.append(float(conf))

        idx = cv2.dnn.NMSBoxes(boxes, confidence, config.CONFIDENCE, config.THRESH)

        coords = []

        if len(idx) > 0:
            for i in idx.flatten():
                x, y = boxes[i][0], boxes[i][1]
                w, h = boxes[i][2], boxes[i][3]
                coords.append([x, y, x+w, y+h])

        return coords

    
    def detect(self, image, isShow=False):
        if type(image) is str:
            image = cv2.imread(image)

        coords = self.getCoordinates(image)
        
        for x1, y1, x2, y2 in coords:
            cv2.rectangle(image, (x1, y1), (x2, y2), config.COLOR, 2)

        if isShow:
            cv2.imshow('Detected Image', image)
            cv2.waitKey()