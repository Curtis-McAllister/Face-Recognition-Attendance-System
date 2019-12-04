#!/usr/bin/env python3
""" Starts application, displays GUI Page components on window"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from app_gui import ApplicationGUI

__author__ = 'Curtis McAllister'
__maintainer__ = 'Curtis McAllister'
__email__ = 'mcallister_c20@ulster.ac.uk'
__status__ = 'Development'


class Application(QMainWindow, ApplicationGUI):
    """ Starts the Application, displays GUI pages on window."""
    def __init__(self, parent=None):
        super(Application, self).__init__(parent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Oxygen')
    showApplication = Application()
    sys.exit(app.exec_())
