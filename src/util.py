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
    r_flg, encoded_img = cv2.imencode('.bmp', image)

    return encoded_img


def encoder_bmp(img: str) -> int:
    with open(img, "rb") as f:
        # enc_img = f.read()
        # enc_img = int.from_bytes(enc_img, byteorder = "big")
        enc_img = f.read().hex()
        # print(enc_img)
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
