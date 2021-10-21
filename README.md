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
    1. Reclassify raster into desired classes
    2. Run 'categorical_change.py'
        - Run 'clip_rasters_to_same_extent.py' if needed
    3. Run 'clump.py' on categorical change
    4. Run 'tile_raster.py' (if needed)
        - run output of 'clump.py'
        - run input CVA raster
    5. Run 'zonal_stats_raster.py'
    6. Run 'unique_class_combinations.py'
    7. Run 'CVA_threshold.py'
    8. Run 'mosaic_tiles.py'

    # Repeat 3-5 with hybrid and Landtrendr maps to get change year raster
