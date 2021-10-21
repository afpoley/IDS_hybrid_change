# This script mimics the raster zonal stats tool in Arcmap; calculate mean of pixels for each image clump
# Note: Assumes input images have been tiled to same # of tiles
# Inputs: CVA tile directory, clump directory, output directory
# Output: Image with mean pixel values for each input clump
# Poley 10/21/21

import os
import fiona
import glob
import rasterio
import rasterio.mask
import numpy as np


def clip_raster(rst_fp, shp_path):
    with fiona.open(shp_path, "r") as shp_src:
        shp = [features["geometry"] for features in shp_src]

    with rasterio.open(rst_fp) as src:
        rst, rst_transform = rasterio.mask.mask(src, shp, crop=True)
        rst = rst[0]
        # rst = src.read(1)
    return rst


def open_raster(rst_fp):
    with rasterio.open(rst_fp) as src:
        src_meta = src.meta
        rst = src.read(1)
    return rst, src_meta


def raster_stat(zones, rst, ids):
    for poly in ids:
        mask = zones
        poly_means = zones
        mask = np.where(mask == poly, 1, 0)
        means = mask*rst
        means = means.astype(np.float64)
        means[means == 0] = np.nan
        means = np.nanmean(means)
        means = means.astype(np.int64)
        if poly == 1:
            means = 0
        # print(str(poly) + ': ' + str(means))
        poly_means[poly_means == poly] = means

    with rasterio.open(out_file, "w", **meta) as dest:
        dest.write_band(1, poly_means)

    return poly_means


fp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1995_2010\\tile_cva\\'
clump_pth = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1995_2010\\tile_clumps\\'
out_fp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1995_2010\\tile_means\\'


clump_ls = glob.glob(clump_pth + '*.tif')
cva_ls = glob.glob(fp + '*.tif')
clump_ls.sort(reverse=True)
cva_ls.sort(reverse=True)


for n, (img, img2) in enumerate(zip(clump_ls, cva_ls), start=1):
    file_name = os.path.basename(img)
    out_file = out_fp + 'clump_mean_' + file_name.split('_')[-1]
    cva, meta = open_raster(img2)
    clump, meta = open_raster(img)
    IDs = np.unique(clump)
    x = raster_stat(clump, cva, IDs)

    print('File ' + str(n) + ' of ' + str(len(clump_ls)) + ' done')


