import glob
import os

import numpy as np
from tqdm import tqdm
import FFIDownloader as dffi
import FFICalibrate as cffi
import FFIStarFinder as sffi
import FFILcCreator as lffi


def print_options():

  dffi_desc = "Download FFI files for a given sector, date, etc."
  cffi_desc = "Calibrate FFI files by removing noise, hot pixels, etc."
  sffi_desc = "Find stars in calibrated FFI images."
  lffi_desc = "Create lightcurves for stars of interest."

  print(f"1) {dffi_desc}")
  print(f"2) {cffi_desc}")
  print(f"3) {sffi_desc}")
  print(f"4) {lffi_desc}")


def main():
    options = {
        "1": dffi.download_fits,
        "2": cffi.calibrate_background,
        "3": sffi.find_stars,
        "4": lffi.create_lightcurve
    }

    data_arrays, means, medians, stds = None, None, None, None
    is_complete = False
    fits_files = glob.glob('FITS/*.fits')


    while not is_complete:
        os.system('cls' if os.name == 'nt' else 'clear')  # clear screen
        print_options()
        selected = input("Select option (1-4): ")

        if selected in options:
            if selected == "1":
                inputs_str = input("Enter sector, year, day, camera, and CCD (comma-separated): ")
                sector, year, day, camera, ccd = inputs_str.split(',')

                inputs = {
                    'sector': sector.strip(),
                    'year': year.strip(),
                    'day': day.strip(),
                    'camera': camera.strip(),
                    'ccd': ccd.strip()
                }
                options[selected](inputs)

            elif selected == "2":
               options[selected](fits_files)

            elif selected == "3":

                save_path = 'calibrated_data'  # Directory where the files are saved

                data_arrays = np.load(os.path.join(save_path, 'data_arrays.npy'))
                means = np.load(os.path.join(save_path, 'means.npy'))
                medians = np.load(os.path.join(save_path, 'medians.npy'))
                stds = np.load(os.path.join(save_path, 'stds.npy'))

                options[selected](fits_files, data_arrays, means, medians, stds)
            elif selected == "4":
                options[selected]()
        else:
            is_complete = True


if __name__ == "__main__":
    main()
