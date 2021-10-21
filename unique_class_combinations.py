# Get unique change class combinations from categorical change.
# Inputs: categorical change, output csv filepath
# Output: CSV of all the categorical change classes present. Used to set individual change thresholds for hybrid change
# Poley 10/21/21

import rasterio
import numpy as np


def open_raster(rst_fp):
    src = rasterio.open(rst_fp)
    img = src.read()
    return img


fp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1995_2010\\catChange1995_2010.tif'
out = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1995_2010\\change_thresholds.csv'

rst = open_raster(fp)
classes = np.unique(rst)
classes = classes.astype(int)
np.savetxt(out, classes, delimiter=',')

