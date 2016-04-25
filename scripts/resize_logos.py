#!/usr/bin/env python

import os
import os.path as op
from PIL import Image

dirPath = op.abspath('./logos')
out_dir = op.join(dirPath, 'resize')

if not op.exists(out_dir):
    os.mkdir(out_dir)

supported_formats = ['png', 'gif', 'jpg']

for img_file in os.listdir(dirPath):

    if img_file[-3:] not in supported_formats:
        print('Extension for file {} not supported, skipped.'.format(img_file))
        continue

    print(img_file)
    img_name = img_file[:-4]
    print(img_name)

    fpath   = os.path.join(dirPath, img_file)
    outPath = os.path.join(out_dir, img_name)

    img = Image.open(fpath)
    if img.mode == "CMYK":
        img = img.convert("RGB")

    img.thumbnail((190, 90), Image.ANTIALIAS)
    img_w, img_h = img.size

    background = Image.new('RGBA', (190, 90), (255, 255, 255, 255))
    bg_w, bg_h = background.size

    offset = int((bg_w - img_w) / 2), int((bg_h - img_h) / 2)

    background.paste(img, offset)

    background.save(outPath+"_thumb.png")

