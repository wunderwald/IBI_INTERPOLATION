'''
Transform a discrete list ob inter-beat intervals (IBIs) to a continuous function using cubic spline interpolation.
The continuous function is sampled at a fixed sampling interval. 

by Moritz Wunderwald, 2023
'''

import os
import shutil
import glob
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

# interval of interpolated samples
INTERVAL_MS = 500

# scale interpolated IBIs so that their sum matches length of the original IBIs
USE_SCALING = False

# I/O
INPUT_DIR = 'ibiData_single'
OUTPUT_DIR = 'ibiDataInterpolated_single'

# I/0 paths
input_dir_path = os.path.join(os.getcwd(), INPUT_DIR)
output_dir_path = os.path.join(os.getcwd(), OUTPUT_DIR)

# create or re-create output folder
if os.path.exists(output_dir_path):
    shutil.rmtree(output_dir_path)
os.makedirs(output_dir_path)

# get input files
input_paths = glob.glob(f"{input_dir_path}/*.csv")

# process input files
for input_path in input_paths:
    print(f"# processing {os.path.basename(input_path)}")

    # read ibi data
    input_data_df = pd.read_csv(input_path)
    t_ms = input_data_df['t_ms'].to_numpy()
    ibi_ms = input_data_df[' ibi_ms'].to_numpy()

    # Create a cubic spline interpolation
    cs = CubicSpline(t_ms, ibi_ms)

    # Generate time grid for interpolation
    t_ms_interpl = np.arange(min(t_ms), max(t_ms), INTERVAL_MS)

    # Get sample values at new grid
    ibi_ms_interpl = cs(t_ms_interpl)

    # optionally scale interpolated ibi
    sum_ibi_original = sum(ibi_ms)
    sum_ibi_interpl = sum(ibi_ms_interpl)
    scl = sum_ibi_original / sum_ibi_interpl
    ibi_ms_interpl_out = ibi_ms_interpl * (scl if USE_SCALING else 1)

    # make output path
    input_file_w_extension = os.path.basename(input_path)
    input_filename, _ = os.path.splitext(input_file_w_extension)
    output_file = f"{input_filename}_interpolated.csv"
    output_path = os.path.join(output_dir_path, output_file)

    # write interpolated ibi data to a csv file
    csv_df = pd.DataFrame({'t_ms': t_ms_interpl, 'ibi_ms': ibi_ms_interpl_out}).round(4)
    csv_df.to_csv(output_path, index=False)