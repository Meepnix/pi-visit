from PySide2.QtCore import QSize, QTimer
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from pi_visit.scan import scan
import cv2
import sys

class MainApp(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.video_size = QSize(960, 540)
        self.setup_ui()
        self.setup_camera()

        self.scan = scan.Scan()

    def setup_ui(self):
        
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)

        self.status_label = QLabel()


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
        
        _, frame = self.capture.read()

        image_result = self.scan.scan_qr_img(frame)

        if image_result:
            self.timer.stop()
            frame = self.scan.get_img()
            self.check_show_status()
            QTimer.singleShot(5000, self.continue_scan)
            
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        #frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0], 
                       frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def check_show_status(self):

        self.status_label.setText(self.scan.get_status())
        self.status_label.show()
    
    def continue_scan(self):

        self.timer.start(30)

        

        








