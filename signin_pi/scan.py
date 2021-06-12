def scan_qr():

    import cv2

    # set up camera object
    cap = cv2.VideoCapture(0)

    # QR code detection object
    detector = cv2.QRCodeDetector()


    while True:
        # get the image
        _, img = cap.read()
        # get bounding box coords and data
        retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(img)

        if len(decoded_info) == 2:
            print("data found: ")
            # Scan img

            first_array_one = points[0][0].astype(int).tolist()
            first_array_two = points[0][1].astype(int).tolist()
            first_array_third = points[0][2].astype(int).tolist()

            second_array_one = points[1][0].astype(int).tolist()
            second_array_two = points[1][1].astype(int).tolist()
            second_array_third = points[1][2].astype(int).tolist()

            #test which QR points is left or right
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



            crop_img = img[y:y+h, x:x+w]

            cv2.imshow("Image", crop_img)

        # display the image preview
        cv2.imshow("code detector", img)
        
        if(cv2.waitKey(1) == ord("q")):
            break
        
    # free camera object and exit
    cap.release()
    cv2.destroyAllWindows()









