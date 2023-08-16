import os

import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats


def calibrate_background(fits_files):
    data_arrays = []
    means = []
    medians = []
    stds = []

    save_path = 'calibrated_data'  # Directory where you want to save the files
    os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist

    for fits_file in fits_files:
        try:
            with fits.open(fits_file, mode='readonly') as hdu:
                data = hdu[1].data
                mean, median, std = sigma_clipped_stats(data, sigma=3.0)
                data_arrays.append(data)
                means.append(mean)
                medians.append(median)
                stds.append(std)
        except Exception as e:
            print(f"Failed to process {fits_file}: {e}")

    # Save the arrays to the specified directory
    np.save(os.path.join(save_path, 'data_arrays.npy'), data_arrays)
    np.save(os.path.join(save_path, 'means.npy'), means)
    np.save(os.path.join(save_path, 'medians.npy'), medians)
    np.save(os.path.join(save_path, 'stds.npy'), stds)
