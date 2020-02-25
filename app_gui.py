""" Module responsible for creation of application pages, navigation between pages
    and display of main application features.

ApplicationGUI is responsible for creation of the GUI for this application, and navigation between GUI subcomponents.
 """

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QStackedLayout, QGridLayout, QLabel, QLineEdit, QSpinBox, QComboBox, \
    QListWidget

from gui_widgets import CameraFeedWidget
from authentication import authenticate_lecturer
from db_interaction import lecturer_module_list, insert_new_lecture, lecture_attendance_list

__author__ = 'Curtis McAllister'
__maintainer__ = 'Curtis McAllister'
__email__ = 'mcallister_c20@ulster.ac.uk'
__status__ = 'Development'

class ApplicationGUI(QWidget):

    # class variables
    __lecturer_id = None
    __module_id = None
    __lecture_id = None
    __module_list = None

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

        # Combobox Widget
        self.cb_module = QComboBox()
        self.cb_module.setStyleSheet('color: white; background-color: grey;')

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
        self.grid_layout_start_page.addWidget(self.cb_module, 1, 2, alignment=QtCore.Qt.AlignLeft)
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
        self.label_module_title = QLabel('')
        self.label_module_title.setStyleSheet('font-size: 20px; color: white')

        # Camera Feed Widget
        self.camera_feed_widget = CameraFeedWidget()

        # TODO: List widget of students marked as present
        self.list_attendance = QListWidget()
        self.list_attendance.setStyleSheet('font-size: 14px; color: white;')

        # Page Layout
        self.camera_feed_page_layout = QGridLayout()
        self.stack_camera_feed_page.setLayout(self.camera_feed_page_layout)
        self.camera_feed_page_layout.addWidget(self.camera_feed_widget, 1, 0)
        self.camera_feed_page_layout.addWidget(self.label_module_title, 0, 1, alignment=QtCore.Qt.AlignTop)
        self.camera_feed_page_layout.addWidget(self.list_attendance, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.camera_feed_page_layout.addWidget(self.button_navigate_main_menu, 2, 1)
        self.setLayout(self.camera_feed_page_layout)

    def login(self):
        """ Log in to the application and navigate to the start page """
        self.set_lecturer_id(authenticate_lecturer(self.entry_email.text(), self.entry_password.text()))
        if authenticate_lecturer(self.entry_email.text(), self.entry_password.text()):
            # clear login page fields
            self.entry_email.setText('')
            self.entry_password.setText('')
            self.label_error_message.setText('')
            # populate combobox from database
            self.set_module_list(lecturer_module_list(self.get_lecturer_id()))
            self.cb_module.addItems(self.get_module_list().values())
            # set module id
            for m_id, title in self.get_module_list().items():
                if title == self.cb_module.currentText():
                    self.set_module_id(m_id)
            # navigate to different page
            self.app_pages.setCurrentIndex(1)
        else:
            self.label_error_message.setText('Email and Password do not match')

    def logout(self):
        self.set_lecture_id(None)
        self.app_pages.setCurrentIndex(0)
        self.cb_module.clear()

    def navigate_to_start_page(self):
        """ Navigates to the Start page. """
        self.list_attendance.clear()
        self.set_lecture_id(None)
        self.app_pages.setCurrentIndex(1)
        self.camera_feed_widget.stop_camera_feed()

    def navigate_to_camera_feed_page(self):
        """ Navigates to the Camera feed page. """
        self.set_lecture_id(insert_new_lecture(self.get_module_id(), self.get_lecturer_id()))
        self.label_module_title.setText(self.cb_module.currentText())
        self.camera_feed_widget.start_camera_feed(self.convert_to_hours(int(self.spin_box_time.value())))
        self.list_attendance.addItems(lecture_attendance_list(self.get_lecture_id()))
        self.app_pages.setCurrentIndex(2)

    def convert_to_hours(self, time):
        converted_time = time * 3600
        return converted_time

    def get_lecturer_id(self):
        return self.__lecturer_id

    def get_module_id(self):
        return self.__module_id

    def get_lecture_id(self):
        return self.__lecture_id

    def get_module_list(self):
        return self.__module_list

    def set_lecturer_id(self, new_l_id):
        self.__lecturer_id = new_l_id

    def set_module_id(self, new_m_id):
        self.__module_id = new_m_id

    def set_lecture_id(self, new_l_id):
        self.__lecture_id = new_l_id

    def set_module_list(self, new_m_list):
        self.__module_list = new_m_list
