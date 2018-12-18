import math
import struct

import numpy
from PIL import Image

import jpeg.dct as dct
import jpeg.huffman as huffman
from jpeg.util import ZIGZAG_INDICES_BACKWARD, build_q_table

LEN_HEADER = 11
NUM_CHANNELS = 3  # YCbCr


class JPEGDecoder:
    def __init__(self, f):
        self.f = f
        header = self.f.read(LEN_HEADER)
        self.width, self.height, self.m, self.scale, self.n = struct.unpack('<LLBBB', header)
        self.q_table = build_q_table(self.m, self.scale, self.n)

    @property
    def block_width(self):
        return math.ceil(self.width / 8.)

    @property
    def block_height(self):
        return math.ceil(self.height / 8.)

    @staticmethod
    def read_frame(f):
        huffman_dc = []
        huffman_rle = []

        for c in range(NUM_CHANNELS):
            len_dc, len_rle = struct.unpack('<LL', f.read(8))
            huffman_dc.append(f.read(len_dc))
            huffman_rle.append(f.read(len_rle))

        return huffman_dc, huffman_rle

    @staticmethod
    def huffman_idc(huffman_dc):
        return huffman.huffman_idc(huffman_dc)

    @staticmethod
    def huffman_iac_rle(huffman_rle):
        return huffman.huffman_iac_rle(huffman_rle)

    @staticmethod
    def idpcm(dpcm_dc):
        return dpcm_dc.cumsum(1)

    @staticmethod
    def run_length_decode(rle_list):
        ac_coefficients_list = []

        for rle in rle_list:
            ac_coefficients = []

            for skip, value in rle:
                if value is not None:
                    ac_coefficients += [0] * skip + [value]

            # pad with zeros
            ac_coefficients += [0] * (63 - len(ac_coefficients))
            ac_coefficients_list.append(ac_coefficients)

        return numpy.array(ac_coefficients_list)

    @staticmethod
    def inverse_zigzag_scan(zvector):
        return numpy.reshape(zvector[ZIGZAG_INDICES_BACKWARD], (8, 8))

    def dequantize(self, qblock):
        return qblock * self.q_table

    @staticmethod
    def idct(fblock):
        return dct.idct(fblock)

    @staticmethod
    def denormalize(nblock):
        return (nblock + 128).clip(0, 255).astype(numpy.uint8)

    def decode(self):
        f = self.f
        # img = Image.new('YCbCr', (self.width, self.height))
        pix = numpy.empty((self.block_height * 8, self.block_width * 8, 3), dtype=numpy.uint8)
        f.seek(LEN_HEADER)

        huffman_dc, huffman_rle = self.read_frame(f)

        num_blocks = self.block_width * self.block_height
        dpcm_dc = numpy.array([self.huffman_idc(dc)[:num_blocks] for dc in huffman_dc])
        rle_c_list = [self.huffman_iac_rle(rle) for rle in huffman_rle]

        dc_coefficients = numpy.expand_dims(self.idpcm(dpcm_dc), -1)
        ac_coefficients = numpy.stack([self.run_length_decode(rle_list) for rle_list in rle_c_list])

        zvectors = numpy.concatenate([dc_coefficients, ac_coefficients], -1)

        for c in range(zvectors.shape[0]):
            for i, zvector in enumerate(zvectors[c]):
                block_y, block_x = i // self.block_width, i % self.block_width

                qblock = self.inverse_zigzag_scan(zvector)
                fblock = self.dequantize(qblock)
                nblock = self.idct(fblock)
                block = self.denormalize(nblock)
                # write to pix
                pix[block_y*8:block_y*8+8,block_x*8:block_x*8+8,c] = block

        pix = pix[:self.height, :self.width, :]
        return Image.fromarray(pix, 'YCbCr').convert('RGB')

    def save(self, filename):
        img = self.decode()
        img.save(filename)
        print(f'Written to {filename}')

