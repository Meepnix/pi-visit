import cv2
import os
from pi_visit.database import database


class Scan():

    def __init__(self):
        self.in_message = os.environ['IN_MESSAGE']
        self.out_message = os.environ['OUT_MESSAGE']
        self.directory = os.environ['IMG_DIRECTORY']
        # QR code detection object
        self.detector = cv2.QRCodeDetector()
        self.dbo = database.database()
        self.status = ''
        self.success_img = False
        self.success_qr = False

    def scan_qr_img(self, img):

        # get bounding box coords and data
        retval, decoded_info, vectors, straight_qrcode = self.detector.detectAndDecodeMulti(
            img)

        if len(decoded_info) == 2:
            print("decoded_info[0]", decoded_info[0])
            print("decoded_info[1]", decoded_info[1])

            if decoded_info[0] and decoded_info[1]:
                print("data found: ", decoded_info)

                self.success_qr, self.status = self.dbo.log_qr(decoded_info[0])

                return self.process_img(vectors, img, decoded_info[0])


                """
                
                # database log
                if decoded_info[0]:
                    self.success_qr, self.status = self.dbo.log_qr(decoded_info[0])

                    return self.process_img(vectors, img, decoded_info[0])

                elif decoded_info[1]:
                    self.success_qr, self.status = self.dbo.log_qr(decoded_info[1])

                    return self.process_img(vectors, img, decoded_info[1])
                """


    def process_img(self, points, image, filename):

        self.cropped_img = self.crop_img(points, image)

        if len(self.cropped_img) > 0:
            self.success_img = True
            self.save_img(filename)

            return True


    def crop_img(self, points, image):
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
        
        return image[y:y+h, x:x+w]
    
    def get_img(self):

        if self.success_img:
            return self.cropped_img
        else:
            return False
    
    def get_status(self):

        if self.success_qr:
            if self.status == 'IN':
                return self.in_message
            else:
                return self.out_message
        else:
            return "ERROR"

    def reset_success(self):

        self.status = ''
        self.success_img = False
        self.success_qr = False

    def save_img(self, filename):

        os.chdir(self.directory)
        cv2.imwrite(filename + '.jpg', self.cropped_img)

    def scan_singleqr_img(self, img):

        # get bounding box coords and data
        retval, vectors, straight_qrcode = self.detector.detectAndDecode(
            img)

        if retval is not None:
 
            print("decoded_info", retval)

            self.success_qr, self.status = self.dbo.log_qr(retval)

            return self.success_qr













