from PySide2.QtCore import QSize, QTimer
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

from pi_visit.scan import scan
import cv2
import sys

import pygame



class MainApp(QWidget):

    def __init__(self):

        QWidget.__init__(self)
        self.video_size = QSize(960, 540)
        self.setup_ui()
        self.setup_camera()
        self.setup_sound()
        self.scan = scan.Scan()
        self.frame = ""

    def setup_ui(self):
        
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)
        self.status_label = QLabel()
        self.status_label.setFont(QFont('Arial', 30))
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.quit_button)
        self.setLayout(self.main_layout)

    def setup_camera(self):
        
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

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
        #frame = cv2.flip(frame, 1)
        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], 
                       self.frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def check_show_status(self):

        self.status_label.setText(self.scan.get_status())
        self.status_label.show()
    
    def continue_scan(self):

        self.capture.release()
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
        self.timer.start(30)

    def setup_sound(self):
        #self.sound = AudioSegment.from_wav("/home/pi/Documents/Projects/pi-visit/sounds/beep-sound.wav")

        pygame.init()
        pygame.mixer.music.load("/home/pi/Documents/Projects/pi-visit/sounds/beep-sound.wav")

        #self.sound = pygame.mixer.Sound("")

    def play_success_sound(self):

        print('play sound')

        pygame.mixer.music.play()
        
        #play(self.sound)

        #playsound("/home/pi/Documents/Projects/pi-visit/sounds/beep-sound.mp3")
        
        

        

        








