# Tile input raster into smaller chunks. Set tile size using tile_width and tile_height
# Inputs: directory with image to be tiled, filename of image to be tiled, output directory to store tiles, tile name
# For IDS change, need to run CVA and clump output
# Note: only edit first part of "output_filename" and leave "_{}-{}.tif" this will be updated with tile number
# Poley 10/21/21
import os
from itertools import product
import rasterio as rio
from rasterio import windows

# Input files
in_path = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\CVA\\updated\\'
input_filename = 'CVA_ftv_1995_2010_utm_clip2.tif'

out_path = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1995_2010\\tile_cva\\'
output_filename = 'cva_tile_{}-{}.tif'


def get_tiles(ds, width=200, height=200):
    nols, nrows = ds.meta['width'], ds.meta['height']
    offsets = product(range(0, nols, width), range(0, nrows, height))
    big_window = windows.Window(col_off=0, row_off=0, width=nols, height=nrows)
    for col_off, row_off in offsets:
        window = windows.Window(col_off=col_off, row_off=row_off, width=width, height=height).intersection(big_window)
        transform = windows.transform(window, ds.transform)
        yield window, transform


with rio.open(os.path.join(in_path, input_filename)) as inds:
    tile_width, tile_height = 200, 200

    meta = inds.meta.copy()

    for window, transform in get_tiles(inds):
        meta['transform'] = transform
        meta['width'], meta['height'] = window.width, window.height
        outpath = os.path.join(out_path, output_filename.format(int(window.col_off), int(window.row_off)))
        with rio.open(outpath, 'w', **meta) as outds:
            outds.write(inds.read(window=window))
