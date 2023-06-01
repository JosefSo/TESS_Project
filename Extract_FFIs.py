import glob

import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture, aperture_photometry
import pandas as pd
from datetime import datetime

# Get a list of all FITS files in the directory
fits_files = glob.glob('FITS2020_2_2/*.fits')  # replace with your directory path

# Initialize an empty DataFrame to store the photometry results
photometry_df = pd.DataFrame()

# Loop over the FITS files
for fits_file in fits_files:
    # Open the FITS file
    with fits.open(fits_file) as hdu:
        data = hdu[1].data

        # Estimate the background and background noise
        mean, median, std = sigma_clipped_stats(data, sigma=3.0)

        # Find the stars in the image
        daofind = DAOStarFinder(fwhm=5.0, threshold=3.*std)
        sources = daofind(data - median)

        # Perform aperture photometry
        apertures = CircularAperture((sources['xcentroid'], sources['ycentroid']), r=3.)
        phot_table = aperture_photometry(data, apertures)

        tm = hdu[0].header['DATE-OBS']

        # Convert the time to a datetime object
        dt = datetime.strptime(tm, "%Y-%m-%dT%H:%M:%S.%f")

        # Convert the datetime object to a more classic format
        classic_time = dt.strftime("%I:%M:%S %p on %B %d, %Y")

        # Add the time of the observation to the photometry table
        phot_table['time'] = classic_time # hdu[0].header['DATE-OBS']

        exposure_time = hdu[0].header['TSTOP'] - hdu[0].header['TSTART']

        # Calculate the flux and add it to the photometry table
        phot_table['flux'] = phot_table['aperture_sum'] / exposure_time

        # Estimate the number of pixels in the aperture
        n_pixels = np.pi * 3**2  # This assumes a circular aperture with a radius of 3 pixels

        # Estimate the gain
        gain = 5.3  # This is an approximate value for TESS

        # Calculate the flux error and add it to the photometry table
        phot_table['flux_error'] = np.sqrt(phot_table['aperture_sum'] / gain + n_pixels * median * gain + n_pixels** 2 *std**2)

        # Append the photometry table to the DataFrame
        photometry_df = photometry_df.append(phot_table.to_pandas(), ignore_index=True)

# Save the photometry results to a CSV file
photometry_df.to_csv('photometry_results_3.csv', index=False)
