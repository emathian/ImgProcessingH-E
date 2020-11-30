
from __future__ import division
import sys
import os
import cv2
import numpy as np
from openslide import OpenSlide
from PIL import Image
from resizeimage import resizeimage

filepath="TNE0277.mrxs"
img  = OpenSlide(filepath)
print()
print(img.dimensions)
Size = img.dimensions
img1=img.read_region(location=(0,0), level=0, size=(65000,65000))
img11=img1.convert("RGB")
#new_image = img11.resize((1500, 1500))
img11.save("TNE0277_small_size.jpeg")