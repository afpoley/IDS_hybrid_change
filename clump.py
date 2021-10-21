# Calculate raster clumps (groups of connected pixels with the same value, i.e. image objects) using WhiteBox Tools
# Inputs: categorical change, output filepath
# Output: raster with clump numbers
# Poley 10/21/21

import glob
import os
import whitebox

wbt = whitebox.WhiteboxTools()
# wbt.verbose = False

# Input files
fp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1995_2010\\catChange1995_2010.tif'
out_file = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\LCMAP\\MTRI_analysis\\1995_2010\\change_clumps.tif'


wbt.clump(fp, out_file, diag=True, zero_back=False)

