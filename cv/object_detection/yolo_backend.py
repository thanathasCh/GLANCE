import numpy as np
import cv2 
from common import config


class YOLOv4():
    def __init__(self):
        self.net = cv2.dnn.readNetFromDarknet(config.CONFIG_FILE, config.WEIGHTS_FILE)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.layerNames = self.net.getLayerNames()
        self.ln = [self.layerNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def getBlob(self, image):
        return cv2.dnn.blobFromImage(image, 1/255., config.OBJ_INPUT_SIZE, swapRB=True, crop=False)


    def getLayerOutputs(self, image):
        blob = self.getBlob(image)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.ln)

        return layerOutputs


    def getCoordinates(self, image):
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
                x, y = max(boxes[i][0], 0), max(boxes[i][1], 0)
                w, h = max(boxes[i][2], 0), max(boxes[i][3], 0)
                coords.append([x, y, x+w, y+h])

        return coords

    
    def detect(self, image, isShow=False):        
        coords = self.getCoordinates(image)
        
        for x1, y1, x2, y2 in coords:
            cv2.rectangle(image, (x1, y1), (x2, y2), config.BLUE, 2)

        if isShow:
            cv2.imshow('Detected Image', image)
            cv2.waitKey()


    def detectImg(self, image):
        coords = self.getCoordinates(images)
        products = []

        for x1, y1, x2, y2 in coords:
            products.append(image[x1:x2, y1:y2])

        return products


    def detectImgCoord(self, image):
        resized_img = cv2.resize(image, config.OBJ_INPUT_SIZE)
        coords = self.getCoordinates(resized_img)
        net_h, net_w = config.OBJ_INPUT_SIZE
        org_h, org_w, _ = image.shape
        ratio_h, ratio_w = org_h / net_h, org_w / net_w


        products = []

        for org_x1, org_y1, org_x2, org_y2 in coords:
            x1, y1 = int(org_x1*ratio_w), int(org_y1*ratio_h)
            x2, y2 = int(org_x2*ratio_w), int(org_y2*ratio_h)

            products.append([image[y1:y2, x1:x2], [[x1, y1], [x2, y2]]])
        return products