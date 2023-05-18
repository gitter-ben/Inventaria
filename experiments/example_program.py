from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text modifier")

        layout = QVBoxLayout(self)

        self.label = QLabel("hello")
        layout.addWidget(self.label)
        
        self.font_params = {"size": 30}
        font = self.label.font()
        font.setPointSize(self.font_params["size"])
        self.label.setFont(font)

        #self.alignment = (Qt.AlignHCenter, Qt.AlignVCenter)
        #self.lagbel.setAlignment(self.alignment[0] | self.alignment[1])

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(5)
        self.slider.setMaximum(50)
        self.slider.setSingleStep(1)
        self.slider.setValue(self.font_params['size'])
        self.slider.valueChanged.connect(self.font_size_changed)
        layout.addWidget(self.slider)


        container = QWidget(self)
        container.setLayout(layout)

        self.setCentralWidget(container)

    def font_size_changed(self, value):
        self.font_params['size'] = value
        font = self.label.font()
        font.setPointSize(self.font_params['size'])
        self.label.setFont(font)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()