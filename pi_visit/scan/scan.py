import cv2
from pi_visit.database import database


class Scan():

    def __init__(self):

        # QR code detection object
        self.detector = cv2.QRCodeDetector()
        self.dbo = database.database()
        self.status = ''
        self.success_img = False
        self.success_qr = False

    def scan_qr_img(self, img):

        # get bounding box coords and data
        retval, decoded_info, points, straight_qrcode = self.detector.detectAndDecodeMulti(
            img)

        if len(decoded_info) == 2:
            print("decoded_info[0]", decoded_info[0])
            print("decoded_info[1]", decoded_info[1])

            if decoded_info[0] or decoded_info[1]:
                print("data found: ", decoded_info)

                # database log
                if decoded_info[0]:
                    self.success_qr, self.status = self.dbo.log_qr(decoded_info[0])

                elif decoded_info[1]:
                    self.success_qr, self.status = self.dbo.log_qr(decoded_info[1])

                # Scan img

                first_array_one = points[0][0].astype(int).tolist()
                first_array_two = points[0][1].astype(int).tolist()
                first_array_third = points[0][2].astype(int).tolist()

                second_array_one = points[1][0].astype(int).tolist()
                second_array_two = points[1][1].astype(int).tolist()
                second_array_third = points[1][2].astype(int).tolist()

                # test which QR points is left or right
                if first_array_two[0] > second_array_two[0]:
                    x = second_array_two[0]
                    y = second_array_two[1]
                    w = first_array_one[0] - x
                    h = first_array_third[1] - y
                else:
                    x = first_array_two[0]
                    y = first_array_two[1]
                    w = second_array_one[0] - x
                    h = second_array_third[1] - y

                self.crop_img = img[y:y+h, x:x+w]

                if len(self.crop_img) > 0:
                    self.success_img = True

                    return True
    
    def get_img(self):

        if self.success_img:
            return self.crop_img
        else:
            return False
    
    def get_status(self):
        if self.success_qr:
            return self.status
        else:
            return "ERROR"

    def reset(self):
        pass













