import math

import numpy


def dct_matrix(n):
    ret = numpy.empty((n, n))

    for k in range(n):
        for i in range(n):
            ret[k, i] = math.pi / n * (i + .5) * k

    ret = numpy.cos(ret)  
    ret[0] /= math.sqrt(2)  # X_0 /= sqrt(2)
    return ret * math.sqrt(2 / n)


def idct_matrix(n):
    ret = numpy.empty((n, n))

    for k in range(n):
        for i in range(n):
            ret[k, i] = math.pi / n * i * (k + .5)

    ret = numpy.cos(ret)
    ret[:, 0] /= math.sqrt(2)  # x_0 /= sqrt(2)
    return ret * math.sqrt(2 / n)


DCT_COEFFICIENT_MATRIX = dct_matrix(8)
IDCT_COEFFICIENT_MATRIX = idct_matrix(8)


def dct(arr):
    # scipy.fftpack.dct( scipy.fftpack.dct( a, axis=0, norm='ortho' ), axis=1, norm='ortho' )
    return (arr.T @ DCT_COEFFICIENT_MATRIX).T @ DCT_COEFFICIENT_MATRIX


def idct(arr):
    return (arr.T @ IDCT_COEFFICIENT_MATRIX).T @ IDCT_COEFFICIENT_MATRIX
