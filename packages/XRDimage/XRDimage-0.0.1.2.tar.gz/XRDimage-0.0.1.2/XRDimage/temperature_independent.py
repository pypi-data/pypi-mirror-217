from PIL import Image as im
import numpy as np
from PIL import ImageOps, ImageChops


def add_margin(pil_img, top, right, bottom, left, color):
  '''
  Image padding script, to add 300 pixels around the border of an XRD image
  so the images become 2048 plus 600 square matrices.
  
  Keyword arguments:
  
  pil_img -- input PIL image whom to add margins
  top -- size of the top margin
  right -- size of the right margin
  bottom -- size of the bottom margin
  left -- size of the left margin
  color -- color to overlay for margins
  '''
  width, height = pil_img.size
  new_width = width + right + left
  new_height = height + top + bottom
  result = im.new(pil_img.mode, (new_width, new_height), color)
  result.paste(pil_img, (left, top))
  return result


def reshape(input_img):
  '''Change image array shape to fit resize operation.
  
  Keyword arguments:
  input_img -- the input PIL image to reshape
  '''
  result_img = input_img.resize((4194304,1))
  result_img = np.array(result_img)
  result_img = result_img[0]
  return result_img

def resize_image(img, ref_path, r_only=False, img_only=False, fixed_ratio=None):
  '''
  Resize image to desired 2048 x 2048 size by finding optimum ratio. 
  The optimum is determined by minimizing a correlation coefficent between
  the input image and a reference image.
  
  Keyword arguments:
  img --> input PIL image to resize
  ref_path --> the full path to the reference image (default: /mnt/rstor/CSE_MSE_RXF131/cradle-members/mdle/wxy215/ti64/ref.tiff)
  r_only --> true when output is the ratio number only (default: False)
  img_only --> true when output is the PIL image output only (default: False)
  fixed_ratio --> the value to fix the ratio value for computation. Set to None to retrieve ratio value automatically (default: None)
  '''
  # add padding to PIL image input
  im_padding = add_margin(img, 300, 300, 300, 300, 0)
  ref = im.open(ref_path)
  C2 = reshape(ref)

  old_size = im_padding.size
  desired_size = 2048

  ### ratio of diameter
  if fixed_ratio != None:
    ratio = np.asarray([fixed_ratio]) # fixed ratio
  else:
    ratio = np.arange(0.9, 1.1, 0.005)     # create a series of ratios, change parameters here

  max_cor = -99999
  max_img = np.nan

  # iterate over ratios to find configuration with the lowest correlation
  for i in ratio:
    new_size = tuple([int(x * i) for x in old_size]) # set reference size

    ### resize padding image
    im_re = im_padding.resize(new_size)

    # create a new image and paste the resized on it
    new_im = im.new(im_padding.mode, (desired_size, desired_size))
    new_im.paste(im_re, ((desired_size-new_size[0])//2,
                        (desired_size-new_size[1])//2))
    max_img = new_im # set max to current since there is only one

    # skip correlation if fixed ratio is no defined
    
    if fixed_ratio == None:
      # with correlation
      C1 = reshape(new_im)
      cor = np.corrcoef(C1, C2) # find correlation value between image and reference

      aa = cor[0,1] # FIXME: max_cor might not be in range
      if max_cor < aa: # set image with min correlation as the new image
        max_cor = aa
        max_img = new_im
        r = i # set min correlation ratio value as output ratio
    else:
      r = i
    
  if r_only:
      return r
  elif img_only:
      return max_img
  else:
      return max_img, r


'''
CHANGELOG:

v0_1 (Jul 23 2022) - changed ratio range from 0.95 to 1.05 to 0.9 to 1.1
                   - fixed bad condition for fixed ratio
'''