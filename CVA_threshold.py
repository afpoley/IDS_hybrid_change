# Apply radiometric change thresholds to categorical change to get hybrid change product
# Inputs: Directory of categorical change tiles, directory of zonal_stats_rasters output, csv of thresholds,
# output directory, output filename basename
# Output: hybrid change product. Radiometric change thresholds remove false categorical change
# Poley 10/21/21

import os
import glob
import rasterio
import numpy as np
from numpy import genfromtxt


def open_raster(rst_fp):
    with rasterio.open(rst_fp) as src:
        src_meta = src.meta
        rst = src.read(1)
    return rst, src_meta


# Categorical change tiles
fp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1980_1995\\tile_change\\'
# Clump tiles
fp2 = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1980_1995\\tile_means\\'
# Thresholds
fp_csv = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1980_1995\\change_thresholds.csv'
# Output directory
out_fp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1980_1995\\tile_hybrid\\'
# Output filename
out_file = 'hybrid_1985_1995_'

change_ls = glob.glob(fp + '*tif')
cva_ls = glob.glob(fp2 + '*tif')
csv = genfromtxt(fp_csv, delimiter=',', skip_header=1)
csv = csv.astype(np.uint16)

changeID = csv[:, 0]
threshold = csv[:, 1]


for img, (rst1, rst2) in enumerate(zip(change_ls, cva_ls), start=1):
    cva, meta = open_raster(rst2)
    change, meta = open_raster(rst1)
    shape = change.shape
    hybrid = np.zeros(shape)

    file_name = os.path.basename(rst1)
    out = out_fp + out_file + file_name.split('_')[-1]

    for (i, j) in zip(changeID, threshold):
        changeid = np.where(change == i, 1, 0)
        change_cva = cva * changeid
        change_cva = np.where(change_cva >= j, 1, 0)
        hybrid_temp = change_cva * change
        hybrid = hybrid + hybrid_temp

    hybrid = hybrid.astype(np.uint16)

    with rasterio.open(out, "w", **meta) as dest:
        dest.write_band(1, hybrid)

    print('File ' + str(img) + ' of ' + str(len(change_ls)) + ' done')

