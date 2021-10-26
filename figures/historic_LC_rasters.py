import rasterio
from rasterio.merge import merge
from rasterio import features
import geopandas as gpd
import pandas as pd
import numpy as np
import os


fp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\FINAL_1995_2010\\hybrid_1995_2010_filter.shp'
base_pth = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\yearly_classifications\\final_1995.tif'
date = pd.read_csv('D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\FINAL_1995_2010\\hybrid_1995_2010_LT.csv')
out_temp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\yearly_classifications\\temp\\final'
out_pth = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\yearly_classifications\\final_'
default_yr = ['1996', '2010']
null_yr = ['0', '2011']


change = gpd.read_file(fp)
date['Id'] = date['Id'].round(0).astype(np.int64)
data = pd.merge(change, date[['Id', 'MAJORITY']], on='Id', how='left')
data['gridcode'] = data['gridcode'].astype(str).str[-2:].astype(np.uint8)

data['MAJORITY'] = data['MAJORITY'].fillna(0)
data['MAJORITY'] = data['MAJORITY'].astype(np.uint16)
data['MAJORITY'] = data['MAJORITY'].astype(np.str)
data['MAJORITY'] = data['MAJORITY'].replace(null_yr, default_yr)
years = data['MAJORITY'].unique()
years.sort()

rst = rasterio.open(base_pth)
meta = rst.meta.copy()

#%%
list = []
list.append(base_pth)
for year in years:
    data_yr = data.loc[data['MAJORITY'] == year]
    out = out_temp + year + '.tif'
    out_final = out_pth + year + '.tif'
    list.append(out)

    with rasterio.open(out, 'w+', **meta) as out:
        out_arr = out.read(1)

        # this is where we create a generator of geom, value pairs to use in rasterizing
        shapes = ((geom, value) for geom, value in zip(data_yr.geometry, data_yr.gridcode))
        burned = features.rasterize(shapes=shapes, fill=0, out=out_arr, transform=out.transform)
        out.write_band(1, burned)

    base = rasterio.open(list[0])
    mask = rasterio.open(list[1])
    merge_list = []
    merge_list.append(base)
    merge_list.append(mask)

    mosaic, out_trans = merge(merge_list, method='last', nodata=0)

    with rasterio.open(out_final, "w", **meta) as dest:
        dest.write(mosaic)

    out.close()
    mask.close()
    os.remove(list[1])
    list = []
    list.append(out_final)
    print("Finished: " + out_pth + year + '.tif')

print('done')
