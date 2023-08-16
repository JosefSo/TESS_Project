

import pandas as pd
import matplotlib.pyplot as plt
import glob

# Function to find the closest star in the table to the given coordinates
def closest_star(data, ra, dec):
    distances = ((data['ra'] - ra) ** 2 + (data['dec'] - dec) ** 2) ** 0.5
    return data.iloc[distances.idxmin()]

def create_lightcurve():

 # Get the RA of the star from the user
 star_ra = float(input("Please enter the RA (Right Ascension) of the star: "))

 # Get the Dec of the star from the user
 star_dec = float(input("Please enter the Dec (Declination) of the star: "))

# Initialize lists to store the flux and time data
 flux_data = []
 time_data = []

# Loop through all the CSV files
 csv_files = glob.glob('photometry_results/photometry_results_*.csv')
 for csv_file in csv_files:
     print(csv_file.title())

    # Load the data from the CSV file
     df = pd.read_csv(csv_file)

     # Find the star closest to the specified coordinates
     star = closest_star(df, star_ra, star_dec)

     print('MJD_OBS: ', star['MJD_OBS'])

     # Append the flux and time to the respective lists
     flux_data.append(star['flux'])
     time_data.append(star['MJD_OBS'])

# Plot the light curve of the star
 plt.figure(figsize=(10, 6))
 plt.plot(time_data, flux_data, '.')
 plt.title(f'Light Curve of Star at RA={star_ra}, Dec={star_dec}')
 plt.xlabel('MJD_OBS')
 plt.ylabel('Flux')
 plt.grid(True)

# Disable the offset on the x-axis
 plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)

 plt.show()