import glob  # for file operations
import numpy as np
from astropy.io import fits  # for handling FITS files
from astropy.stats import sigma_clipped_stats  # for statistical operations on data
from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture, aperture_photometry  # for photometry tasks
import pandas as pd
from datetime import datetime
from astropy.wcs import WCS  # World Coordinate System (WCS)
from astropy.time import Time
from astroquery.mast import Catalogs  # for querying the Mikulski Archive for Space Telescopes (MAST)
import time
import matplotlib.pyplot as plt


def closest_source(sources, position):
    """
    This function identifies the closest source to a given position in an image.

    Parameters:
    - sources: A table of identified sources, where each source has 'xcentroid' and 'ycentroid' properties.
    - position: A tuple containing the (x, y) position to which we want to find the closest source.

    The function calculates the Euclidean distance from the given position to each source and returns the source
    with the smallest distance.
    """
    distances = np.sqrt((sources['xcentroid'] - position[0]) ** 2 + (sources['ycentroid'] - position[1]) ** 2)
    return sources[np.argmin(distances)]


def compare_to_background(phot_table, median):
    """
    This function compares the aperture sum for each source in a photometry table to the median background level.
    If the value is significantly above 1, it indicates that the source is brighter than the background.
    Conversely, if it is close to 1 or less, it suggests that the source is not much brighter than the background,
    which could mean that it is faint or that it could be noise rather than a real source.
    On average, a good rule of thumb might be that a star of interest should be at least 5-10 times brighter than
    the median background level to be clearly detectable.

    Parameters:
    - phot_table: A table with photometry results for each source, including an 'aperture_sum' property.
    - median: The median background level of the image.

    The function adds a 'aperture_to_background' column to the photometry table, which is calculated as
    'aperture_sum' divided by 'median', and returns the updated table.
    """
    phot_table['aperture_to_background'] = phot_table['aperture_sum'] / median
    phot_table['median'] = median  # median background level
    return phot_table




def add_tic_ids(df):
    """
    This function adds a TIC ID column to a DataFrame containing RA and Dec coordinates for each source.

    Parameters:
    - df: The DataFrame to add TIC IDs to. Must include 'ra' and 'dec' columns.

    The function queries the TESS Input Catalog for each source and adds a 'tic' column to the DataFrame.
    radius: 0.001 degrees * 60 arcminutes/degree = 0.06 arcminutes
    """
    # Initialize an empty list to store the TIC IDs
    tic_ids = []

    # For each source, query the TESS Input Catalog
    for i, row in df.iterrows():
        # 0.001 degrees * 60 arcminutes/degree = 0.06 arcminutes
        catalogData = Catalogs.query_object(f"{row['ra']} {row['dec']}", radius=0.001, catalog="TIC") # modify the radius
        if len(catalogData) > 0:
            tic_id = catalogData[0]['ID']
        else:
            tic_id = None

        tic_ids.append(tic_id)
        # print('tic_id: ', tic_id)

        # Introduce a small delay between queries to avoid overwhelming the server
        time.sleep(0.5)

    # Add the TIC IDs as a new column in the DataFrame
    df['tic'] = tic_ids

    return df


def perform_photometry(data, sources):
    """
    This function performs aperture photometry on an image for a given list of sources.

    Parameters:
    - data: A 2D numpy array representing the image data.
    - sources: A table of identified sources, where each source has 'xcentroid' and 'ycentroid' properties.

    The zip function combines the 'xcentroid' and 'ycentroid' arrays into pairs of coordinates,
    and list converts it into a list of tuples.
    The function returns a table with the photometry results for each source.
    """
    positions = list(zip(sources['xcentroid'], sources['ycentroid']))
    apertures = CircularAperture(positions, r=3.)  # r can be modified
    phot_table = aperture_photometry(data, apertures)

    return phot_table


def calculate_flux(phot_table, exposure_time):
    """
    This function calculates the flux for each source in a photometry table.

    Parameters:
    - phot_table: A table with photometry results for each source, including an 'aperture_sum' property.
    - exposure_time: The exposure time of the image, in seconds.

    flux is the amount of light received per unit time, so by dividing the total amount of light received
    ('aperture_sum') by the time it took to receive that light ('exposure_time'), we get the flux
    """
    phot_table['flux'] = phot_table['aperture_sum'] / exposure_time  # flux is the amount of light received per time
    return phot_table


def calculate_flux_error(phot_table, n_pixels, median, gain, std):
    """
    This function calculates the flux error for each source in a photometry table.

    Parameters:
    - phot_table: A table with photometry results for each source, including an 'aperture_sum' property.
    - n_pixels: The number of pixels inside the aperture.
    - median: The median background level of the image.
    - gain: The gain of the image detector, in electrons per ADU. (e.g., a CCD camera) (свойство детектора изображения)
    - std: The standard deviation of the background noise in the image. (стандартное отклонение фонового шума)

    1. Poisson noise from the signal: This is represented by the phot_table['aperture_sum'] / gain term in the formula.
       It is due to the fact that light consists of discrete photons, and therefore the number arriving in any given
       time period follows a Poisson distribution.
    2. Poisson noise from the background: This is represented by the n_pixels * median * gain term. It is due to the
       variation in the number of photons coming from the background.
    3. Read noise from the detector: This is represented by the n_pixels ** 2 * std ** 2 term. It is an additional
       source of noise caused by the electronics in the detector when it reads out the image.
    """
    # sum the squares and take the square root of the total
    phot_table['flux_error'] = np.sqrt(  # because uncertainties in quadrature
        phot_table['aperture_sum'] / gain  # Poisson distribution
        + n_pixels * median * gain  # Poisson noise from the background
        + n_pixels ** 2 * std ** 2)  # Read noise from the detector
    return phot_table


def format_time(time_string):
    """
    Convert a time string in the format "%Y-%m-%dT%H:%M:%S.%f" to
    a more classic format.
    """
    dt = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S.%f")
    classic_time = dt.strftime("%I:%M:%S %p on %B %d, %Y")
    return classic_time


def process_fits_file(fits_file):
    """
    This function processes a FITS file and performs photometry on the sources found in the image.

    Parameters:
    - fits_file: The path to the FITS file to process.

    The function opens the FITS file, reads the image data, estimates the background and background noise, finds the
    sources in the image using DAOStarFinder, performs aperture photometry on the sources, calculates the exposure
    time from the FITS header, calculates the flux for each source, estimates the number of pixels in the aperture,
    estimates the gain, calculates the flux error for
    each source, and finally returns a tuple containing the photometry table, sources table, exposure time, number of
    pixels, median background, gain, standard deviation of the background noise, image data, and the observation
    date from the FITS header.
    """
    # Open the FITS file
    with fits.open(fits_file) as hdu:
        data = hdu[1].data



        # Estimate the background and background noise
        mean, median, std = sigma_clipped_stats(data, sigma=3.0)  # sigma=3.0 means that any data point that is more than 3 standard deviations away from the mean will be considered an outlier and excluded from the calculations
        # mean - the average pixel value in the image
        # median - the middle pixel value when all the values are sorted
        # std - measure of the spread of pixel values around the mean

        """
        The DAOStarFinder class implements the DAOFIND algorithm (Stetson, 1987) which uses a wavelet transform of 
        the input image to calculate the local mean and standard deviation, and then selects sources where the 
        wavelet-transformed image is larger than a certain threshold above the local background.
        The FWHM=5.0 (Full Width at Half Maximum) is a measure of the extent of a function, given by the difference 
        between the two extreme values of the independent variable at which the dependent variable is equal to half of 
        its maximum value.
        The threshold=3. (limit for detection of the stars) is a value above which a star will be detected
        This means that for a local peak to be considered a star, it must be at least 3 standard deviations brighter
        than the background
        """
        # Find the stars in the image
        daofind = DAOStarFinder(fwhm=5.0, threshold=3. * std)  # fwhm can be modified
        sources = daofind(data - median)

        # Perform aperture photometry
        phot_table = perform_photometry(data, sources)



        # Calculate the exposure time
        exposure_time = hdu[0].header['TSTOP'] - hdu[0].header['TSTART']

        # Calculate the flux and add it to the photometry table
        phot_table = calculate_flux(phot_table, exposure_time)

        # Estimate the number of pixels in the aperture
        n_pixels = np.pi * 3 ** 2  # This assumes a circular aperture with a radius of 3 pixels

        # Extract the gain from the header
        gainA = hdu[1].header['GAINA']
        gainB = hdu[1].header['GAINB']
        gainC = hdu[1].header['GAINC']
        gainD = hdu[1].header['GAIND']
        gain = (gainA + gainB + gainC + gainD) / 4  # (5.2) This is an approximate value for TESS

        # Calculate the flux error and add it to the photometry table
        phot_table = calculate_flux_error(phot_table, n_pixels, median, gain, std)

        # get the header
        header = hdu[0].header
        date_obs = header['DATE-OBS']
        date_end = header['DATE-END']

        mjd_obs = Time(date_obs, format='isot', scale='utc').mjd
        mjd_end = Time(date_end, format='isot', scale='utc').mjd

        # Remember to include data in the returned tuple
        return phot_table, sources, exposure_time, n_pixels, median, gain, std, data, hdu[0].header['DATE-OBS'], mjd_obs, mjd_end


def main():
    fits_files = glob.glob('FITS2020_2_2/*.fits')  # change to folder where your FFI's (FITS) are.
    counter = 0

    for i, fits_file in enumerate(fits_files):
        counter+=1
        print(f"Processing file {counter} of {len(fits_files)}")
        phot_table, sources, exposure_time, n_pixels, median, gain, std, data, date_obs, mjd_obs, mjd_end = process_fits_file(fits_file)

        # Perform aperture photometry on all stars
        positions = [(source['xcentroid'], source['ycentroid']) for source in sources]
        apertures = CircularAperture(positions, r=3.)
        phot_table = aperture_photometry(data, apertures)

        # Add the time of the observation to the photometry table
        phot_table['time'] = format_time(date_obs)
        phot_table['MJD_OBS'] = mjd_obs  # MJD - Modified Julian Date of Observation

        with fits.open(fits_file) as hdu:
            # Initialize the WCS object
            w = WCS(hdu[1].header)

            # Convert pixel coordinates to celestial coordinates
            positions = list(zip(sources['xcentroid'], sources['ycentroid']))
            world_coords = w.all_pix2world(positions, 0)
            ra = world_coords[:, 0]
            dec = world_coords[:, 1]

            # Add RA and DEC to the photometry table
            phot_table['ra'] = ra
            phot_table['dec'] = dec

        # Calculate the flux and flux error for all stars
        phot_table = calculate_flux(phot_table, exposure_time)
        phot_table = calculate_flux_error(phot_table, n_pixels, median, gain, std)

        # Compare aperture sum to background level
        phot_table = compare_to_background(phot_table, median)

        # Save the photometry results to a CSV file
        phot_table.to_pandas().to_csv(f'photometry_results/photometry_results_{i}.csv', index=False)


if __name__ == "__main__":
    main()
