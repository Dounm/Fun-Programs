# !/usr/bin/env python3


import sys

import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-o', '--output')
parser.add_argument('--width', type=int, default=80)
parser.add_argument('--height', type=int, default=80)
args = parser.parse_args()

img_path = args.file
width = args.width
height = args.height
output_path = args.output

ascii_chars = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def get_char(r, g, b, alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_chars)    
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1) / length
    return ascii_chars[int(gray/unit)]

if __name__ == '__main__':
    img = Image.open(img_path)
    img = img.resize((width, height), Image.NEAREST)

    txt = ""
    for i in range(height):
        for j in range(width):
            txt += get_char(*img.getpixel((j,i)))
        txt += '\n'
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(txt)
    else:
        with open('output.txt', 'w') as f:
            f.write(txt)
