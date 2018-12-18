import numpy

ZIGZAG_INDICES_BACKWARD = [
    0, 1, 5, 6, 14, 15, 27, 28,
    2, 4, 7, 13, 16, 26, 29, 42,
    3, 8, 12, 17, 25, 30, 41, 43,
    9, 11, 18, 24, 31, 40, 44, 53,
    10, 19, 23, 32, 39, 45, 52, 54,
    20, 22, 33, 38, 46, 51, 55, 60,
    21, 34, 37, 47, 50, 56, 59, 61,
    35, 36, 48, 49, 57, 58, 62, 63,
]
ZIGZAG_INDICES = numpy.empty(64, dtype=numpy.uint8)
ZIGZAG_INDICES[ZIGZAG_INDICES_BACKWARD] = numpy.arange(64)

Q_DC = 16


def build_q_table(m, scale, n):
    q_table = numpy.empty(64, dtype=numpy.uint8)
    q_table[ZIGZAG_INDICES] = [Q_DC] + [scale] * m + [scale * n] * (63 - m)
    q_table = numpy.reshape(q_table, (8, 8))
    return q_table
