#!/usr/bin/python

from __future__ import division
import sys
import os
import cv2
import numpy as np
from openslide import OpenSlide
from PIL import Image
from resizeimage import resizeimage
import random 
def getGradientMagnitude(im):
    "Get magnitude of gradient for given image"
    ddepth = cv2.CV_32F
    dx = cv2.Sobel(im, ddepth, 1, 0)
    dy = cv2.Sobel(im, ddepth, 0, 1)
    dxabs = cv2.convertScaleAbs(dx)
    dyabs = cv2.convertScaleAbs(dy)
    mag = cv2.addWeighted(dxabs, 0.5, dyabs, 0.5, 0)
    return mag


def random():
    # Parallelize on loop
    filepath="C:/Users/mathiane/OneDrive - IARC/Documents/DraftR/TCGA-AO-A0JB-01Z-00-DX1.250FE098-345B-4981-9236-0519E1C9058E.svs"
    img  = OpenSlide(filepath)
    try:
        os.mkdir("C:/Users/mathiane/OneDrive - IARC/Documents/DraftR/TCGA-COAD/tiles_preprocessed")
    except:
        print("The Folder already exist")
    try:
        os.mkdir("C:/Users/mathiane/OneDrive - IARC/Documents/DraftR/TCGA-COAD/tiles_preprocessed/TCGA-AA-3972")
    except:
        print("The Folder already exist")
    if str(img.properties.values.__self__.get('tiff.ImageDescription')).split("|")[1] == "AppMag = 40":
        sz=2048
        seq=1748
    else:
        sz=1024
        seq=874
    [w, h] = img.dimensions
    couple_coords_accepted = []
    for x in range(1, w, seq):
        for y in range(1, h, seq):
            img1=img.read_region(location=(x,y), level=0, size=(sz,sz))
            img11=img1.convert("RGB")
            img111=img11.resize((512,512),Image.ANTIALIAS)
            pix = np.array(img111)
            grad=getGradientMagnitude(pix)
            unique, counts = np.unique(grad, return_counts=True)
            mean_ch = np.mean(pix, axis=2)
            bright_pixels_count = np.argwhere(mean_ch > 220).shape[0]
            if counts[np.argwhere(unique<=15)].sum() < 512*512*0.6 and bright_pixels_count <  512*512*0.5 :
                # img111.save("/Users/mathian/Desktop/DraftR/TCGA-COAD/tiles_preprocessed/TCGA-AA-3972" + "/" + "TCGA-AA-3972.TCGA-COAD.S001" + "_" +  str(x) + "_" + str(y) + '.jpg', 'JPEG', optimize=True, quality=94)
                couple_coords_accepted.append((x,y))

    sample_random_accepted_slides = random.sample(couple_coords_accepted, 100)
    for (x,y) in sample_random_accepted_slides:
        img1=img.read_region(location=(x,y), level=0, size=(sz,sz))
        img11=img1.convert("RGB")
        print("here")
        print(type(img11))
        print(img11.size)
        img111=img11.resize((512,512),Image.ANTIALIAS)
        img111.save("TCGA-COAD/tiles_preprocessed/TCGA-AA-3972/TCGA-AA-3972.TCGA-COAD_S001" + "_" +  str(x) + "_" + str(y) + '.jpg', 'JPEG', optimize=True, quality=94)
         

if __name__ == "__main__":
   main()