import sys
import cv2
import sympy
import numpy
from splitter import (
    rnd_scalar,
    hash_to_scalar,
    generate_share,
)

from recover import (
    lagrange,
    lagrange_coef,
)

from const import (
    image_path,
    gopher,
    REC,
    width, height,
)

from util import (
    encoder_bmp,
    decoder_bmp,
    encoder_jpeg,
    decoder_jpeg,
)

def show_img(image):
    all_image = []
    # for img in image:
    #     all_image.append(cv2.imread(img))
    #     merge = numpy.hstack(all_image)
        
    # cv2.imshow("img", merge)
    for img in image:
        all_image.append(cv2.imread(img))

    # window size
    W = width * 5
    H = height * 5
    W2 = width * 8
    H2 = height * 8

    for i in range(len(all_image)):
        # resize window
        all_image[i] = cv2.resize(all_image[i], (W, H))
        # BMP
        if i == 0:
            cv2.imshow("Original Image", all_image[i])
            cv2.moveWindow("Original Image", i, i)
        elif i == len(all_image) - 1:
            cv2.imshow("Recovered Image", all_image[i])
            cv2.moveWindow("Recovered Image", i * W, 0)
        # JPEG SHOW
        # elif i == len(all_image) - 2:
        #     all_image[i] = cv2.resize(all_image[i], (W2, H2))
        #     cv2.imshow("Original JPEG Image", all_image[i])
        #     cv2.moveWindow("Original JPEG Image", 0, 400)
        # elif i == len(all_image) - 1:
        #     all_image[i] = cv2.resize(all_image[i], (W2, H2))
        #     cv2.imshow("Recovered JPEG Image", all_image[i])
        #     cv2.moveWindow("Recovered JPEG Image", W2, 400)
        # BMP
        else:
            title = "Share" + str(i)
            cv2.imshow(title, all_image[i])
            cv2.moveWindow(title, i * W, 0)
    
    cv2.waitKey(1)
    # cv2.destroyAllWindows()


def show_img2(image):
    all_image = []
    for img in image:
        all_image.append(cv2.imread(img))

    W = width * 8
    H = height * 8

    for i in range(len(all_image)):
        # resize window
        all_image[i] = cv2.resize(all_image[i], (W, H))
        # BMP
        if i == 0:
            cv2.imshow("Original JPEG Image", all_image[i])
            cv2.moveWindow("Original JPEG Image", 0, 400)
        elif i == len(all_image) - 1:
            cv2.imshow("Recovered JPEG Image", all_image[i])
            cv2.moveWindow("Recovered JPEG Image", W, 400)

        else:
            title = "Share" + str(i)
            cv2.imshow(title, all_image[i])
            cv2.moveWindow(title, i * W, 0)    

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
def main():
    args = sys.argv
    if len(args) == 1:
        n = 5
        k = 5
    else:
        n = int(args[1])
        k = int(args[2])
    
    Secret = encoder_bmp(gopher)
    
    shares = generate_share(Secret, n, k)
    for i in range(len(shares)):
        print(f"share[{i}] : ", shares[i])
        
    recovered_img = lagrange(0, shares)

    # write shares
    for i in range(len(shares)):
        decoder_bmp(REC, f"Share{i + 1}.bmp", shares[i])
    
    # write recovered image
    decoder_bmp(REC, "Recovered_Image.bmp", recovered_img)
    

    print("Original Data :  ", Secret)
    print("Recovered Data : ", recovered_img)
    if Secret == recovered_img:
         print("Correctly Recovered BMP IMAGE!!")
    else:
        print("Recover Failed!!")

    l = [gopher]
    for i in range(len(shares)):
        l.append(REC + f"Share{i + 1}.bmp")
    l.append(REC + "Recovered_Image.bmp")
        
    show_img(l)

    # JPEG TEST
    print("JPEG TEST START")
    Secret = encoder_jpeg(image_path)
    Shares = []
    for i in range(len(Secret)):
        tmp = generate_share(Secret[i], n, k)
        Shares.append(tmp)
        
    for i in range(len(Shares)):
        print(f"share[{i}]", Shares[i])
        
    print("Generate Shares completed")
    
    recovered_img = []
    for i in range(len(Shares)):
        tmp = lagrange(0, Shares[i])
        recovered_img.append(tmp)
        print("recovered_img", tmp)
        
    print("Recovered Image completed")
    
    # write recovered image
    decoder_jpeg(REC, "Recovered_JPEG_Image.jpg", recovered_img)
    print("decode Image completed")

    # check image
    for i in range(len(Secret)):
        recovered_img[i] = int(recovered_img[i], 16)
        if Secret[i] == recovered_img[i]:
            pass
        else:
            print("Recover Failed!!")
            exit(1)
    print("Correctly Recovered JPEG IMAGE!!")

    # l.append(image_path)
    # l.append(REC + "Recovered_JPEG_Image.jpg")
    l = [image_path]
    l.append(REC + "Recovered_JPEG_Image.jpg")
    show_img2(l)


if __name__ == "__main__":
    main()
