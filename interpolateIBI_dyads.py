'''
Transform a discrete list of inter-beat intervals (IBIs) to a continuous function using cubic spline interpolation.
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

# scale interpolated IBIs so that their sum matches length of the original recording
USE_SCALING = False

# I/O
INPUT_DIR = 'ibiData_dyads'
OUTPUT_DIR = 'ibiDataInterpolated_dyads'

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
    t_ms_combined = input_data_df['t_ms'].to_numpy()
    ibi_ms_combined = input_data_df[' ibi_ms'].to_numpy()
    ecg_markers = input_data_df[' ecg_id'].to_numpy()

    # make indices to split data
    sampleIsEcg1 = ecg_markers == ' ecg1'
    sampleIsEcg2 = ecg_markers == ' ecg2'
    
    # split data
    t_ms_ecg1 = t_ms_combined[sampleIsEcg1]
    ibi_ms_ecg1 = ibi_ms_combined[sampleIsEcg1]
    t_ms_ecg2 = t_ms_combined[sampleIsEcg2]
    ibi_ms_ecg2 = ibi_ms_combined[sampleIsEcg2]

    # Create a cubic spline interpolation
    cs_ecg1 = CubicSpline(t_ms_ecg1, ibi_ms_ecg1)
    cs_ecg2 = CubicSpline(t_ms_ecg2, ibi_ms_ecg2)

    # Generate time grid for interpolation
    t_ms_interpl = np.arange(min(t_ms_combined), max(t_ms_combined), INTERVAL_MS)

    # Get interpolated sample values
    ibi_ms_interpl_ecg1 = cs_ecg1(t_ms_interpl)
    ibi_ms_interpl_ecg2 = cs_ecg2(t_ms_interpl)

    # make scaling factors
    recording_length = t_ms_combined[len(t_ms_combined)-1] - t_ms_combined[0]
    sum_ibi_interpl_ecg1 = sum(ibi_ms_interpl_ecg1)
    sum_ibi_interpl_ecg2 = sum(ibi_ms_interpl_ecg2)
    scl_ecg1 = recording_length / sum_ibi_interpl_ecg1
    scl_ecg2 = recording_length / sum_ibi_interpl_ecg2
    
    # optionally scale interpolated ibi
    ibi_ms_interpl_out_ecg1 = ibi_ms_interpl_ecg1 * (scl_ecg1 if USE_SCALING else 1)
    ibi_ms_interpl_out_ecg2 = ibi_ms_interpl_ecg2 * (scl_ecg2 if USE_SCALING else 1)

    # make output path
    input_file_w_extension = os.path.basename(input_path)
    input_filename, _ = os.path.splitext(input_file_w_extension)
    output_file = f"{input_filename}_interpolated.csv"
    output_path = os.path.join(output_dir_path, output_file)

    # write interpolated ibi data to a csv file
    csv_df = pd.DataFrame({
        't_ms': t_ms_interpl, 
        'ibi_ms_ecg1': ibi_ms_interpl_out_ecg1, 
        'ibi_ms_ecg2': ibi_ms_interpl_out_ecg2, 
    }).round(4)
    csv_df.to_csv(output_path, index=False)