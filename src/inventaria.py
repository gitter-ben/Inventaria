from PyQt5.Qt import QApplication
from mainwindow import MainWindow
import sys

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())