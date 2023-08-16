
# TESS FFI Data Processing

This repository contains a collection of Python scripts to download, calibrate, analyze, and generate lightcurves from TESS Full Frame Image (FFI) data.

## Overview

The Transiting Exoplanet Survey Satellite (TESS) takes full frame images covering a 24x96 degree strip of sky with a cadence of 30 minutes. This FFI data is available on MAST archive.

This code provides a workflow to:

- Download FFI files for a given sector, date range, CCD, etc.
- Calibrate the images by removing noise, hot pixels, cosmic rays. 
- Detect stars and extract photometry using DAOStarFinder and aperture photometry
- Convert pixel positions to RA/Dec celestial coordinates using WCS
- Add star IDs by cross-matching with TIC catalog
- Calculate lightcurves and times series flux for stars of interest

The calibrated images and photometry results are saved to output folders for further analysis.

## Usage

The main entrypoint is main.py. Run this script and follow the prompt to:

1. Enter parameters to download FFIs (sector, date, CCD) 
2. Calibrate downloaded FFIs
3. Detect stars and extract photometry
4. Generate lightcurves for stars of interest

Example usage:

python main.py
Select option (1-4): 1
Enter sector, year, day, camera, CCD (comma-separated): 2, 2020, 2, 2, 1 
### Downloads FFI files for given criteria

Select option (1-4): 2
### Calibrates downloaded files

Select option (1-4): 3
### Detects stars and performs photometry 

Select option (1-4): 4
### Creates lightcurves for stars of interest

### Requirements

- astropy
- photutils
- pandas
- matplotlib
- BeautifulSoup
- requests
- numpy

### Input

- FFI files from MAST archive
- TESS Input Catalog (TIC) 

### Output

- calibrated_data/: Calibrated FFI arrays after removing noise (>3sigma clipped mean)
- photometry_results/: CSV files containing photometry data for all detected stars per image
- lightcurves/: Lightcurves for stars of interest

## Methodology

### FFI Download

FFIDownloader.py takes user input for sector, date, CCD camera, etc. It constructs a query to the MAST FFI archive and uses BeautifulSoup to scrape and download all FFI files matching that criteria.

### Calibration

FFICalibrate.py loads each FFI file, extracts the image data array, and calculates sigma-clipped stats to find the mean, median, and standard deviation of background noise. This is used for calibration and noise removal. 

The calibrated arrays are saved to calibrated_data/ for re-use.

### Photometry

FFIStarFinder.py loads the calibrated arrays and uses Photutils and DAOStarFinder to detect sources and perform aperture photometry. 

Flux is calculated using the aperture sums and exposure time. Flux errors are estimated using Poisson noise of source+background, and read noise.  

The photometry results are converted to RA/Dec using WCS package and cross-matched to the TIC catalog to get IDs.

Results are saved in photometry_results/

### Lightcurves

FFILcCreator.py loads the photometry tables, identifies the star closest to user-provided RA/Dec, and generates a lightcurve timeseries by combining the flux across all observations.

Lightcurves are saved to lightcurves/

## Credits

Photutils: https://photutils.readthedocs.io/en/stable/  
WCSAxes: https://wcsaxes.readthedocs.io/en/latest/index.html







## Background

The TESS mission is searching for exoplanets using the transit method. TESS has 4 wide-field cameras that take images of 24x96 degree sections of sky continuously for 27 days each.
These Full Frame Images (FFIs) cover the entire observation sector at a 30 minute cadence. They are stored in FITS format - 16 megapixel images with a pixel scale of 21 arcseconds/pixel.
This project processes the FFIs to perform aperture photometry on all detectable stars. This generates flux measurements over time that can be analyzed to find variable stars, exoplanets, and study stellar behavior.

#### The key steps are:
- Open FITS file, extract image data
- Estimate background noise (mean, median, standard deviation)
- Detect stars using DAOStarFinder in Photutils
- Perform aperture photometry around each star
- Calculate flux using total counts and exposure time
- Propagate uncertainties: photon noise, background noise, detector noise
- Add coordinates by converting pixel location to RA and Dec
- Output CSV file with fluxes, errors, times, coordinates

#### The resulting high-precision light curves can be used to:
- Plot light curves and analyze stellar variability
- Search for transiting exoplanets through periodic dimming
- Generate power spectra to find stellar rotation periods
- Classify variable stars like RR Lyrae, eclipsing binaries, etc.




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















# TESS_Project


The Transiting Exoplanet Survey Satellite (TESS) project is a project led by NASA, its purpose is to examine a cyclical decrease in the illumination levels (Photon Flax) of about 200K stars in order to detect the transit of planets in the observation angle from the MCA (Exoplanet Transit).


<img width="437" alt="Screen Shot 2023-01-11 at 13 48 02" src="https://user-images.githubusercontent.com/77780368/211798780-a0ed5c6f-2921-4059-a396-52e92cd0ef54.png">

[תאור פרויקט TESS FFI.pdf](https://github.com/JosefSo/TESS_Project/files/10391931/TESS.FFI.pdf)

Relevant links:

link to google colabs of project: https://drive.google.com/drive/u/0/folders/17NqFE3CNOKlHaAtrYiTJjCToQvu5Z5Pd
https://mast.stsci.edu/tesscut/ https://docs.lightkurve.org/tutorials/1-getting-started/searching-for-data-products.html https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html https://www.researchgate.net/figure/Time-series-data-of-a-light-curve_fig2_324868315

FITS File Header Definitions: https://cdn.diffractionlimited.com/help/maximdl/FITS_File_Header_Definitions.htm




