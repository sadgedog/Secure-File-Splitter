# About this

image splitter is an application that allows you to secure your secret images by distributing them.

# Detail

image splitter distributes an image into several "shares" based on Samir's secret sharing.
The individual shares themselves have no special meaning, and original image can be restored only when it has attracted more than a predetermined "threshold" number of shares.



![explain](./docs/explain.png)

# How to run

- Run : ./test.sh or python3 main.py

image splitter includes sympy, numpy and cv2 as external libraries.
Therefore, please install those libraries when you test this.

- Demo

BMP format test\
![test](./docs/example.gif)

JPEG format test\
![JPEG](./docs/example2.gif)



It takes 0.87sec to recover JPEG image\
Generate Shares -> 9.15 MB/sec\
Recover Images -> 413 KB/sec


# TODO:
- Support PNG

- Improve efficiency

- Support Video format
