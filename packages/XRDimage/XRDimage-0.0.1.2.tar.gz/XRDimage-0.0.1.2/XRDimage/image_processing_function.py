from PIL import Image
import os
from os.path import join, isfile, isdir
import re
import sys

# relative imports
from dark_correction import dark_correction
from find_center import find_center
from image_registration import register_image
from temperature_independent import resize_image

def save_img(img, file_path):
  ''' Save image as tiff file to specified file path.
  
  Keyword arguments:
  
  img -- PIL image to save
  file_path -- complete file path for where to save the file
  is_dry_run -- specify whether to perform a dry-run operation (default: False)
  '''
  # save the file on different directory and filename with categorical suffix
  final_file_path = file_path.replace('darkCor_', '').replace('.tiff', '_v00_0.tiff') # TODO: change to regex
  print('saving result to path --> {}'.format(final_file_path))
  img.save(final_file_path)

def image_operations(file_path, output_folder, dark_file_path, ref_img_path):
  '''Apply preprocessing transformations to image and save to disk.
  
  Keyword arguments:
  
  file_path -- the full file path to the image input
  output_folder -- the folder for which to save the outputs
  ref_img_path -- full path to reference image to be used for resize
  '''
  try:
    curr_img = Image.open(file_path) # open image as numpy array
    curr_img = dark_correction(curr_img, dark_file_path) # TODO: add dark file path as required
    img_center_x, img_center_y = find_center(curr_img) # find the ring center
    curr_img = register_image(curr_img, img_center_x, img_center_y) # register image given center
    curr_img, ratio_value = resize_image(curr_img, ref_path=ref_img_path) # resize the image and get the rescale ratio

    print(f'file path: {file_path}')
    print(f'image center: ({img_center_x}, {img_center_y})')
    print(f'ratio: {ratio_value}')
    
    file_name = re.findall('\w+.tiff$', file_path)[0] # get the file name of the image
    save_path = join(output_folder, file_name)
    save_img(curr_img, save_path) # save the image
  except Exception as e:
    print(e)