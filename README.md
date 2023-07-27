
# Photometric Light Curve Analysis

This project performs aperture photometry on TESS Full Frame Images (FFIs) to generate light curves and analyze variable stars.

## Overview

- `ExtractFromFFIs.py` contains functions to process FITS files from the TESS mission, perform aperture photometry on identified sources, calculate fluxes and flux errors, and output CSV files with the results.

- `PlotLightCurve.py` demonstrates loading the CSV files, identifying the target star using coordinates, extracting the flux over time, and generating a light curve plot.

- The `photometry_results` folder contains example CSV output files from `ExtractFromFFIs.py`.

## Background

The [TESS](https://www.nasa.gov/tess-transiting-exoplanet-survey-satellite) (Transiting Exoplanet Survey Satellite) is a NASA astrophysics mission launched in 2018 to survey the sky for exoplanets. 

TESS takes images of large sectors of the sky in 26 observation sectors, producing Full Frame Images (FFIs) with a 30 minute cadence. The FFIs are stored in FITS format.

This project processes the TESS FFIs to perform aperture photometry on stars detected in the images. This generates flux measurements over time that can be used to plot light curves and analyze stellar variability.

Photutils, Astropy, and other Python libraries are used to handle FITS files, calculate photometry, and analyze the resulting data.

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

- Photutils documentation: https://photutils.readthedocs.io/en/stable/
- TESS mission: https://www.nasa.gov/tess-transiting-exoplanet-survey-satellite
- TESS Input Catalog: https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html

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




