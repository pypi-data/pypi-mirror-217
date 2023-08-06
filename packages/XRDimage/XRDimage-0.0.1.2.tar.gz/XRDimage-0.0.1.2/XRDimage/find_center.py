import numpy as np
from PIL import Image as im
from PIL import ImageOps, ImageChops

def create_circular_mask(h, w, outer_radius, inner_radius, center=None):
  '''Create a 2048 x 2048 circular 'ring' mask for specified radii.
  
    Keyword arguments:
    
    h -- height of the bounding box for the mask
    w -- width of the bounding box for the mask
    outer_radius -- outer radius for the mask
    inner_radius -- inner radius for the mask
    center -- coordinate tuple of the center of mask. Takes the center of the image as the center if None (default: None)
  '''
  if center is None: # use the middle of the image
    center = (int(w/2), int(h/2))
  #if radius is None: # use the smallest distance between the center and image walls
  #    radius = min(center[0], center[1], w-center[0], h-center[1])
  Y, X = np.ogrid[:h, :w]
  dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
  mask = (dist_from_center <= outer_radius) & (dist_from_center >= inner_radius)
  return mask

def define_mask(h=2048, w=2048, inner_radius=40, white_width=8, black_width=10):
  '''Returns a multiring mask of the given dimensions that can be multiplied to filter an XRD image.
  
    Keyword arguments:
    
    h -- height of image
    w -- width of the image
    inner_radius -- inner radius of the first ring
    white_width -- width of the transparent ring portions for the filter
    black_width -- width of the opaque ring portions for the filter
  '''
  # get image mask dimensions
  # define center mask value
  center = (int(w/2), int(h/2))
  # set ring mask parameters
  result_mask = np.zeros((h,w))
  # iterate over entire mask to set appropriate values
  for i in range(0,50):
      start = inner_radius + (white_width + black_width) * i
      end = start + white_width
      raw_mask = create_circular_mask(w,h, outer_radius = end, inner_radius = start)
      one_array = np.ones((w,h))
      mask = raw_mask * one_array
      result_mask = np.add(result_mask, mask)
  return result_mask
  
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

def find_center(img, mask=None):
  '''
  Apply mask over central region of interest on XRD image. Find the iteration of
  maximum intensity and return corresponding coordinates. The expected XRD image 
  dimensions are 2048 x 2048.

  Keyword arguments:

  img -- input PIL XRD image from which to find the ring center
  mask -- the mask to use for finding the mask. Mask is generated through the define_mask function if None (default: None)
  '''
  if mask == None:
      mask = define_mask()
      
  mask = im.fromarray(mask)

  ### image padding
  img_padding = add_margin(img, 300, 300, 300, 300, 0)
  mask_padding = add_margin(mask, 300, 300, 300, 300, 0)

  ### find center
  max_i = -99999
  cord = np.nan
  p = 0

  for i in range (-20,20):
      for j in range(-20,20):
          offset_img = np.roll(mask_padding, i, axis=0)  ### go down
          offset_img = np.roll(offset_img, j, axis=1) ### go right
          aa = img_padding * offset_img
          c = aa.sum()
          if c > max_i:
              max_i = c
              cord = [i,j]
          elif c == max_i:
              p = p+1


  final_x = cord[1] + 1024
  final_y = cord[0] + 1024

  return final_x, final_y