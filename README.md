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

BMP format test
![test](./docs/example.gif)

JPEG format test
![JPEG](./docs/example2.gif)


# TODO:
- Support PNG

- Improve efficiency.\
Relatively new python versions are very slow in converting very very long Integer type to  String.
For this reason, Integer types with more than 4300 digits are prohibited (this limit can be removed by using sys.set_int_max_str_digits()).
Despite avoiding these causes of very slow speed, this application is still very very slow when distributing large files such as JPEGs.