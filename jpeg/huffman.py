import io

import numpy

HUFFMAN_DC_SIZE = {
    0: '00',
    1: '010',
    2: '011',
    3: '100',
    4: '101',
    5: '110',
    6: '1110',
    7: '11110',
    8: '111110',
    9: '1111110',
    10: '11111110',
    11: '111111110',
}
HUFFMAN_INVERSE_DC_SIZE = {v: k for k, v in HUFFMAN_DC_SIZE.items()}

HUFFMAN_COMPONENTS = {None: ''}
HUFFMAN_INVERSE_COMPONENTS = {}

# build HUFFMAN_COMPONENTS
for size in range(12):
    if size == 0:
        values = [0]
        codes = ['']
    else:
        # positive part
        s = 2 ** (size - 1)
        positive = list(range(s, s + s))
        negative = list(range(1 - s - s, 1 - s))
        values = negative + positive
        codes = [bin(code)[2:].rjust(size, '0') for code in list(range(2 ** size))]

    for value, code in zip(values, codes):
        HUFFMAN_COMPONENTS[value] = code

    HUFFMAN_INVERSE_COMPONENTS[size] = dict(zip(codes, values))

del size

HUFFMAN_AC_RL_SIZE = {
    (0, 0): '1010',
    (0, 1): '00',
    (0, 2): '01',
    (0, 3): '100',
    (0, 4): '1011',
    (0, 5): '11010',
    (0, 6): '1111000',
    (0, 7): '11111000',
    (0, 8): '1111110110',
    (0, 9): '1111111110000010',
    (0, 10): '1111111110000011',
    (1, 1): '1100',
    (1, 2): '11011',
    (1, 3): '1111001',
    (1, 4): '111110110',
    (1, 5): '11111110110',
    (1, 6): '1111111110000100',
    (1, 7): '1111111110000101',
    (1, 8): '1111111110000110',
    (1, 9): '1111111110000111',
    (1, 10): '1111111110001000',
    (2, 1): '11100',
    (2, 2): '11111001',
    (2, 3): '1111110111',
    (2, 4): '111111110100',
    (2, 5): '1111111110001001',
    (2, 6): '1111111110001010',
    (2, 7): '1111111110001011',
    (2, 8): '1111111110001100',
    (2, 9): '1111111110001101',
    (2, 10): '1111111110001110',
    (3, 1): '111010',
    (3, 2): '111110111',
    (3, 3): '111111110101',
    (3, 4): '1111111110001111',
    (3, 5): '1111111110010000',
    (3, 6): '1111111110010001',
    (3, 7): '1111111110010010',
    (3, 8): '1111111110010011',
    (3, 9): '1111111110010100',
    (3, 10): '1111111110010101',
    (4, 1): '111011',
    (4, 2): '1111111000',
    (4, 3): '1111111110010110',
    (4, 4): '1111111110010111',
    (4, 5): '1111111110011000',
    (4, 6): '1111111110011001',
    (4, 7): '1111111110011010',
    (4, 8): '1111111110011011',
    (4, 9): '1111111110011100',
    (4, 10): '1111111110011101',
    (5, 1): '1111010',
    (5, 2): '11111110111',
    (5, 3): '1111111110011110',
    (5, 4): '1111111110011111',
    (5, 5): '1111111110100000',
    (5, 6): '1111111110100001',
    (5, 7): '1111111110100010',
    (5, 8): '1111111110100011',
    (5, 9): '1111111110100100',
    (5, 10): '1111111110100101',
    (6, 1): '1111011',
    (6, 2): '111111110110',
    (6, 3): '1111111110100110',
    (6, 4): '1111111110100111',
    (6, 5): '1111111110101000',
    (6, 6): '1111111110101001',
    (6, 7): '1111111110101010',
    (6, 8): '1111111110101011',
    (6, 9): '1111111110101100',
    (6, 10): '1111111110101101',
    (7, 1): '11111010',
    (7, 2): '111111110111',
    (7, 3): '1111111110101110',
    (7, 4): '1111111110101111',
    (7, 5): '1111111110110000',
    (7, 6): '1111111110110001',
    (7, 7): '1111111110110010',
    (7, 8): '1111111110110011',
    (7, 9): '1111111110110100',
    (7, 10): '1111111110110101',
    (8, 1): '111111000',
    (8, 2): '111111111000000',
    (8, 3): '1111111110110110',
    (8, 4): '1111111110110111',
    (8, 5): '1111111110111000',
    (8, 6): '1111111110111001',
    (8, 7): '1111111110111010',
    (8, 8): '1111111110111011',
    (8, 9): '1111111110111100',
    (8, 10): '1111111110111101',
    (9, 1): '111111001',
    (9, 2): '1111111110111110',
    (9, 3): '1111111110111111',
    (9, 4): '1111111111000000',
    (9, 5): '1111111111000001',
    (9, 6): '1111111111000010',
    (9, 7): '1111111111000011',
    (9, 8): '1111111111000100',
    (9, 9): '1111111111000101',
    (9, 10): '1111111111000110',
    (10, 1): '111111010',
    (10, 2): '1111111111000111',
    (10, 3): '1111111111001000',
    (10, 4): '1111111111001001',
    (10, 5): '1111111111001010',
    (10, 6): '1111111111001011',
    (10, 7): '1111111111001100',
    (10, 8): '1111111111001101',
    (10, 9): '1111111111001110',
    (10, 10): '1111111111001111',
    (11, 1): '1111111001',
    (11, 2): '1111111111010000',
    (11, 3): '1111111111010001',
    (11, 4): '1111111111010010',
    (11, 5): '1111111111010011',
    (11, 6): '1111111111010100',
    (11, 7): '1111111111010101',
    (11, 8): '1111111111010110',
    (11, 9): '1111111111010111',
    (11, 10): '1111111111011000',
    (12, 1): '1111111010',
    (12, 2): '1111111111011001',
    (12, 3): '1111111111011010',
    (12, 4): '1111111111011011',
    (12, 5): '1111111111011100',
    (12, 6): '1111111111011101',
    (12, 7): '1111111111011110',
    (12, 8): '1111111111011111',
    (12, 9): '1111111111100000',
    (12, 10): '1111111111100001',
    (13, 1): '11111111000',
    (13, 2): '1111111111100010',
    (13, 3): '1111111111100011',
    (13, 4): '1111111111100100',
    (13, 5): '1111111111100101',
    (13, 6): '1111111111100110',
    (13, 7): '1111111111100111',
    (13, 8): '1111111111101000',
    (13, 9): '1111111111101001',
    (13, 10): '1111111111101010',
    (14, 1): '1111111111101011',
    (14, 2): '1111111111101100',
    (14, 3): '1111111111101101',
    (14, 4): '1111111111101110',
    (14, 5): '1111111111101111',
    (14, 6): '1111111111110000',
    (14, 7): '1111111111110001',
    (14, 8): '1111111111110010',
    (14, 9): '1111111111110011',
    (14, 10): '1111111111110100',
    (15, 1): '1111111111110101',
    (15, 2): '1111111111110110',
    (15, 3): '1111111111110111',
    (15, 4): '1111111111111000',
    (15, 5): '1111111111111001',
    (15, 6): '1111111111111010',
    (15, 7): '1111111111111011',
    (15, 8): '1111111111111100',
    (15, 9): '1111111111111101',
    (15, 10): '1111111111111110',
    (15, 0): '11111111001',
}
HUFFMAN_INVERSE_AC_RL_SIZE = {v: k for k, v in HUFFMAN_AC_RL_SIZE.items()}


def huffman_dc(dpcm_dc):
    bytestream = io.BytesIO()
    bits = ''

    for value in dpcm_dc:
        value = int(value)
        code_for_value = HUFFMAN_COMPONENTS[value]
        size = len(code_for_value)
        code_for_size = HUFFMAN_DC_SIZE[size]
        # print(size, value, '=>', code_for_size, code_for_value)
        bits += code_for_size + code_for_value

        while len(bits) >= 8:
            a, b = bits[:8], bits[8:]
            bytestream.write(bytes([int(a, 2)]))
            bits = b

    while bits:
        a, b = bits[:8], bits[8:]
        a = a.ljust(8, '0')
        bytestream.write(bytes([int(a, 2)]))
        bits = b

    return bytestream.getvalue()


def huffman_ac_rle(ac_rle_list):
    bytestream = io.BytesIO()
    bits = ''

    # print(hash(tuple([tuple(rle) for rle in ac_rle_list])))

    for ac_rle in ac_rle_list:
        # print(ac_rle)

        for skip, value in ac_rle:
            code_for_value = HUFFMAN_COMPONENTS[value]
            size_for_value = len(code_for_value)
            code_for_size = HUFFMAN_AC_RL_SIZE[(skip, size_for_value)]
            bits += code_for_size + code_for_value
            # print(skip, size_for_value, value, '=>', code_for_size, code_for_value)

            while len(bits) >= 8:
                a, b = bits[:8], bits[8:]
                bytestream.write(bytes([int(a, 2)]))
                bits = b

    while bits:
        a, b = bits[:8], bits[8:]
        a = a.ljust(8, '0')
        bytestream.write(bytes([int(a, 2)]))
        bits = b

    return bytestream.getvalue()


def to_bitstream(bytes_):
    bitstream = io.StringIO()

    for b in bytes_:
        bitstream.write(bin(b)[2:].rjust(8, '0'))

    bitstream.seek(0)
    return bitstream


def huffman_idc(huffman_encoded_dc):
    dpcm_dc = []
    bitstream = to_bitstream(huffman_encoded_dc)

    for_size = True
    tmp = ''

    while True:
        b = bitstream.read(1)

        if not b:
            break

        tmp += b

        try:
            if for_size:
                size = HUFFMAN_INVERSE_DC_SIZE[tmp]
                # print('size:', tmp)
            else:
                value = inverse_components[tmp]
                # print('value:', tmp)
        except KeyError:
            continue

        if for_size:
            if not size:
                for_size = False
                value = 0
                # print(size, value)
                dpcm_dc.append(value)
            else:
                inverse_components = HUFFMAN_INVERSE_COMPONENTS[size]
        else:
            # print(size, value)
            dpcm_dc.append(value)

        tmp = ''
        for_size = not for_size

    return dpcm_dc


def huffman_iac_rle(huffman_encoded_rle):
    rle_list = []
    rle = []
    bitstream = to_bitstream(huffman_encoded_rle)

    for_size = True
    tmp = ''
    num_ac = 0

    while True:
        b = bitstream.read(1)

        if not b:
            break

        tmp += b

        try:
            if for_size:
                skip, size_for_value = HUFFMAN_INVERSE_AC_RL_SIZE[tmp]
                # print('code skip/sss:', tmp)
            else:
                value = inverse_components[tmp]
                # print('code value:', tmp)
        except KeyError:
            assert for_size or len(tmp) < size_for_value, (tmp, size_for_value)
            continue

        if for_size:
            if not size_for_value:
                for_size = False
                value = None
                # print(skip, size_for_value, value)
                rle.append((skip, value))
                num_ac += skip + 1
            else:
                inverse_components = HUFFMAN_INVERSE_COMPONENTS[size_for_value]
        else:
            # print(skip, size_for_value, value)
            rle.append((skip, value))
            num_ac += skip + 1

        if rle and rle[-1] == (0, None) or num_ac == 63:
            rle_list.append(rle)
            rle = []
            num_ac = 0

        tmp = ''
        for_size = not for_size

    return rle_list
