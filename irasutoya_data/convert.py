#resizes and adds a black bar to all images in directory original

from PIL import Image, ImageOps

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('in_dir')
parser.add_argument('out_dir')
args = parser.parse_args()

directory = args.in_dir

for filename in os.listdir(directory):
    var1 = os.path.join(directory, filename)
    if os.path.isfile(var1):
        print(var1)
        try:
            im = Image.open(var1)
            im = ImageOps.pad(im, (512, 512), color='black')
            im.save(os.path.join(args.out_dir, filename))
        except:
            print('skip')
