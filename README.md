Documentation for the NASA IDS change analysis
Poley 10/21/2021


Required python packages:
- whitebox
- numpy
- rasterio
- rasterio.mask
- os
- glob
- math
- itertools
- fiona

Processing steps:
1. Reclassify land cover change for year 1 and 2 into IDS change classes:
        * 1 = urban
        * 2 = suburban
        * 3 = barren
        * 4 = agriculture
        * 5 = grasslands
        * 6 = deciduous
        * 7 = evergreen
        * 8 = shrubs
        * 9 = woody wetlands
        * 10 = non-woody wetlands
        * 11 = aquatic bed
        * 12 = water
2. Run 'categorical_change.py'
3. Run 'clump.py' on categorical change
4. Run 'tile_raster.py'
        - run output of 'clump.py'
        - run input CVA raster from Google Earth engine
5. Run 'zonal_stats_raster.py'
6. Run 'unique_class_combinations.py'
7. Manually set radiometric change thresholds for each available change
    class within categorical change product. look around image real identifiable
    change, observe mean radiometric change values from 'zonal_stats_raster.py'.
8. Run 'CVA_threshold.py'
9. Run 'mosaic_tiles.py'
10. Manually check outputs from hybrid change results and modify thresholds
    as needed. Repeat this process several of times.
