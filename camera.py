""" Module responsible for providing control of the camera which the system will use. """

import time
import numpy as np
import cv2
from PyQt5 import QtCore

__author__ = "Curtis McAllister"
__maintainer__ = "Curtis McAllister"
__email__ = "mcallister_c20@ulster.ac.uk"
__status__ = "Development"

class Camera(QtCore.QObject):
    """ Creates a Camera object able to be accessed by other objects, and provides controls for the camera. """
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        """ Initialises the Camera object. """
        super().__init__(parent)
        self.camera = None

        # TODO:
        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        """ Starts the camera feed. """
        self.camera = cv2.VideoCapture(0)

        self.timer.start(0, self)

    def stop_recording(self):
        """ Stops the camera feed. """
        self.timer.stop()
        self.camera.release()

    def timerEvent(self, event):
        """ Event run after evert increment of the timer which outputs image data. """
        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)

