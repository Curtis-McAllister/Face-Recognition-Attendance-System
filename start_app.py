import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from app_gui import ApplicationGUI


class Application(QMainWindow, ApplicationGUI):
    def __init__(self, parent=None):
        super(Application, self).__init__(parent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Oxygen')
    showApplication = Application()
    sys.exit(app.exec_())
