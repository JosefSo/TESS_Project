import lightkurve as lk
import matplotlib.pyplot as plt

# lightkurve - Light Curve
# Light curve products: tables containing the measured flux at each observation time.
# Target pixel file products: stacks of images with the pixel-level observation at each observation time.
# HLSPs - High Level Science Products: a specific version of a data product produced by an analysis or photometry
# pipeline. Lightkurve has access to HLSP light curves produced by the photometry pipelines EVEREST, K2SFF, and K2SC.
# FFIs - Full Frame Images


# When using Lightkurve, we kindly request that you cite the following packages:
#
# lightkurve
# astropy
# astroquery — if you are using search_lightcurve() or search_targetpixelfile().
# tesscut — if you are using search_tesscut().

print("----------------------------------Searching for Light Curves ------------------------------------------------\n")

search_result = lk.search_lightcurve('KIC 3733346', author='Kepler')
# print(search_result)

print("--------------------------------------------------------------------------------------------------")

for column in search_result.table.columns:
    print(column)

print("--------------------------------------------------------------------------------------------------")

import numpy as np
quarter2_index = np.where(search_result.table['mission'] == 'Kepler Quarter 02')[0]
#print(search_result[quarter2_index])

print("--------------------------------------------------------------------------------------------------")

quarter2_index = np.where(search_result.table['author'] == 'Kepler')[0]
#print(search_result[quarter2_index])

print("--------------------------------------------------------------------------------------------------")

search_result_q2 = lk.search_lightcurve('KIC 3733346', author='Kepler', quarter=2)
#print(search_result_q2)

print("\n-------------------------------------- 2.1 Downloading a single light curve --------------------------------\n")
# A light curve can be downloaded by calling .download()
lc = search_result_q2.download()
# print(lc)
# lc.plot()
# plt.show()

print("--------------------------------------------------------------------------------------------------")
# search_result = lk.search_lightcurve("Kepler-8", author="Kepler", cadence="long")
# klc = search_result[4].download()
# print(klc)
# klc.plot()
# plt.show()

print("\n-------------------------------- 2.2 Downloading a collection of light curves -----------------------------\n")

lc_collection = search_result[:5].download_all()
print(lc_collection)


# Create a larger figure for clarity
fig, ax = plt.subplots(figsize=(20,5))
# Plot the light curve collection
lc_collection.plot(ax=ax)

# plt.show()

# NORMALIZATION - (Didn't work)
# fig, ax = plt.subplots(figsize=(20,5))
# for lc in lc_collection:
#   lc.normalize().plot(ax=ax, label=f'Quarter {lc.quarter}')

# plt.show()

print("\n-------------------------------- 3. Searching for Target Pixel Files -----------------------------\n")

search_result = lk.search_targetpixelfile('K2-199', exptime=1800)
print(search_result)

print("\n-------------------------------- 3.1 Downloading a single target pixel file -----------------------------\n")

# When you call download on a search result containing more than one entry, it will download only the first entry in
# the search result. Lightkurve will raise a friendly warning to let you know when this occurs.
tpf = search_result.download()
tpf.plot()


# turn the TPF into a light curve, there is a to_lightcurve method. - Didn't succeed
# lc = tpf.to_lightcurve()
# lc.plot()



print("\n------------------------- 3.2 Downloading a collection of target pixel files ------------------------\n")

tpf_collection = search_result.download_all()
print(tpf_collection)
tpf_collection.plot()



print("\n------------------------------ Searching for TESS Full Frame Image (FFI) Cutouts -----------------------\n")

search_result = lk.search_tesscut('Pi Men')
print(search_result)

tpf_cutout = search_result[0].download(cutout_size=10)
tpf_cutout.plot()

print("\n------------------------------ 5. Performing a Cone Search -----------------------\n")
# If you are interested in identifying a number of nearby targets, you can perform a cone search, which will
# return all available targets within a cone of a specfied radius on the sky. The radius can be either
# a float or an astropy.units.Quantity object.

search_result = lk.search_targetpixelfile('Trappist-1', radius=180., campaign=12, exptime=1800)
print(search_result)



# plt.show()