""" Module responsible for creation of application pages, navigation between pages
    and display of main application features.

ApplicationGUI is responsible for creation of the GUI for this application, and navigation between GUI subcomponents.
 """

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QStackedLayout, QGridLayout, QLabel, QLineEdit

from gui_widgets import CameraFeedWidget

__author__ = "Curtis McAllister"
__maintainer__ = "Curtis McAllister"
__email__ = "mcallister_c20@ulster.ac.uk"
__status__ = "Development"

class ApplicationGUI(QWidget):
    """Class used to define GUI components of the application, and enable navigation between pages of the GUI."""
    def __init__(self, parent=None):
        """ Initialises GUI page layout """
        super().__init__(parent)

        self.app_pages = QStackedLayout()
        self.stack_start_page = QWidget()
        self.stack_camera_feed_page = QWidget()

        self.start_page_ui()
        self.camera_feed_page_ui()

        self.app_pages.addWidget(self.stack_start_page)
        self.app_pages.addWidget(self.stack_camera_feed_page)

    def start_page_ui(self):
        """ GUI Start page, contains components to set both the time and module the system will run for,
         also contains a button to navigate to the camera feed page."""
        # Page Properties
        self.stack_start_page.setWindowTitle('Start Page')
        self.stack_start_page.setFixedSize(600, 400)
        self.stack_start_page.setStyleSheet("background: #424242")

        # Label Widgets
        self.label_title = QLabel(self.stack_start_page, text='Face Recognition Attendance System')
        self.label_title.setStyleSheet("font-size: 24px; color: white;")
        self.label_title.setGeometry(60, 20, 600, 30)
        self.label_module = QLabel(text='Module:')
        self.label_module.setStyleSheet("font-size: 16px; color: white")
        self.label_timer = QLabel(text='Length of Class (Minutes):')
        self.label_timer.setStyleSheet("font-size: 16px; color: white")

        # Text Entry Widgets
        # TODO: Replace module QLineEdit with dropdown menu of modules connected to database
        self.entry_module = QLineEdit()
        self.entry_module.setStyleSheet("color: white; background-color: grey;")
        self.entry_timer = QLineEdit()
        self.entry_timer.setStyleSheet("color: white; background-color: grey;")

        # Button Widgets
        self.button_navigate_start = QPushButton(text='Start Recording')
        self.button_navigate_start.setStyleSheet("background-color: #003366")

        # Button Widget Signal
        self.button_navigate_start.clicked.connect(self.navigate_to_camera_feed_page)

        # Grid Layout Widget
        self.grid_layout_start_page = QGridLayout()
        self.stack_start_page.setLayout(self.grid_layout_start_page)
        self.grid_layout_start_page.addWidget(self.label_module, 1, 1, alignment=QtCore.Qt.AlignRight)
        self.grid_layout_start_page.addWidget(self.entry_module, 1, 2, alignment=QtCore.Qt.AlignLeft)
        self.grid_layout_start_page.addWidget(self.label_timer, 2, 1, alignment=QtCore.Qt.AlignRight)
        self.grid_layout_start_page.addWidget(self.entry_timer, 2, 2, alignment=QtCore.Qt.AlignLeft)
        self.grid_layout_start_page.addWidget(self.button_navigate_start, 3, 2, alignment=QtCore.Qt.AlignLeft)

    def camera_feed_page_ui(self):
        """ GUI Page which displays the camera feed, module which the attendance is being recorded for,
         and list of students marked as present. Also contains a button to navigate back to the start page. """
        # Page Properties
        self.stack_camera_feed_page.setWindowTitle('Face Detection Page')
        self.stack_camera_feed_page.setFixedSize(900, 600)
        self.stack_camera_feed_page.setStyleSheet("background: #424242")

        # Button Widgets
        self.button_navigate_main_menu = QPushButton(text='Main Menu')
        self.button_navigate_main_menu.setStyleSheet("background-color: #003366")
        self.button_navigate_main_menu.setGeometry(0, 50, 120, 60)

        # Button Widget Signal
        self.button_navigate_main_menu.clicked.connect(self.navigate_to_start_page)

        # Label Widget
        self.label_module_title = QLabel()
        self.label_module_title.setStyleSheet("font-size: 20px; color: white")

        # Camera Feed Widget
        self.camera_feed_widget = CameraFeedWidget()

        # TODO: List widget of students marked as present

        # Page Layout
        self.camera_feed_page_layout = QGridLayout()
        self.stack_camera_feed_page.setLayout(self.camera_feed_page_layout)
        self.camera_feed_page_layout.addWidget(self.camera_feed_widget, 0, 0)
        self.camera_feed_page_layout.addWidget(self.label_module_title, 0, 1, alignment=QtCore.Qt.AlignTop)
        self.camera_feed_page_layout.addWidget(self.button_navigate_main_menu, 2, 1)
        self.setLayout(self.camera_feed_page_layout)

    def navigate_to_start_page(self):
        """ Navigates to the Start page. """
        self.app_pages.setCurrentIndex(0)
        self.camera_feed_widget.hide_camera_feed()

    def navigate_to_camera_feed_page(self):
        """ Navigates to the Camera feed page. """
        self.app_pages.setCurrentIndex(1)
        self.label_module_title.setText(self.entry_module.text())
        self.camera_feed_widget.display_camera_feed()
