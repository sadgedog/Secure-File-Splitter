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
        f = f.read()
    
    encoded_img = []
    # integer limit 4300 in python
    for i in range(0, len(f), split_rate):
        tmp = int.from_bytes(f[i : i + split_rate], "little")
        encoded_img.append(tmp)

    return encoded_img


def decoder(filepath: str, name, img: list) -> None:
    for i in range(len(img)):
        img[i] = img[i].to_bytes(split_rate, "little")
            
    data = b''.join(img)

    filename = filepath + name
    with open(filename, "wb") as f:
        f.write(data)

    
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
