
# Photometric Light Curve Analysis

This project performs aperture photometry on TESS Full Frame Images (FFIs) to generate light curves and analyze variable stars.

## Overview

- `ExtractFromFFIs.py` contains functions to process FITS files from the TESS mission, perform aperture photometry on identified sources, calculate fluxes and flux errors, and output CSV files with the results.

- `PlotLightCurve.py` demonstrates loading the CSV files, identifying the target star using coordinates, extracting the flux over time, and generating a light curve plot.

- The `photometry_results` folder contains example CSV output files from `ExtractFromFFIs.py`.

## Background

The TESS mission is searching for exoplanets using the transit method. TESS has 4 wide-field cameras that take images of 24x96 degree sections of sky continuously for 27 days each.
These Full Frame Images (FFIs) cover the entire observation sector at a 30 minute cadence. They are stored in FITS format - 16 megapixel images with a pixel scale of 21 arcseconds/pixel.
This project processes the FFIs to perform aperture photometry on all detectable stars. This generates flux measurements over time that can be analyzed to find variable stars, exoplanets, and study stellar behavior.

### The key steps are:
- Open FITS file, extract image data
- Estimate background noise (mean, median, standard deviation)
- Detect stars using DAOStarFinder in Photutils
- Perform aperture photometry around each star
- Calculate flux using total counts and exposure time
- Propagate uncertainties: photon noise, background noise, detector noise
- Add coordinates by converting pixel location to RA and Dec
- Output CSV file with fluxes, errors, times, coordinates

### The resulting high-precision light curves can be used to:
- Plot light curves and analyze stellar variability
- Search for transiting exoplanets through periodic dimming
- Generate power spectra to find stellar rotation periods
- Classify variable stars like RR Lyrae, eclipsing binaries, etc.


## Usage

The main steps are:

1. Modify `ExtractFromFFIs.py` to point to your folder of TESS FFI FITS files.

2. Run `ExtractFromFFIs.py` to loop through the FITS files. For each file it will:
   - Open the FITS and extract the image data
   - Estimate background noise
   - Detect stars using Photutils 
   - Perform aperture photometry around each star
   - Calculate flux and flux errors
   - Convert pixel coordinates to RA and Dec 
   - Output a CSV file with the photometry results

3. Specify the RA and Dec coordinates of your target star in `PlotLightCurve.py`.

4. Run `PlotLightCurve.py` to:
   - Load the CSV files 
   - Identify the target star 
   - Extract flux measurements over time
   - Plot the light curve

5. Tweak parameters and analysis as desired - aperture size, binning light curve, periodogram, etc.

## Requirements

- Python 3 
- Astropy
- Photutils
- Matplotlib
- Pandas
- Astroquery

## References

- TESS Input Catalog: https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html
- Photutils documentation: https://photutils.readthedocs.io/en/stable/
- TESS mission: https://www.nasa.gov/tess-transiting-exoplanet-survey-satellite
- Photometry Guide: https://photutils.readthedocs.io/en/stable/photometry.html


## License

This project is licensed under the MIT License - see the LICENSE file for details.

Let me know if you would like me to expand or modify this README further!












# TESS_Project


The Transiting Exoplanet Survey Satellite (TESS) project is a project led by NASA, its purpose is to examine a cyclical decrease in the illumination levels (Photon Flax) of about 200K stars in order to detect the transit of planets in the observation angle from the MCA (Exoplanet Transit).


<img width="437" alt="Screen Shot 2023-01-11 at 13 48 02" src="https://user-images.githubusercontent.com/77780368/211798780-a0ed5c6f-2921-4059-a396-52e92cd0ef54.png">

[תאור פרויקט TESS FFI.pdf](https://github.com/JosefSo/TESS_Project/files/10391931/TESS.FFI.pdf)

Relevant links:

link to google colabs of project: https://drive.google.com/drive/u/0/folders/17NqFE3CNOKlHaAtrYiTJjCToQvu5Z5Pd
https://mast.stsci.edu/tesscut/ https://docs.lightkurve.org/tutorials/1-getting-started/searching-for-data-products.html https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html https://www.researchgate.net/figure/Time-series-data-of-a-light-curve_fig2_324868315

FITS File Header Definitions: https://cdn.diffractionlimited.com/help/maximdl/FITS_File_Header_Definitions.htm




