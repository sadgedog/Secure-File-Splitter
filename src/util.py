import sys
import time
import cv2
from const import (
    split_rate,
    image_path,
    gopher,
    REC,
    fmt,
)

# int, str間の変換は桁数が大きくなるとかなり遅い
# そのためhexのまま分割してその先でint変換する
def encoder(img: str) -> list[int]:
    with open(img, "rb") as f:
        f = f.read().hex()
    
    img = f
    encoded_img = []
    # integer limit 4300 in python
    # for each elemet -> 2900
    for i in range(0, len(img), split_rate):
        tmp = int(img[i : i + split_rate], 16)
        encoded_img.append(tmp)
        tmp = 0

    return encoded_img


def decoder(filepath: str, name, img: list) -> None:
    # 16 -> 10 -> 16で桁が消えることがあるので
    # 桁数合わせて0パディング
    s1 = time.perf_counter()

    for i in range(len(img)):
        img[i] = hex(int(img[i]))[2:]
        if len(img[i]) < split_rate  and img.index(img[-1]) != i:
            img[i] = "0" * (split_rate - len(img[i])) + img[i]
            
    data = "".join(map(str, img))
    data = bytes.fromhex(data)

    e1 = time.perf_counter()
    print(e1 - s1)

    filename = filepath + name
    with open(filename, "wb") as f:
        f.write(data)
    e2 = time.perf_counter()
    print(e2 - e1)

    
def encoder_bmp(img: str) -> int:
    with open(img, "rb") as f:
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
