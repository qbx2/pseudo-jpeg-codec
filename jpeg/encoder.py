import io
import math
import struct

import numpy
from PIL import Image

import jpeg.dct as dct
import jpeg.huffman as huffman


ZIGZAG_INDICES = numpy.empty(64, dtype=numpy.uint8)
ZIGZAG_INDICES[[
    0, 1, 5, 6, 14, 15, 27, 28,
    2, 4, 7, 13, 16, 26, 29, 42,
    3, 8, 12, 17, 25, 30, 41, 43,
    9, 11, 18, 24, 31, 40, 44, 53,
    10, 19, 23, 32, 39, 45, 52, 54,
    20, 22, 33, 38, 46, 51, 55, 60,
    21, 34, 37, 47, 50, 56, 59, 61,
    35, 36, 48, 49, 57, 58, 62, 63,
]] = numpy.arange(64)
print(ZIGZAG_INDICES)


class JPEGEncoder:
    def __init__(self, path, m, scale, n):
        rgb_img = Image.open(path)
        ycbcr_img = rgb_img.convert('YCbCr')
        self.img = numpy.array(ycbcr_img)

        print('img shape:', self.img.shape)
        self.height, self.width, self.num_channels = self.img.shape
        self.m, self.scale, self.n = m, scale, n
        assert self.num_channels == 3

        print(f'block shape: {(self.block_height, self.block_width)}')

        q_table = numpy.empty(64, dtype=numpy.uint8)
        q_table[ZIGZAG_INDICES] = [16] + [scale] * m + [scale * n] * (63 - m)
        self.quantization_table = numpy.reshape(q_table, (8, 8))
        print(f'quantization_table: {self.quantization_table}')

    def __getitem__(self, key):
        block_y, block_x = key
        y, x = block_y * 8, block_x * 8

        data = self.img[y:y+8, x:x+8]
        h, w, c = data.shape

        if 0 in (h, w):
            print(self.block_width, self.block_height)
            raise IndexError(key)

        block = numpy.zeros((8, 8, self.num_channels))
        block[:h, :w, :c] = data
        return block

    @property
    def block_width(self):
        return math.ceil(self.width / 8)

    @property
    def block_height(self):
        return math.ceil(self.height / 8)
    
    @staticmethod
    def normalize(block):
        return (block - 128).astype(numpy.int8)

    @staticmethod
    def dct(block):
        return dct.dct(block)

    def quantize(self, block):
        return numpy.round(block / self.quantization_table).astype(numpy.int32)

    @staticmethod
    def zigzag_scan(block):
        return numpy.reshape(block, 64)[ZIGZAG_INDICES]

    @staticmethod
    def run_length_encode(vector):
        dc_coefficient, ac_coefficients = vector[0], vector[1:]

        # (run_length, amplitude)
        # size will be determined in the next step
        ret = []
        run_length = 0

        for ac in ac_coefficients:
            ac = float(ac)

            if not ac:
                run_length += 1
                continue

            while run_length > 15:
                ret.append((15, 0))
                run_length -= 16

            ret.append((run_length, ac))
            run_length = 0

        if run_length:
            # Add EOB
            ret.append((0, 0))

        return dc_coefficient, ret

    @staticmethod
    def dpcm(dc_coefficients):
        # reverse: dpcm_dc.cumsum(1)
        padded = numpy.pad(dc_coefficients, ((0, 0), (1, 0)), 'constant')
        return numpy.diff(padded)

    @staticmethod
    def huffman_dc(dpcm_dc):
        return huffman.huffman_dc(dpcm_dc)

    @staticmethod
    def huffman_ac_rle(ac_rle):
        return huffman.huffman_ac_rle(ac_rle)

    def build_frame(self, huffman_dc, huffman_rle):
        buf = io.BytesIO()
        header = struct.pack('<LLBBB', self.width, self.height, self.m, self.scale, self.n)
        buf.write(header)

        for dc, rle in zip(huffman_dc, huffman_rle):
            buf.write(struct.pack('<LL', len(dc), len(rle)))
            buf.write(dc)
            buf.write(rle)

        return buf.getvalue()

    def save(self, path):
        dc_coefficients = [[] for _ in range(self.num_channels)]
        rle_list = [[] for _ in range(self.num_channels)]

        for block_y in range(self.block_height):
            for block_x in range(self.block_width):
                blocks = self[block_y, block_x]

                for c in range(blocks.shape[-1]):
                    block = blocks[..., c]
                    # print('block:', block)
                    nblock = self.normalize(block)
                    # print('nblock:', nblock)
                    fblock = self.dct(block)
                    # print('fblock:', fblock)
                    qblock = self.quantize(fblock)
                    # print('qblock:', qblock)
                    zvector = self.zigzag_scan(qblock)
                    # print('zvector:', zvector)
                    dc_coefficient, rle = self.run_length_encode(zvector)
                    # print('rle:', rle)
                    dc_coefficients[c].append(dc_coefficient)
                    rle_list[c].append(rle)

        dpcm_dc = self.dpcm(dc_coefficients)
        huffman_dc = [self.huffman_dc(dc) for dc in dpcm_dc]
        huffman_rle = [self.huffman_ac_rle(rle) for rle in rle_list]
        frame = self.build_frame(huffman_dc, huffman_rle)

        with open(path, 'wb') as f:
            f.write(frame)
            print(f'Written to {path}')
