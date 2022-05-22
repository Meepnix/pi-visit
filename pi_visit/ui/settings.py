from PySide2.QtCore import QSize, QTimer
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox
import configparser
import os


class settings(QWidget):

    def __init__(self):

        super().__init__()

        self.resolutions = {
            '640 x 360': {'width' : '640', 'height' : '360'},
            '854 x 480': {'width' : '854', 'height' : '480'},
            '960 x 540': {'width' : '960', 'height' : '540'},
            '1024 x 576': {'width' : '1024', 'height' : '576'},
            '1280 x 720': {'width' : '1280', 'height' : '720'},
            '1366 x 768': {'width' : '1366', 'height' : '768'},
            '1600 x 900': {'width' : '1600', 'height' : '900'},
            '1920 x 1080': {'width' : '1920', 'height' : '1080'}
            
        }
        self.directory = os.environ['MAIN_DIRECTORY']
        self.selected_res = ""

        self.setup_ui()
        self.check_config_exists()
        self.read_config()



    def setup_ui(self):

        layout = QVBoxLayout()
        self.res_box = QComboBox()
        
        for res in self.resolutions:
            self.res_box.addItem(res)
        
        self.res_box.currentIndexChanged.connect(self.res_box_change)

        self.button_save = QPushButton("Apply")
        self.button_save.clicked.connect(self.update_config)
        self.button_save.setEnabled(False)
        
        layout.addWidget(self.res_box)
        layout.addWidget(self.button_save)
        self.setLayout(layout)
        self.setWindowTitle("Settings")


    def res_box_change(self):
        
        if self.selected_res != self.res_box.currentText():
            self.selected_res = self.res_box.currentText()
            self.button_save.setEnabled(True)


    def check_config_exists(self):
        if not os.path.exists(self.directory + 'config.ini'):

            self.create_config()


    def create_config(self):
        config = configparser.ConfigParser()
        config.add_section('camera')
        config.set('camera', 'resolution', '640 x 360')
        config.set('camera', 'resolution_width', '640')
        config.set('camera', 'resolution_height', '360')

        with open(self.directory + 'config.ini', 'w') as configfile:
            config.write(configfile)


    def update_config(self):

        res = self.selected_res
        config = configparser.ConfigParser()
        config.read(self.directory + 'config.ini')
        camera = config['camera']
        camera['resolution'] = res
        camera['resolution_width'] = self.resolutions[res]['width']
        camera['resolution_height'] = self.resolutions[res]['height']

        with open(self.directory + 'config.ini', 'w') as configfile:
            config.write(configfile)

    
    def read_config(self):
        
        config = configparser.ConfigParser()
        config.read(self.directory + 'config.ini')

        res_param = config['camera']
        self.selected_res = res_param['resolution']

        self.set_res_box()


    def set_res_box(self):

        index = self.res_box.findText(self.selected_res)
        self.res_box.setCurrentIndex(index)


    def default_config(self):
        pass

