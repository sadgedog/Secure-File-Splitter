import sys
import time
import io
import cv2
from PIL import Image
from splitter import (
    rnd_scalar,
    hash_to_scalar,
    generate_share,
    generate_share_2,
)

from recover import (
    lagrange,
    lagrange_coef,
)

from const import (
    fm,
    fm_bmp,
    image_path,
    gif_path,
    gopher,
    REC,
    share_name,
    split_rate,
    split_rate_bmp,
    recover_name,
    recover_name_bmp,
    recover_name_bmp2,
    recover_name_gif,
    width, height,
)

from util import (
    encoder_bmp,
    decoder_bmp,
    encoder,
    decoder,
)

def show_img(image):
    all_image = []
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
        else:
            title = "Share" + str(i)
            cv2.imshow(title, all_image[i])
            cv2.moveWindow(title, i * W, 0)
    
    cv2.waitKey(1)


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

    cv2.waitKey(1)


def show_img3(image):
    Video = []
    W = width * 6
    H = height * 6
    for i in range(len(image)):
        Video.append(cv2.VideoCapture(image[i]))
        
    fps = Video[0].get(cv2.CAP_PROP_FPS)

    FRAME = []
    FRAME2 = []
    while Video[0].isOpened():
        ret, frame = Video[0].read()
        ret2, frame2 = Video[1].read()
        if frame is None:
            break
        FRAME.append(frame)
        FRAME2.append(frame2)
    Video[0].release()
    Video[1].release()
    
    end = False
    while True:
        if end:
            break
        for f in range(len(FRAME)):
            cv2.imshow("Original GIF", FRAME[f])
            cv2.moveWindow("Original GIF", W*3, 400)
            cv2.waitKey(int(200 / fps))
            
            cv2.imshow("Recovered GIF", FRAME2[f])
            cv2.moveWindow("Recovered GIF", W*5, 400)
            cv2.waitKey(int(200 / fps))
            k = cv2.waitKey(int(fps)) & 0xFF
            if k == 27:
                end = True
                break
            
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

    # BMP test
    Secret = encoder_bmp(gopher)
    
    shares = generate_share(Secret, n, k, fm)
        
    recovered_img = lagrange(0, shares, fm)

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
    s_all = time.perf_counter()
    s_enc = time.perf_counter()
    Secret = encoder(image_path)
    e_enc = time.perf_counter()
    print("Encode Time :   ", e_enc - s_enc)
    Shares = []

    S1 = time.perf_counter()
    # rnd coefficients
    l = []
    for i in range(1, k):
        tmp = rnd_scalar(fm)
        l.append(tmp)
        
    for i in range(len(Secret)):
        tmp = generate_share_2(Secret[i], n, k, l)
        Shares.append(tmp)
    
    E1 = time.perf_counter()
    print("Generate Time : ", E1 - S1)
    # Generate Time -> 42.04 MB/sec

    print("Encode + Generate Time : ", E1 - s_enc, "\n")

    print("Generate shares finished")
    
    S2 = time.perf_counter()
    recovered_img = []
    for i in range(len(Shares)):
        tmp = lagrange(0, Shares[i], fm)
        recovered_img.append(tmp)
        
    E2 = time.perf_counter()
    print("Recover Time :  ", E2 - S2)
    # Recover time -> 32.71 MB/sec

    s_dec = time.perf_counter()
    # write recovered image
    decoder(REC, recover_name, recovered_img)
    e_dec = time.perf_counter()
    print("Decode Time :   ", e_dec - s_dec)

    print("Recover + Decode Time : ", e_dec - S2, "\n")
    
    print("Recovered Image finished")
    
    e_all = time.perf_counter()
    print("Total Time :    ", e_all - s_all)

    # check image
    for i in range(len(Secret)):
        recovered_img[i] = int.from_bytes(recovered_img[i], "little")
        if Secret[i] == recovered_img[i]:
            pass
        else:
            print(Secret[i])
            print(recovered_img[i])
            print("Recover Failed!!")
            exit(1)
    print("Correctly Recovered JPEG IMAGE!!")

    l = [image_path]
    l.append(REC + recover_name)
    show_img2(l)


    # gif
    Secret = encoder(gif_path)
    Shares = []

    # rnd coefficients
    l = []
    for i in range(1, k):
        tmp = rnd_scalar(fm)
        l.append(tmp)

    # gen shares
    for i in range(len(Secret)):
        tmp = generate_share_2(Secret[i], n, k, l)
        Shares.append(tmp)

    # recover image
    recovered_img = []
    for i in range(len(Shares)):
        tmp = lagrange(0, Shares[i], fm)
        recovered_img.append(tmp)
        
    # write recovered image
    decoder(REC, recover_name_gif, recovered_img)

    # check image
    for i in range(len(Secret)):
        recovered_img[i] = int.from_bytes(recovered_img[i], "little")
        if Secret[i] == recovered_img[i]:
            pass
        else:
            print("Recover Failed!!")
            exit(1)
    print("Correctly Recovered JPEG IMAGE!!")

    l = [gif_path]
    l.append(REC + recover_name_gif)

    show_img3(l)


sys.set_int_max_str_digits(4500)

def camera():
    args = sys.argv
    n = int(args[1])
    k = int(args[2])
    cap = cv2.VideoCapture(0)
    
    l = []
    for i in range(1, k):
        tmp = rnd_scalar(fm)
        l.append(tmp)

    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        fmt = io.BytesIO()
        image.save(fmt, format="jpeg")
        b_frame = fmt.getvalue()

        print("encode")
        encoded_img = []
        for i in range(0, len(b_frame), split_rate):
            tmp = int.from_bytes(b_frame[i : i + split_rate], "little")
            encoded_img.append(tmp)

        print("gen shares")
        Shares = []
        for i in range(len(encoded_img)):
            tmp = generate_share_2(encoded_img[i], n, k, l)
            Shares.append(tmp)

        print("recover")
        recovered_img = []
        for i in range(len(Shares)):
            tmp = lagrange(0, Shares[i], fm)
            recovered_img.append(tmp)

        # check
        f = False
        for i in range(len(encoded_img)):
            if encoded_img[i] == recovered_img[i]:
                f = True
                pass
            else:
                print("Recover Failed!")
                f = False
                break
        if f:
            print("Recover OK!")
            
        
        print("decode")
        for i in range(len(recovered_img)):
            recovered_img[i] = recovered_img[i].to_bytes(split_rate, "little")
        data = b''.join(recovered_img)
        # data = jpeg_fmt + data
        with open(REC + recover_name, "wb") as f:
            f.write(data)
                    
        print("show")
        img = cv2.imread(REC + recover_name)
        cv2.imshow("WebCamera", img)

        key = cv2.waitKey(10)
        if key == 27:
            break
            
    cv2.destroyAllWindow()

    
def camera_bmp():
    args = sys.argv
    n = int(args[1])
    k = int(args[2])
    cap = cv2.VideoCapture(0)
    format_num = 3
    
    l = []
    for i in range(1, k):
        tmp = rnd_scalar(fm_bmp)
        l.append(tmp)

    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        fmt = io.BytesIO()
        image.save(fmt, format="bmp")
        b_frame = fmt.getvalue()

        print("encode")
        encoded_img = []
        encoded_format = []
        
        for i in range(0, format_num, split_rate_bmp):
            tmp = int.from_bytes(b_frame[i : i + split_rate_bmp], "little")
            encoded_format.append(tmp)
        
        for i in range(format_num, len(b_frame), split_rate_bmp):
            tmp = int.from_bytes(b_frame[i : i + split_rate_bmp], "little")
            encoded_img.append(tmp)
        
        print("gen shares")
        fail_Shares = []
        for i in range(len(encoded_img)):
            # tmp = generate_share(encoded_img[i], n, k, fm_bmp)
            tmp = generate_share(encoded_img[i], n, k, fm)
            fail_Shares.append(tmp)

        Shares = []
        encoded_img[0:1] = encoded_format
        for i in range(len(encoded_img)):
            # tmp = generate_share(encoded_img[i], n+1, k, fm_bmp)
            tmp = generate_share(encoded_img[i], n+1, k, fm)
            Shares.append(tmp)

        
        print("recover")
        recover_fail_img = []
        for i in range(len(fail_Shares)):
            tmp = lagrange(0, fail_Shares[i], fm_bmp)
            # tmp = lagrange(0, fail_Shares[i], fm)
            recover_fail_img.append(tmp)
            
        recover_img = []
        for i in range(len(Shares)):
            # tmp = lagrange(0, Shares[i], fm_bmp)
            tmp = lagrange(0, Shares[i], fm)
            recover_img.append(tmp)

            
        print("decode")
        recover_fail_img[0:1] = encoded_format
        re = []
        for i in range(len(recover_fail_img)):
            recover_fail_img[i] = recover_fail_img[i].to_bytes(split_rate_bmp, "little")
        data = b''.join(recover_fail_img)
        with open(REC + recover_name_bmp, "wb") as f:
            f.write(data)

        for i in range(len(recover_fail_img)):
            recover_img[i] = recover_img[i].to_bytes(split_rate_bmp, "little")
        data = b''.join(recover_img)
        with open(REC + recover_name_bmp2, "wb") as f:
            f.write(data)
            
        print("show")
        img_fail = cv2.imread(REC + recover_name_bmp)
        h = img_fail.shape[0]
        w = img_fail.shape[1]
        img_fail =  cv2.resize(img_fail, (int(w/2), int(h/2)))
        cv2.imshow("WebCamera_Fail", img_fail)
        
        img = cv2.imread(REC + recover_name_bmp2)
        img =  cv2.resize(img, (int(w/2), int(h/2)))
        cv2.imshow("WebCamera", img)
        cv2.moveWindow("WebCamera", int(w/2), -200)

        key = cv2.waitKey(10)
        if key == 27:
            break
            
    cv2.destroyAllWindow()



if __name__ == "__main__":
    args = sys.argv
    if args[3] == "main":
        main()
    elif args[3] == "camera":
        camera()
    elif args[3] == "camera_compare":
        camera_bmp()
