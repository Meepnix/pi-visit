from PySide2.QtCore import QSize, QTimer
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout

from pi_visit.ui import qr, settings


class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.win_multi = None
        self.win_single = None
        self.win_settings = None

        self.button_single = QPushButton("Push for Single QR")
        self.button_multi = QPushButton("Push for Multi QR")
        self.button_settings = QPushButton("Settings")
        self.button_single.clicked.connect(self.show_single_qr_window)
        self.button_multi.clicked.connect(self.show_multi_qr_window)
        self.button_settings.clicked.connect(self.show_settings_window)

        self.widget = QWidget()
        self.menu_layout = QVBoxLayout(self.widget)
        self.menu_layout.addWidget(self.button_single)
        self.menu_layout.addWidget(self.button_multi)
        self.menu_layout.addWidget(self.button_settings)
        self.setCentralWidget(self.widget)


    def show_multi_qr_window(self):

        if self.win_multi is None:
            self.win_multi = qr.MultiQr()
            self.win_multi.show()
        elif not self.win_multi.isVisible():
            self.win_multi.show()
            self.win_multi.reset()

    def show_single_qr_window(self):
        
        if self.win_single is None:
            self.win_single = qr.SingleQR()
            self.win_single.show()
        elif not self.win_single.isVisible():
            self.win_single.show()
            self.win_single.reset()

    def show_settings_window(self):

        if self.win_settings is None:
            self.win_settings = settings.settings()
            self.win_settings.show()
        elif not self.win_settings.isVisible():
            self.win_settings.show()
            self.win_settings.reset()


        

