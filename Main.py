import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap

from PIL.ImageQt import ImageQt
from MapReturner import ImageGenerator


class MainWindow(QMainWindow):
    def __init__(self, image):
        super().__init__()

        self.setGeometry(750, 300, 800, 600)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Карта')
        self.show()
        self.image_label = QLabel(self)
        self.pixmap = QPixmap.fromImage(ImageQt(image))
        self.image_label.setPixmap(self.pixmap)

# generator.get_from_toponym("Кириши, ленинградская 6", "0.0002")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    generator = ImageGenerator()
    form = MainWindow(generator.get_from_toponym("Кириши, ленинградская 6", "0.0002"))
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
