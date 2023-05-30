import os
from astropy.io import fits
from datetime import datetime

# The directory containing the FITS files
directory = "C://Users//kiril//PycharmProjects//pythonProject3//FFIs"

# Get a list of all FITS files in the directory
fits_files = [f for f in os.listdir(directory) if f.endswith('.fits')]

# For each FITS file
for fits_file in fits_files:
    # Open the FITS file
    hdul = fits.open(os.path.join(directory, fits_file))

    # Print the number of FFIs (HDUs) in the file
    print(f"Number of FFIs in {fits_file}: {len(hdul)}")

    # For each FFI (HDU) in the file
    for hdu in hdul:
        # Get the time the image was taken from the header
        time = hdu.header.get('DATE-OBS')

        # If the time is not available, skip this image
        if time is None:
            continue

        # Convert the time to a datetime object
        dt = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")

        # Convert the datetime object to a more classic format
        classic_time = dt.strftime("%I:%M:%S %p on %B %d, %Y")

        # Print the time the image was taken
        print(f"Image taken at: {classic_time}")

    # Close the FITS file
    hdul.close()