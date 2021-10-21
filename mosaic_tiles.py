import glob
import rasterio
from rasterio.merge import merge


def open_raster(rst_fp, files):
    src = rasterio.open(rst_fp)
    src_meta = src.meta
    files.append(src)
    return src_meta


data = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1980_1995\\tile_hybrid\\'
out_fp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1980_1995\\hybrid_1985_1995.tif'

ls = glob.glob(data + '*tif')
mosaic_ls = []

for file in ls:
    meta = open_raster(file, mosaic_ls)

mosaic, out_trans = merge(mosaic_ls, method='first', nodata=0)

# Copy the metadata
out_meta = meta.copy()
print(out_meta)

out_meta.update({'driver': 'GTiff',
                 'width': mosaic.shape[2],
                 'height': mosaic.shape[1],
                 'count': mosaic.shape[0],
                 'transform': out_trans,
                 'nodata': 0})

print(out_meta)

# Write the mosaic raster to disk
with rasterio.open(out_fp, "w", **out_meta) as dest:
    dest.write(mosaic)

print('done')
