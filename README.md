# About this

image splitter is an application that allows you to secure your secret images by distributing them.

# Detail

image splitter distributes an image into several "shares" based on Samir's secret sharing.
The individual shares themselves have no special meaning, and original image can be restored only when it has attracted more than a predetermined "threshold" number of shares.

![explain](./docs/explain.pdf)

# How to run

- Run : ./test.sh or python3 main.py

image splitter includes sympy, numpy and cv2 as external libraries.
Therefore, please install those libraries when you test this.


![test](./docs/example.gif)
