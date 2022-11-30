import cv2

width = 45
height = 58

def show_img3(image):
    image = cv2.VideoCapture(image)
        
    fps = image.get(cv2.CAP_PROP_FPS)

    while image.isOpened():
        ret, frame = image.read()
        if ret:
            cv2.imshow("frame", frame)
            cv2.waitKey(int(1000 / fps))
        else:
            image.release()
            
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # i = 0
    # while True:
    #     is_success, img = image.read()
    #     if not is_success:
    #         break
    #     images.append(img)
    #     i += 1

    # W = width * 8
    # H = height * 8

    # image = cv2.resize(all_image[i], (W, H))
    # cv2.imshow("Original GIF", image)
    # cv2.moveWindow("Original GIF", 0, 400)
    # cv2.waitKey(int(1000/fps))

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


p = "../recovered_image/recover_gif.gif"
p2 = "../recovered_image/img.jpg"
show_img3(p)
