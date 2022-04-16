from PySide2.QtCore import QSize, QTimer
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout

from pi_visit.ui import qr


class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.win = None
        self.button = QPushButton("Push for Multi QR")
        self.button.clicked.connect(self.show_multi_qr_window)
        self.setCentralWidget(self.button)


    def show_multi_qr_window(self):

        if self.win is None:
            self.win = qr.MultiQr()
            self.win.show()
        elif not self.win.isVisible():
            self.win.show()

