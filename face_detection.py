""" Module responsible for detection of faces in camera feed """
from os import path

import numpy as np
import cv2

__author__ = "Curtis McAllister"
__maintainer__ = "Curtis McAllister"
__email__ = "mcallister_c20@ulster.ac.uk"
__status__ = "Development"

"""Adapted from: Adrian Rosebrock, Face detection with OpenCV and deep learning, Pyimage search, 26/02/2018
Available at: https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/
Accessed on: 01/12/2019
"""
def detect_faces(image: np.ndarray):
    """ Detects faces in image.

    Loads resnet single shot detection caffe model, and passes it image data to detect faces in. Predictions of
    detected faces are compared against a confidence limit to ensure only the certain predictions are selected,
    the bounding box co-ordinates of these faces are then computed and a list of these co-ordinates are returned.

    Args:
         image: multi-dimensional array of image data

    Returns:
        detected_faces: list containing co-ordinate values of bounding boxes of detected faces
    """
    net = cv2.dnn.readNetFromCaffe(path.realpath("models/deploy.prototxt.txt"),
                                   path.realpath("models/res10_300x300_ssd_iter_140000.caffemodel"))

    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    detected_faces = []

    for i in range(0, detections.shape[2]):
        # extract confidence of face detection prediction
        confidence = detections[0, 0, i, 2]

        # filtering unreliable detections of faces by comparing against confidence limit
        if confidence < 0.75:
            continue

        # determining the coordinates of bounding boxes of detected faces
        box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
        (start_x, start_y, end_x, end_y) = box.astype("int")

        bounding_box_coords = ((start_x, start_y), (end_x, end_y))

        detected_faces.append(bounding_box_coords)

    return detected_faces
