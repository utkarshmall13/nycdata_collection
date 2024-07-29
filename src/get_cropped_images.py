from os.path import join, isdir
from os import listdir, mkdir
import json
from PIL import Image
from tqdm import tqdm
import argparse

argparser = argparse.ArgumentParser(description='Download orthophotos')
argparser.add_argument('-id', '--input_dir', help='Input directory', default='../data/ortho')
argparser.add_argument('-od', '--output_dir', help='Output directory', default='../data/satelliteimages')


args = argparser.parse_args()

idir = args.input_dir
coordfile = 'coordinates.json'
odir = args.output_dir

if not isdir(odir):
    mkdir(odir)

with open(coordfile, 'r') as f:
    coords = json.load(f)

for key in tqdm(coords.keys()):
    # print(coords[key])
    im = Image.open(join(idir, key+'.jpg'))
    h, w = im.size
    for row in coords[key]:
        center = [int(row[1]*w), int((1-row[2])*h)]
        # print(row, center)
        left = max(0, center[0]-168)
        right = min(w, center[0]+168)
        top = max(0, center[1]-168)
        bottom = min(h, center[1]+168)
        if left==0:
            right = 336
        if right==w:
            left = w-336
        if top==0:
            bottom = 336
        if bottom==h:
            top = h-336
        assert right-left==336 and bottom-top==336
        im1 = im.crop((left, top, right, bottom))
        outdir = join(odir, str(row[0]//5000).zfill(4))
        if not isdir(outdir):
            mkdir(outdir)
        im1.save(join(outdir, str(row[0]).zfill(8)+'.jpg'))
        # break
    # break
    # break