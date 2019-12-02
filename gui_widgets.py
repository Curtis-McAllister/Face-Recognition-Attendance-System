""" Module which creates widgets for use within the applications GUI.

 CameraFrameWidget is reponsible for showing frames from a video. CameraFeedWidget displays results
  from CameraFrameWidget and passes data from the camera to CameraFrameWidget.
 """

import numpy as np

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPainter

from camera import Camera

__author__ = "Curtis McAllister"
__maintainer__ = "Curtis McAllister"
__email__ = "mcallister_c20@ulster.ac.uk"
__status__ = "Development"


class CameraFrameWidget(QWidget):
    """ CameraFrameWidget is responsible for returning frames from the camera to the camera feed widget. """
    def __init__(self, parent=None):
        """ Initialises the CameraFrameWidget. """
        super().__init__(parent)
        self.image = QImage()

    # TODO: add face detection method to draw bounding box around detected faces.

    def display_frame(self, image_data):
        """ Displays a frame from the camera.

        Receives image data and adjusts widget size to match it.

        Args:
            image_data: Image data from the camera.
        """

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
        height, width, colour = image.shape
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

    def start_camera_feed(self):
        """ Starts the camera feed. """
        self.camera_feed.start_recording()

    def stop_camera_feed(self):
        """ Stops the camera feed. """
        self.camera_feed.stop_recording()
