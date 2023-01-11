from astropy.io import fits
hdu = fits.open('demo-lightcurve.fits')
type(hdu)

print(hdu.info())

print("--------------------------------------------------------------------------------------------------")

# hdu is a set of astropy.io.fits objects, which is what we would expect.
# Lets take a look at the header of the first extension.

import pprint
pprint.pprint(hdu[0].header) # print beautiful

# print(hdu[0].header)