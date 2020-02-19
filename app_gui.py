""" Module responsible for creation of application pages, navigation between pages
    and display of main application features.

ApplicationGUI is responsible for creation of the GUI for this application, and navigation between GUI subcomponents.
 """

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QStackedLayout, QGridLayout, QLabel, QLineEdit, QSpinBox, QComboBox

from gui_widgets import CameraFeedWidget
from authentication import authenticate_lecturer

__author__ = 'Curtis McAllister'
__maintainer__ = 'Curtis McAllister'
__email__ = 'mcallister_c20@ulster.ac.uk'
__status__ = 'Development'

class ApplicationGUI(QWidget):
    """Class used to define GUI components of the application, and enable navigation between pages of the GUI."""
    def __init__(self, parent=None):
        """ Initialises GUI page layout """
        super().__init__(parent)

        self.app_pages = QStackedLayout()
        self.stack_login_page = QWidget()
        self.stack_start_page = QWidget()
        self.stack_camera_feed_page = QWidget()

        self.login_page_ui()
        self.start_page_ui()
        self.camera_feed_page_ui()

        self.app_pages.addWidget(self.stack_login_page)
        self.app_pages.addWidget(self.stack_start_page)
        self.app_pages.addWidget(self.stack_camera_feed_page)

    def login_page_ui(self):
        # Page Properties
        self.stack_login_page.setWindowTitle('Login Page')
        self.stack_login_page.setFixedSize(600, 400)
        self.stack_login_page.setStyleSheet('background: #424242')

        # Label Widgets
        self.label_login_title = QLabel(self.stack_login_page, text='Login Page')
        self.label_login_title.setStyleSheet('font-size: 24px; color: white;')
        self.label_login_title.setGeometry(270, 20, 600, 30)
        self.label_email = QLabel(text='Email:')
        self.label_email.setStyleSheet('font-size: 16px; color: white')
        self.label_password = QLabel(text='Password:')
        self.label_password.setStyleSheet('font-size: 16px; color: white')
        self.label_error_message = QLabel(text='')
        self.label_error_message.setStyleSheet('font-size: 16px; color: red;')

        # Text Entry Widgets
        self.entry_email = QLineEdit()
        self.entry_email.setStyleSheet('color: white; background-color: grey;')
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        self.entry_password.setStyleSheet('color: white; background-color: grey;')

        # Button Widgets
        self.button_login = QPushButton(text='Login')
        self.button_login.setStyleSheet('color: white; background-color: #003366')

        # Button Widget Signal
        self.button_login.clicked.connect(self.login)

        # Grid Layout Widget
        self.grid_layout_login_page = QGridLayout()
        self.stack_login_page.setLayout(self.grid_layout_login_page)
        self.grid_layout_login_page.addWidget(self.label_email, 1, 1, alignment=QtCore.Qt.AlignRight)
        self.grid_layout_login_page.addWidget(self.entry_email, 1, 2, alignment=QtCore.Qt.AlignLeft)
        self.grid_layout_login_page.addWidget(self.label_password, 2, 1, alignment=QtCore.Qt.AlignRight)
        self.grid_layout_login_page.addWidget(self.entry_password, 2, 2, alignment=QtCore.Qt.AlignLeft)
        self.grid_layout_login_page.addWidget(self.label_error_message, 3, 1, alignment=QtCore.Qt.AlignRight)
        self.grid_layout_login_page.addWidget(self.button_login, 3, 2, alignment=QtCore.Qt.AlignLeft)

    def start_page_ui(self):
        """ GUI Start page, contains components to set both the time and module the system will run for,
         also contains a button to navigate to the camera feed page."""
        # Page Properties
        self.stack_start_page.setWindowTitle('Start Page')
        self.stack_start_page.setFixedSize(600, 400)
        self.stack_start_page.setStyleSheet('background: #424242')

        # Label Widgets
        self.label_title = QLabel(self.stack_start_page, text='Face Recognition Attendance System')
        self.label_title.setStyleSheet('font-size: 24px; color: white;')
        self.label_title.setGeometry(60, 20, 600, 30)
        self.label_module = QLabel(text='Module:')
        self.label_module.setStyleSheet('font-size: 16px; color: white')
        self.label_timer = QLabel(text='Length of Class (Hours):')
        self.label_timer.setStyleSheet('font-size: 16px; color: white')

        # Text Entry Widget
        # TODO: Replace module QLineEdit with dropdown menu of modules connected to database
        self.entry_module = QComboBox()
        self.entry_module.setStyleSheet('color: white; background-color: grey;')

        # Spin Box Widget
        self.spin_box_time = QSpinBox()
        self.spin_box_time.setMinimum(1)
        self.spin_box_time.setMaximum(24)
        self.spin_box_time.setStyleSheet('color: white; background-color: grey')

        # Button Widgets
        self.button_logout = QPushButton(text='Logout')
        self.button_logout.setStyleSheet('color: white; background-color: #003366')
        self.button_navigate_start = QPushButton(text='Start Recording')
        self.button_navigate_start.setStyleSheet('color: white; background-color: #003366')

        # Button Widget Signal
        self.button_logout.clicked.connect(self.logout)
        self.button_navigate_start.clicked.connect(self.navigate_to_camera_feed_page)

        # Grid Layout Widget
        self.grid_layout_start_page = QGridLayout()
        self.stack_start_page.setLayout(self.grid_layout_start_page)
        self.grid_layout_start_page.addWidget(self.label_module, 1, 1, alignment=QtCore.Qt.AlignRight)
        self.grid_layout_start_page.addWidget(self.entry_module, 1, 2, alignment=QtCore.Qt.AlignLeft)
        self.grid_layout_start_page.addWidget(self.label_timer, 2, 1, alignment=QtCore.Qt.AlignRight)
        self.grid_layout_start_page.addWidget(self.spin_box_time, 2, 2, alignment=QtCore.Qt.AlignLeft)
        self.grid_layout_start_page.addWidget(self.button_logout, 3, 1, alignment=QtCore.Qt.AlignRight)
        self.grid_layout_start_page.addWidget(self.button_navigate_start, 3, 2, alignment=QtCore.Qt.AlignLeft)

    def camera_feed_page_ui(self):
        """ GUI Page which displays the camera feed, module which the attendance is being recorded for,
         and list of students marked as present. Also contains a button to navigate back to the start page. """
        # Page Properties
        self.stack_camera_feed_page.setWindowTitle('Face Detection Page')
        self.stack_camera_feed_page.setFixedSize(1000, 600)
        self.stack_camera_feed_page.setStyleSheet('background: #424242')

        # Button Widgets
        self.button_navigate_main_menu = QPushButton(text='Cancel and return to Start Page')
        self.button_navigate_main_menu.setStyleSheet('color: white; background-color: #003366')
        self.button_navigate_main_menu.setGeometry(0, 50, 120, 60)

        # Button Widget Signal
        self.button_navigate_main_menu.clicked.connect(self.navigate_to_start_page)

        # Label Widget
        self.label_module_title = QLabel()
        self.label_module_title.setStyleSheet('font-size: 20px; color: white')

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

    def login(self):
        """ Log in to the application and navigate to the start page """
        if authenticate_lecturer(self.entry_email.text(), self.entry_password.text()):
            # TODO: set variable for lecturer_id field
            self.entry_email.setText('')
            self.entry_password.setText('')
            self.label_error_message.setText('')
            self.app_pages.setCurrentIndex(1)
        else:
            self.label_error_message.setText('Email and Password do not match')

    def logout(self):
        # TODO: reset lecturer_id
        self.app_pages.setCurrentIndex(0)

    def navigate_to_start_page(self):
        """ Navigates to the Start page. """
        self.app_pages.setCurrentIndex(1)
        self.camera_feed_widget.stop_camera_feed()

    def navigate_to_camera_feed_page(self):
        """ Navigates to the Camera feed page. """
        self.app_pages.setCurrentIndex(2)
        self.label_module_title.setText(self.entry_module.text())
        self.camera_feed_widget.start_camera_feed(self.convert_to_hours(int(self.spin_box_time.value())))

    def convert_to_hours(self, time):
        converted_time = time * 3600
        return converted_time
