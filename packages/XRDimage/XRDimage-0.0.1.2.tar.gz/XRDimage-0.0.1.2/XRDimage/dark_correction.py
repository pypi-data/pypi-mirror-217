import numpy as np
from PIL import Image as im

def dark_correction(img, dark_file_path, threshold=16384):
  '''
  Apply darkness correction to the specified input file and output
  a dark-corrected PIL image.

  Keyword arguments:

  img -- input file image for dark correction
  dark_file_path -- full path to reference image whose pixels are subtracted from those of the input images
  threshold -- the intensity value below which the pixels are set to 0
  '''
  img_arr = np.array(img) # open image as array
  img_dark = np.array(im.open(dark_file_path)) # open reference image as array

  ### dark correction: minus orignal im
  darkCor = img_arr - img_dark

  ### set all negative value as 0
  darkCor[darkCor > threshold] = 0 # set threshold at given number
  save_img = im.fromarray((darkCor))
  return save_img