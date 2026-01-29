import cv2
import os
import numpy as np

def train_model():
    faces = []
    labels = []
    label = 0

    for user in os.listdir("dataset"):
        for img in os.listdir(f"dataset/{user}"):
            faces.append(cv2.imread(f"dataset/{user}/{img}", 0))
            labels.append(label)
        label += 1

    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(faces, np.array(labels))
    model.save("model/face_model.yml")
