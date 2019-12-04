""" Module which creates widgets for use within the applications GUI.

 CameraFrameWidget is reponsible for showing frames from a video. CameraFeedWidget displays results
 from CameraFrameWidget and passes data from the camera to CameraFrameWidget.
 """

import numpy as np
import cv2

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPainter

from face_detection import detect_faces
from camera import Camera

__author__ = 'Curtis McAllister'
__maintainer__ = 'Curtis McAllister'
__email__ = 'mcallister_c20@ulster.ac.uk'
__status__ = 'Development'


class CameraFrameWidget(QWidget):
    """ CameraFrameWidget is responsible for returning frames from the camera to the camera feed widget. """
    def __init__(self, parent=None):
        """ Initialises the CameraFrameWidget. """
        super().__init__(parent)
        self.image = QImage()
        self.__bounding_box_colour = (0, 255, 0)
        self.__bounding_box_thickness = 3

    def display_frame(self, image_data):
        """ Paints a bounding box around detected faces in the camera feed and displays this frame.

        Receives image data, passes it to face_detection model then uses the returned results to paint a bounding box
        around detected faces. Then adjusts the widget size to match the size of the image.

        Args:
            image_data: Image data from the camera.
        """
        detected_faces = detect_faces(image_data)

        for (bounding_box_start, bounding_box_end) in detected_faces:
            cv2.rectangle(image_data,
                          bounding_box_start,
                          bounding_box_end,
                          self.__bounding_box_colour,
                          self.__bounding_box_thickness)

        self.image = self.get_frame(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def get_frame(self, image: np.ndarray):
        """ Processes camera image data and returns it.

         Determines height and width of image array, stores image array as a QImage
         and converts the rgb values of the image.

         Args:
            image: multidimensional array of image data received from the camera.

         Returns:
            feed_image: processed image data.

         """
        height, width = image.shape[:2]
        bytes_per_line = 3 * width
        feed_image = QImage

        feed_image = feed_image(image.data,
                                width,
                                height,
                                bytes_per_line,
                                QImage.Format_RGB888)

        feed_image = feed_image.rgbSwapped()
        return feed_image

    def paintEvent(self, event):
        """ Event called to redisplay frames of the video """
        frame_painter = QPainter(self)
        frame_painter.drawImage(0, 0, self.image)
        self.image = QImage()


class CameraFeedWidget(QWidget):
    """ Displays the camera feed for use in camera feed gui component, initialises the camera
     and passes camera feed to CameraFrameWidget. """
    def __init__(self, parent=None):
        """ Initialises the Camera feed widget. """
        super().__init__(parent)
        self.video_frame_widget = CameraFrameWidget()

        self.camera_feed = Camera()

        self.video_frame_data_slot = self.video_frame_widget.display_frame
        self.camera_feed.image_data.connect(self.video_frame_data_slot)

        self.camera_feed_widget_layout = QVBoxLayout()
        self.camera_feed_widget_layout.addWidget(self.video_frame_widget)
        self.setLayout(self.camera_feed_widget_layout)

    def start_camera_feed(self, time):
        """ Starts the camera feed. """
        self.camera_feed.start_recording(time)

    def stop_camera_feed(self):
        """ Stops the camera feed. """
        self.camera_feed.stop_recording()
