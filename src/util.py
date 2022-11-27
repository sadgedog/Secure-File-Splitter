import sys
sys.set_int_max_str_digits(1000000000)

import cv2
from const import (
    image_path,
    gopher,
    REC,
    fmt,
)

# TODO : jpeg, png, etc...
def encoder(img: str) -> str:
    image = cv2.imread(img)
    # cv2.imshow("img", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    r_flg, encoded_img = cv2.imencode('.jpeg', image)

    return encoded_img

# int, str間の変換は桁数が大きくなるとかなり遅い
# そのためhexのまま分割してその先でint変換する
def encoder_jpeg(img: str) -> list[int]:
    # img = encoder(img)
    with open(img, "rb") as f:
        f = f.read().hex()
        # f = int(f, 16)
    img = f
    encoded_img = []
    # integer limit 4300 in python
    # for each elemet -> 1000 * (1 ~ 3)
    # img = str(img)
    for i in range(0, len(img), 1000):
        tmp = "".join(map(str, img[i : i + 1000]))
        tmp = int(tmp, 16)
        encoded_img.append(tmp)

    return encoded_img


def decoder_jpeg(filepath: str, name, img: list) -> None:
    # 16 -> 10 -> 16で桁が消えることがあるので
    # 桁数合わせて0パディング
    for i in range(len(img)):
        img[i] = hex(int(img[i]))[2:]
        while len(img[i]) % 1000 != 0 and img.index(img[-1]) != i:
            img[i] = "0" + img[i]
    data = "".join(map(str, img))
    data = bytes.fromhex(data)
    
    filename = filepath + name
    with open(filename, "wb") as f:
        f.write(data)

# decoder_jpeg("../recovered_image/", "test.jpeg", Result)
    

def encoder_bmp(img: str) -> int:
    with open(img, "rb") as f:
        # enc_img = f.read()
        # enc_img = int.from_bytes(enc_img, byteorder = "big")
        enc_img = f.read().hex()
        print(enc_img)
        enc_img = enc_img[len(fmt):]
        enc_img = int(enc_img, 16)
        
    return enc_img


def decoder_bmp(filepath: str, name, img: int) -> None:
    # remove "0x"
    data = hex(img)[2:]
    # align for bytes
    if (len(data) % 2 != 0):
        data += "0"
    data = fmt + data
    data = bytes.fromhex(data)
    filename = filepath + name
    with open(filename, "wb") as f:
        f.write(data)
