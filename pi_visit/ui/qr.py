from PySide2.QtCore import QSize, QTimer
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox
from abc import ABCMeta, abstractmethod
import cv2
import sys
import configparser
import os
import pygame

from pi_visit.scan import scan



class Qr(QWidget):

    
    def __init__(self):
        
        super().__init__()
        self.video_size = QSize(640, 360)
        self.frame = ""
        self.quit = False
        self.directory = os.environ['MAIN_DIRECTORY']

        self.setup_ui()
        self.read_config_update()
        self.setup_camera()
        self.setup_sound()
        self.scan = scan.Scan()


    def setup_ui(self):

        self.title_label = QLabel()
        self.title_label.setFont(QFont('Arial', 14))
        self.title_label.setText(self.get_title())
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)
        self.status_label = QLabel()
        self.status_label.setFont(QFont('Arial', 30))
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.quit_button)
        self.setLayout(self.main_layout)
        self.setWindowTitle(self.get_title())


    def setup_camera(self):
        
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 
                         self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 
                         self.video_size.height())
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)


    @abstractmethod
    def display_video_stream(self):
        pass


    @abstractmethod
    def get_title(self):
        pass


    def check_show_status(self):

        self.status_label.setText(self.scan.get_status())
        self.status_label.show()


    def continue_scan(self):

        if not self.quit:
            self.capture.release()
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 
                             self.video_size.width())
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 
                             self.video_size.height())
            self.timer.start(30)


    def release_scan(self):
        self.timer.stop()
        self.capture.release()


    def setup_sound(self):
        
        pygame.init()
        pygame.mixer.music.load(
            "/home/pi/Documents/Projects/pi-visit/sounds/beep-sound.wav")


    def play_success_sound(self):

        print('play sound')
        pygame.mixer.music.play()


    def closeEvent(self, event):
        print("event")
        reply = QMessageBox.question(
            self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.release_scan()
            self.quit = True
            
            event.accept()
        else:
            event.ignore()


    def read_config_update(self):
        config = configparser.ConfigParser()
        config.read(self.directory + 'config.ini')
        res_param = config['camera']
        
        self.video_size = QSize(
            int(res_param['resolution_width']),
            int(res_param['resolution_height']))

        self.update_ui_settings()


    def update_ui_settings(self):
        self.image_label.setFixedSize(self.video_size)


    def reset(self):
        self.read_config_update()
        self.quit = False
        self.continue_scan()

        

class MultiQr(Qr):


    def display_video_stream(self):
        
        _, self.frame = self.capture.read()
        image_result = self.scan.scan_qr_img(self.frame)

        if image_result:
            self.play_success_sound()
            self.timer.stop()
            self.frame = self.scan.get_img()
            self.check_show_status()
            QTimer.singleShot(15000, self.continue_scan)

        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)

        image = QImage(
            self.frame, self.frame.shape[1], self.frame.shape[0], 
            self.frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))


    def get_title(self):

        return "Multi Scan QR"



class SingleQR(Qr):

    
    def display_video_stream(self):
        
        _, self.frame = self.capture.read()
        scan_result = self.scan.scan_singleqr_img(self.frame)

        if scan_result:
            self.play_success_sound()
            self.timer.stop()
            self.check_show_status()
            QTimer.singleShot(15000, self.continue_scan)

        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)

        image = QImage(
            self.frame, self.frame.shape[1], 
            self.frame.shape[0], self.frame.strides[0], 
            QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))


    def get_title(self):

        return "Single Scan QR"
