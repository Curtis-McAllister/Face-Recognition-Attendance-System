import sys
import unittest
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

import start_app

app = QApplication(sys.argv)

class App_Unit_Test(unittest.TestCase):
    def setUp(self):
        self.form = start_app.Application()

    def test_defaults_login_page(self):
        self.assertEqual(self.form.label_login_title.text(), 'Login Page')
        self.assertEqual(self.form.label_email.text(), 'Email:')
        self.assertEqual(self.form.label_password.text(), 'Password:')
        self.assertEqual(self.form.entry_email.text(), '')
        self.assertEqual(self.form.entry_password.text(), '')

    def test_defaults_setup_page(self):
        self.assertEqual(self.form.label_title.text(), 'Face Recognition Attendance System')
        self.assertEqual(self.form.label_module.text(), 'Module:')
        self.assertEqual(self.form.label_timer.text(), 'Length of Class (Hours):')
        # Module combo box empty
        self.assertEqual(self.form.cb_module.currentIndex(), -1)
        self.assertEqual(self.form.spin_box_time.value(), 1)

    def test_defaults_camera_page(self):
        self.assertEqual(self.form.label_title.text(), 'Face Recognition Attendance System')
        self.assertEqual(self.form.label_module.text(), 'Module:')
        self.assertEqual(self.form.label_timer.text(), 'Length of Class (Hours):')
        # Module combo box empty
        self.assertEqual(self.form.list_attendance.count(), 0)


    def test_invalid_login(self):
        self.form.entry_email.setText('roberta@university.ac.uk')
        self.form.entry_password.setText('incorrect password')

        login_button = self.form.button_login
        QTest.mouseClick(login_button, Qt.LeftButton)
        self.assertEqual(self.form.label_error_message.text(), 'Email and Password do not match')
        self.assertEqual(self.form.get_lecturer_id(), False)
        self.assertEqual(self.form.app_pages.currentIndex(), 0)
        self.assertEqual(self.form.cb_module.count(), 0)

    def test_login(self):
        self.form.entry_email.setText('roberta@university.ac.uk')
        self.form.entry_password.setText('roberta')

        loginButton = self.form.button_login
        QTest.mouseClick(loginButton, Qt.LeftButton)
        self.assertEqual(self.form.get_lecturer_id(), 2)
        self.assertEqual(self.form.app_pages.currentIndex(), 1)
        self.assertGreater(self.form.cb_module.count(), 0)

    def test_time_selection(self):
        self.form.spin_box_time.setValue(2)

        self.assertEqual(self.form.spin_box_time.value(), 2)

    def test_logout(self):
        logout_button = self.form.button_logout
        QTest.mouseClick(logout_button, Qt.LeftButton)
        self.assertEqual(self.form.app_pages.currentIndex(), 0)

    def test_login_page_after_logout(self):
        self.assertEqual(self.form.label_login_title.text(), 'Login Page')
        self.assertEqual(self.form.label_email.text(), 'Email:')
        self.assertEqual(self.form.label_password.text(), 'Password:')
        self.assertEqual(self.form.entry_email.text(), '')
        self.assertEqual(self.form.entry_password.text(), '')

    def test_login_and_start_app(self):
        self.form.entry_email.setText('roberta@university.ac.uk')
        self.form.entry_password.setText('roberta')

        loginButton = self.form.button_login
        QTest.mouseClick(loginButton, Qt.LeftButton)

        self.assertEqual(self.form.get_lecturer_id(), 2)
        self.assertEqual(self.form.app_pages.currentIndex(), 1)
        self.assertGreater(self.form.cb_module.count(), 0)

        start_button = self.form.button_navigate_start
        QTest.mouseClick(start_button, Qt.LeftButton)

        self.assertEqual(self.form.app_pages.currentIndex(), 2)
        self.assertGreater(self.form.list_attendance.count(), 0)
        # test camera is active
        self.assertIsNotNone(self.form.camera_feed_widget.camera_feed.camera)

    # TODO: camera destroyed, attendance list populated




