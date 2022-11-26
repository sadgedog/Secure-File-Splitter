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
    for i in range(len(all_image)):
        # resize window
        all_image[i] = cv2.resize(all_image[i], (W, H))
        
        if i == 0:
            cv2.imshow("Original Image", all_image[i])
            cv2.moveWindow("Original Image", i, i)
        elif i == len(all_image) - 1:
            cv2.imshow("Recovered Image", all_image[i])
            cv2.moveWindow("Recovered Image", i * W, 0)
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
         print("Correctly Recovered!!")
    else:
        print("Recover Failed!!")

    l = [gopher]
    for i in range(len(shares)):
        l.append(REC + f"Share{i + 1}.bmp")
    l.append(REC + "Recovered_Image.bmp")
        
    show_img(l)


if __name__ == "__main__":
    main()
