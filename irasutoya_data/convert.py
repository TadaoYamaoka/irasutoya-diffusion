#resizes and adds a black bar to all images in directory original

from PIL import Image, ImageOps

import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('in_xlsx')
parser.add_argument('out_dir')
args = parser.parse_args()

df = pd.read_excel(args.in_xlsx)
df = df.drop_duplicates()
directory = os.path.dirname(args.in_xlsx)

os.makedirs(os.path.join(args.out_dir, 'img'), exist_ok=True)
os.makedirs(os.path.join(args.out_dir, 'txt'), exist_ok=True)

for row in df[['path', 'en']].to_dict(orient='records'):
    print(row['path'])
    tmp_filename = row['path'].replace('/', '_')
    basename, ext = os.path.splitext(tmp_filename)
    basename = basename.replace('.', '_')
    img_filename = basename + ext
    txt_filename = basename + '.txt'
    try:
        im = Image.open(os.path.join(directory, row['path']))
        im = ImageOps.pad(im, (512, 512), color='black')
        im.save(os.path.join(args.out_dir, 'img', img_filename))

        txt = row['en']
        if txt[-1] != ".":
            txt += ','
        else:
            txt = txt[:-1] + ','
        txt += ' irasutoya'
        with open(os.path.join(args.out_dir, 'txt', txt_filename), 'w') as f:
            f.write(txt)
    except:
        print('skip')
