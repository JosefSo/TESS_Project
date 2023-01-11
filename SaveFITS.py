from lightkurve import search_lightcurve
import matplotlib.pyplot as plt


lc = search_lightcurve('KIC 757076', author="Kepler", quarter=3).download()
lc = lc.remove_nans()
# lc = lc.remove_outliers()  # This is not working
lc.scatter()

#lc.plot()

lc.to_fits(path='demo-lightcurve.fits', overwrite=True)

plt.show()
