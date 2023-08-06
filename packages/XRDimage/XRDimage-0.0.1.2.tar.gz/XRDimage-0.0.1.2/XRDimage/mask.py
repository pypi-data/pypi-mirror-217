import numpy as np
from PIL import Image as im
from PIL import ImageOps, ImageChops

from .find_center import create_circular_mask

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