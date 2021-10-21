# Calculate categorical change between two classified maps. Assumes classes match IDS scheme (see README for class info)
# Inputs: year1 and year2 classified maps, output filepath
# Output: change product formatted like Y10Y2 or Y100Y2 (i.e. 12010 or 3001)
# Note: If using different classes than IDS, modify line 29 to reclassify non-change areas
# Poley 10/21/21

import rasterio
import rasterio.mask
import numpy as np


def open_raster(rst_fp):
    with rasterio.open(rst_fp) as src:
        src_meta = src.meta
        rst = src.read(1)
    return rst, src_meta


fp_year1 = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\final_1995_lcmap_reclass_clip.tif'
fp_year2 = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\final_2010_lcmap_reclass_clip.tif'
out_file = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1995_2010\\catChange1995_2010.tif'

y1, meta = open_raster(fp_year1)
y2, meta = open_raster(fp_year2)
change = (y1*1000) + y2
change = change.astype(np.float64)

# Reclassify non-change zones:
non_change = [1001, 2002, 3003, 4004, 5005, 6006, 7007, 8008, 9009, 10010, 11011, 12012]

for n in non_change:
    change[change == n] = np.nan

change = change.astype(np.uint16)
meta.update({'dtype': 'uint16'})

with rasterio.open(out_file, "w", **meta) as dest:
    dest.write_band(1, change)

print('Finished: ' + str(out_file))
