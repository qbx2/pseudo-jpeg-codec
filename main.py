#!/usr/bin/env python3
import argparse
import sys
from pprint import pprint

from jpeg import JPEGEncoder, JPEGDecoder

assert sys.version_info >= (3, 6), 'Python 3.6+ is required'


def get_output_filename(filename, args):
    return f'{filename}-{args.m}-{args.scale}-{args.n}.pjpg'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['encode', 'decode', 'aio'], help='aio for all in one')
    parser.add_argument('--m', type=int)
    parser.add_argument('--scale', type=int)
    parser.add_argument('--n', type=int)
    parser.add_argument('filename', type=str, nargs='+')
    args = parser.parse_args()
    pprint(args)

    if args.mode == 'encode':
        for filename in args.filename:
            print(f'Encoding {filename}')
            output_filename = get_output_filename(filename, args)
            JPEGEncoder(filename, args.m, args.scale, args.n).save(output_filename)
    elif args.mode == 'decode':
        for filename in args.filename:
            print(f'Decoding {filename}')

            with open(filename, 'rb') as f:
                JPEGDecoder(f).save(f'{filename}.bmp')
    elif args.mode == 'aio':
        for filename in args.filename:
            print(f'Encoding {filename}')

            encoder = JPEGEncoder(filename, args.m, args.scale, args.n)
            filename = get_output_filename(filename, args)
            encoder.save(filename)

            print(f'Decoding {filename}')

            with open(filename, 'rb') as f:
                JPEGDecoder(f).save(f'{filename}.bmp')
    else:
        raise ValueError(f'Unsupported mode {args.mode}')


if __name__ == '__main__':
    main()
