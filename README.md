Documentation for the NASA IDS change analysis.
Scripts can be used for any hybrid change detection if categorical change script is modified to account for correct class numbers (line 29).
- Poley 10/21/2021


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
1. Run 'GEE_change_vector_analysis_Landtrendr.py' in Google Earth engine (GEE). This produces change magnitude using temporally smoothed time-series produced from Landtrendr. Smoothing is based on Tasseled Cap Brightness but could be changed to another spectral index. Once finished download output image for further analysis on local machine.
2. Reclassify land cover change for years 1 and 2 into IDS change classes:
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
3. Run 'categorical_change.py'
4. Run 'clump.py' on categorical change
5. Run 'tile_raster.py' three times (run outputs of 'clump.py', 'GEE_change_vector_analysis_Landtrendr.py', and 'categorical_change.py').
6. Run 'zonal_stats_raster.py'
7. Run 'unique_class_combinations.py'
8. Manually set radiometric change thresholds for each available change class within categorical change product. Use CSV from step 7 to record threshold values in column 2. Look around image for real identifiable change, observe mean radiometric change values from 'zonal_stats_raster.py' output.
9. Run 'CVA_threshold.py'
10. Run 'mosaic_tiles.py'
11. Manually check outputs from hybrid change results and modify thresholds as needed. Repeat this process several of times.


Notes:
- Images MUST have the same number of rows & columns to run scripts
- It can be helpful to mosaic output of 'zonal_stats_raster.py' to observe mean
radiometric change when determining change thresholds.
