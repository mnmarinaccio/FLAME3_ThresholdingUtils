# Documentation 


## Table of Contents
- [Documentation](#documentation)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [`OtsuUtils.py`](#otsuutilspy)
      - [Function: `otsu_threshold()` ](#function-otsu_threshold-)
      - [Function: `otsu_threshold_thermal()` ](#function-otsu_threshold_thermal-)
    - [`ThresholdingUtils.py`](#thresholdingutilspy)
      - [Function: `tiff_image_convert()` ](#function-tiff_image_convert-)
      - [Function: `tiff_folder_convert()` ](#function-tiff_folder_convert-)
    - [`TIFF_Utilities.py`](#tiff_utilitiespy)
      - [Function: `tiff_single_info()` ](#function-tiff_single_info-)
      - [Function: `tiff_max_min()` ](#function-tiff_max_min-)
      - [Function: `tiff_resize_images()` ](#function-tiff_resize_images-)
      - [Function: `tiff_binary_image_convert()` ](#function-tiff_binary_image_convert-)
      - [Function: `tiff_binary_folder_convert()` ](#function-tiff_binary_folder_convert-)
      - [Function: `tiff_convert_to_greyscale()` ](#function-tiff_convert_to_greyscale-)
    - [`TIFF_Labeling_Utilities.py`](#tiff_labeling_utilitiespy)
      - [Function: `rangeLabel()`](#function-rangelabel)
      - [Function: `divideRange()`](#function-dividerange)
      - [Function: `labelTiff()`](#function-labeltiff)
      - [Function: `apply_colormap_and_save()`](#function-apply_colormap_and_save)
      - [Function: `checkLabels()`](#function-checklabels)

  - [License](#license)

---

## Overview
### `OtsuUtils.py`

#### Function: `otsu_threshold()` <br /> 
`otsu_threshold(input_image_path, plotHist=False, printThresh=True)` <br /> 

Takes an image file, converts it to grayscale, and applies **Otsu’s Method** to automatically determine the optimal threshold for binarizing the image. It optionally displays a histogram of pixel values and prints the chosen threshold. The result is a black-and-white binary image where pixels are either set to **0 (black)** or **255 (white)**, depending on whether they are below or above the threshold.  

Arguments
- **`input_image_path`** *(str)*  
  Path to the input image file (TIFF, JPEG, PNG, etc.).  

- **`plotHist`** *(bool, default=False)*  
  If `True`, displays a histogram of grayscale pixel values before thresholding.  

- **`printThresh`** *(bool, default=True)*  
  If `True`, prints the computed optimal threshold value.  


Inputs
- **Type:** `str`  
- **Description:** File path to an image that can be opened by **PIL** (e.g., TIFF, PNG, JPEG).  


Outputs
- **`tiff_bin_image_final`** *(PIL.Image.Image)*  
  The binarized black-and-white image.  

- **`optimal_threshold`** *(int)*  
  The computed Otsu threshold value (0–255).  


---


#### Function: `otsu_threshold_thermal()` <br />

`otsu_threshold_thermal(input_image_path, plotHist=False, printThresh=True)` <br /> 
 
Takes a thermal JPEG image file, computes the histogram of pixel intensities, and applies **Otsu’s Method** to automatically determine the optimal threshold for binarizing the image. It optionally displays a histogram of pixel values and prints the chosen threshold. The result is a black-and-white binary image where pixels are either set to **0 (black)** or **255 (white)**, depending on whether they are below or above the threshold.  



Arguments
- **`input_image_path`** *(str)*  
  Path to the input thermal JPEG file.  

- **`plotHist`** *(bool, default=False)*  
  If `True`, displays a histogram of grayscale pixel values before thresholding.  

- **`printThresh`** *(bool, default=True)*  
  If `True`, prints the computed optimal threshold value.  


Inputs
- **Type:** `str`  
- **Description:** File path to an image that can be opened by **PIL** (e.g., JPEG).  


Outputs
- **`binarized_image_pil`** *(PIL.Image.Image)*  
  The binarized black-and-white image.  

- **`optimal_threshold`** *(int)*  
  The computed Otsu threshold value (0–255).  

---

### `ThresholdingUtils.py`
#### Function: `tiff_image_convert()` <br />

`tiff_image_convert(input_image_path, output_image_path, imageType, saveImage=True, thermal_image=None, low_threshold=50, high_threshold=150, binThresh=50, plotHist=False)` <br /> 

Converts a TIFF (or other supported image) into a binary ground truth for segmentation using one of three methods:  
1. **Standard Binary Thresholding** (simple intensity cutoff)  
2. **Hysteresis Thresholding** (edge detection with low/high thresholds)  
3. **Otsu’s Method** (automatic thresholding based on pixel intensity variance)  

The function supports saving the processed image to disk and allows method-specific parameters to be customized.  


Arguments  
- **`input_image_path`** *(str)*  
  Path to the input image file (TIFF, JPEG, PNG, etc.).  

- **`output_image_path`** *(str)*  
  Path prefix for saving the output binary image.  

- **`imageType`** *(str)*  
  Thresholding method to use:  
  - `'BINARY'` - Standard binary thresholding  
  - `'HYST'` - Hysteresis thresholding  
  - `'OTSU'` - Otsu’s Method  

- **`saveImage`** *(bool, default=True)*  
  If `True`, saves the resulting binary image to disk.  

- **`thermal_image`** *(bool, default=None)*  
  If `True` and `imageType='OTSU'`, uses the thermal image Otsu implementation.  

- **`low_threshold`** *(int, default=50)*  
  Lower cutoff for hysteresis thresholding (in intensity values).  

- **`high_threshold`** *(int, default=150)*  
  Upper cutoff for hysteresis thresholding (in intensity values).  

- **`binThresh`** *(int, default=50)*  
  Threshold value for standard binary thresholding (in intensity values).  

- **`plotHist`** *(bool, default=False)*  
  If `True`, plots the grayscale histogram when using Otsu’s Method.  


Inputs  
- **Type:** `str`  
- **Description:** File path to an image that can be opened by **PIL** (e.g., TIFF, PNG, JPEG).  


Outputs  
- **Binary Image** *(PIL.Image.Image or NumPy array)*  
  - For `'BINARY'` and `'OTSU'`: returns a **PIL.Image.Image** of the binarized image.  
  - For `'HYST'`: returns a **NumPy array** representing the hysteresis-thresholded image.  

- **Error Code** *(int)*  
  Returns `-1` if an invalid `imageType` is provided.  

---

#### Function: `tiff_folder_convert()` <br />

`tiff_folder_convert(input_folder, output_folder, imageType, thermal_image=None, low_threshold=50, high_threshold=150, binThresh=50, saveImage=True)` <br />

Converts a folder of TIFF (or supported) images into binary ground-truth segmentation masks using one of three thresholding techniques:  
1. **Standard Binary Thresholding**  
2. **Hysteresis Thresholding**  
3. **Otsu’s Method**  

It processes every image in the input folder, applies the chosen thresholding method, and saves the resulting binary images in the specified output folder.  
For Otsu’s method, the function also records threshold values into a CSV file and reports the mean threshold across all images.  


**Arguments**

- **`input_folder`** *(str)*  
  Path to the folder containing input images (TIFF, JPG, PNG supported depending on method).  

- **`output_folder`** *(str)*  
  Path to the folder where processed binary images will be saved.  

- **`imageType`** *(str)*  
  Thresholding method to use. Options:  
  - `"BINARY"` - Standard binary thresholding (fixed threshold).  
  - `"HYST"` - Hysteresis thresholding.  
  - `"OTSU"` - Otsu’s method.  

- **`thermal_image`** *(bool, optional, default=None)*  
  If `True` with `imageType="OTSU"`, applies thermal-image-specific Otsu thresholding (`otsu_threshold_thermal`).  

- **`low_threshold`** *(int, default=50)*  
  Lower threshold value (°C) for hysteresis method.  

- **`high_threshold`** *(int, default=150)*  
  Upper threshold value (°C) for hysteresis method.  

- **`binThresh`** *(int, default=50)*  
  Threshold (°C) for standard binary thresholding.  

- **`saveImage`** *(bool, default=True)*  
  If `True`, saves each processed image to the output folder.  


**Inputs**

- **Type:** `str` (folder paths)  
- **Description:**  
  Path to a folder containing images. Each image should be a TIFF for `"BINARY"` or `"HYST"` methods.  
  For `"OTSU"`, supported formats are TIFF, TIF, JPG, and JPEG.  


**Outputs**

- **Binary images saved to disk** *(TIFF format)* in the `output_folder`.  
- **Console logs** with the number of images processed.  
- **For Otsu’s method:**  
  - CSV file (`optimal_thresholds.csv`) with filename–threshold pairs.  
  - Mean optimal threshold value printed to console.  
- **Return value:** `None` (outputs are files and console logs).  

---

### `TIFF_Utilities.py`

#### Function: `tiff_single_info()` <br />  
`tiff_single_info(input_image_path, print_flag)` <br />  

Opens a TIFF (or other supported) image, converts it into a PyTorch tensor, and computes the **unique pixel values** after flooring (rounding down) the pixel intensities. Optionally prints the image shape and the number of unique pixel classes detected.  


**Arguments**  
- **`input_image_path`** *(str)*  
  Path to the input image file (TIFF, JPEG, PNG, etc.).  

- **`print_flag`** *(bool)*  
  If `True`, prints image shape and number of unique pixel classes after rounding.  


**Inputs**  
- **Type:** `str`  
- **Description:** File path to an image that can be opened by **PIL** and converted into a PyTorch tensor.  


**Outputs**  
- **`unique_list`** *(torch.Tensor)*  
  A tensor of the unique pixel values in the image (after flooring).  

- **Console Output (optional):**  
  If `print_flag=True`, prints:  
  - Image shape (tensor dimensions).  
  - Number of unique pixel classes in the image.  

---

#### Function: `tiff_max_min()` <br />  
`tiff_max_min(input_folder)` <br />  

Scans all TIFF images in a folder, converts each image to a PyTorch tensor, and computes the **maximum and minimum pixel values** across all images. Prints progress every 50 images processed.  


**Arguments**  
- **`input_folder`** *(str)*  
  Path to the folder containing input TIFF images.  


**Inputs**  
- **Type:** `str`  
- **Description:** Folder path containing images that can be opened by **PIL** and converted into PyTorch tensors.  


**Outputs**  
- **`MAX`** *(torch.Tensor / float)*  
  The maximum pixel value found across all images in the folder.  

- **`MIN`** *(torch.Tensor / float)*  
  The minimum pixel value found across all images in the folder.  

- **Console Output:**  
  Prints the number of images processed at the first image and every 50 images thereafter.  

---

#### Function: `tiff_resize_images()` <br />  
`tiff_resize_images(input_folder, output_folder, height, width)` <br />  

Resizes all images in a specified folder (TIFF, JPG, JPEG) to the given height and width, and saves them to an output folder. Prints progress for the first image and every 50 images processed.  


**Arguments**  
- **`input_folder`** *(str)*  
  Path to the folder containing the input images.  

- **`output_folder`** *(str)*  
  Path to the folder where resized images will be saved.  

- **`height`** *(int)*  
  Desired height (in pixels) for the resized images.  

- **`width`** *(int)*  
  Desired width (in pixels) for the resized images.  


**Inputs**  
- **Type:** `str` (folder paths)  
- **Description:** Folder containing images in TIFF, JPG, or JPEG format.  


**Outputs**  
- **Resized images saved to disk** in the `output_folder`.  
- **Return value:** `None`  
- **Console Output:**  
  Prints the number of images processed for the first image and every 50 images thereafter.  

---

#### Function: `tiff_binary_image_convert()` <br />  
`tiff_binary_image_convert(input_image_path, output_image_path, thresh, saveImage)` <br />  

Converts a single image into a **binary image** based on a specified threshold. Pixels with values above the threshold are set to **255 (white)**, and pixels below are set to **0 (black)**. Optionally saves the resulting binary image to disk.  


**Arguments**  
- **`input_image_path`** *(str)*  
  Path to the input image file (TIFF, JPEG, PNG, etc.).  

- **`output_image_path`** *(str)*  
  Path prefix for saving the output binary image.  

- **`thresh`** *(int)*  
  Threshold value for binary conversion.  

- **`saveImage`** *(bool)*  
  If `True`, saves the resulting binary image to disk.  


**Inputs**  
- **Type:** `str`  
- **Description:** File path to an image that can be opened by **PIL**.  


**Outputs**  
- **`tiff_bin_image`** *(PIL.Image.Image)*  
  The binarized black-and-white image.  

- **Return value:** `PIL.Image.Image`  
- **Console Output:** None  

---

#### Function: `tiff_binary_folder_convert()` <br />  
`tiff_binary_folder_convert(input_folder, output_folder, thresh)` <br />  

Converts all TIFF images in a folder into **binary images** using a specified threshold. Pixels above the threshold are set to **255 (white)**, and pixels below are set to **0 (black)**. Saves the resulting binary images to the specified output folder.  


**Arguments**  
- **`input_folder`** *(str)*  
  Path to the folder containing input TIFF images.  

- **`output_folder`** *(str)*  
  Path to the folder where processed binary images will be saved.  

- **`thresh`** *(int)*  
  Threshold value for binary conversion (e.g., in °C for thermal images).  


**Inputs**  
- **Type:** `str` (folder paths)  
- **Description:** Folder containing TIFF images to convert.  


**Outputs**  
- **Binary images saved to disk** *(JPEG format, same filename as input without extension)* in the `output_folder`.  
- **Return value:** `None`  
- **Console Output:**  
  Prints the number of images processed for the first image and every 50 images thereafter.  

---

#### Function: `tiff_convert_to_greyscale()` <br />  
`tiff_convert_to_greyscale(input_image_path, output_image_path, display=True, saveImage=True)` <br />  

Converts a TIFF (or other supported) image to **grayscale**, optionally displays it, and optionally saves it to disk. The function uses PyTorch tensors for the conversion and then converts back to a PIL image for display or saving.  

**Arguments**  
- **`input_image_path`** *(str)*  
  Path to the input image file (TIFF, JPEG, PNG, etc.).  

- **`output_image_path`** *(str)*  
  Path to save the grayscale image.  

- **`display`** *(bool, default=True)*  
  If `True`, displays the grayscale image using matplotlib.  

- **`saveImage`** *(bool, default=True)*  
  If `True`, saves the resulting grayscale image to disk.  


**Inputs**  
- **Type:** `str`  
- **Description:** File path to an image that can be opened by **PIL** and converted into a PyTorch tensor.  


**Outputs**  
- **`tiff_grey_image`** *(PIL.Image.Image)*  
  The resulting grayscale image.  

- **Return value:** `PIL.Image.Image`  
- **Console Output / Display:**  
  Optionally displays the grayscale image using matplotlib if `display=True`.  

---

### `TIFF_Labeling_Utilities.py`

#### Function: `rangeLabel()` <br />  
`rangeLabel(tiffSampleArray, fireBoundaries, fire_rows, fire_cols, fire_values, height, width, labelTolerance=0.3)` <br />  

Labels a thermal image array based on **predefined value ranges** and assigns class IDs to each pixel. Fire pixels are labeled according to the range they fall into, while all non-fire pixels are assigned the **background class (0)**. A tolerance can be specified to allow small deviations at the boundaries.  

Arguments
- **`tiffSampleArray`** *(np.ndarray)*  
  The original image array (height × width) containing pixel values to be labeled.  

- **`fireBoundaries`** *(list of float)*  
  List of numeric boundaries defining the class ranges for labeling. Length should be `num_classes + 1`.  

- **`fire_rows`** *(np.ndarray or list)*  
  Row indices of the fire pixels (typically obtained from a thresholded binary image).  

- **`fire_cols`** *(np.ndarray or list)*  
  Column indices of the fire pixels.  

- **`fire_values`** *(np.ndarray or list)*  
  The corresponding pixel values of the fire pixels used to determine the class label.  

- **`height`** *(int)*  
  Height of the full image.  

- **`width`** *(int)*  
  Width of the full image.  

- **`labelTolerance`** *(float, default=0.3)*  
  Optional tolerance added to the upper boundary of the last class to ensure edge values are included.  

Inputs
- **Type:** `np.ndarray`, `list`, `float`, `int`  
- **Description:** The function operates on the image array and pixel indices, using numeric ranges to assign class labels.  

Outputs
- **`tiffSampleArray`** *(np.ndarray)*  
  The labeled image array with class IDs:  
  - Fire pixels are assigned labels `1…num_classes` according to their value ranges.  
  - All other pixels are assigned `0` (background).  

Notes
- Prints a warning if a value does not fall within any range.  
- Prints an error if a computed label exceeds the number of classes.

---

#### Function: `divideRange()` <br />  
`divideRange(fireValues, num_classes, decimal_places=14, verbose=False)` <br />  

Divides a set of fire pixel values into **evenly spaced class ranges** for labeling. Computes the minimum, maximum, and interval, then generates a list of boundaries to be used for assigning class IDs.  

Arguments
- **`fireValues`** *(np.ndarray or list)*  
  Array or list of pixel values representing fire regions in the image.  

- **`num_classes`** *(int)*  
  Number of classes to divide the fire values into.  

- **`decimal_places`** *(int, default=14)*  
  Number of decimal places to round the computed boundaries.  

- **`verbose`** *(bool, default=False)*  
  If `True`, prints detailed information about min, max, range, and interval of fire values.  

Inputs
- **Type:** `np.ndarray`, `list`, `int`, `bool`  
- **Description:** The function takes the pixel values of fire regions and calculates numeric boundaries for class labels.  

Outputs
- **`boundaries`** *(list of float)*  
  A list of `num_classes + 1` numeric boundaries representing the intervals for each class.  

Notes
- The boundaries are **evenly spaced** from the minimum to the maximum fire value.  
- Can be used in combination with `rangeLabel()` to assign class IDs to each pixel.

---

#### Function: `labelTiff()` <br />  
`labelTiff(tiffSamplePath, tiffBinaryPath, num_classes, height, width, labelTolerance=0.3, verbose=False)` <br />  

Labels a TIFF image based on pixel intensity ranges and a thresholded binary mask. Combines `divideRange()` and `rangeLabel()` to assign class IDs to fire pixels while assigning **0 to non-fire pixels**.  

Arguments
- **`tiffSamplePath`** *(str)*  
  Path to the TIFF image containing the raw thermal or intensity values.  

- **`tiffBinaryPath`** *(str)*  
  Path to the thresholded binary TIFF image indicating fire pixels (255 for fire, 0 for background).  

- **`num_classes`** *(int)*  
  Number of classes (including fire intensity ranges) to label the fire pixels.  

- **`height`** *(int)*  
  Height of the full image.  

- **`width`** *(int)*  
  Width of the full image.  

- **`labelTolerance`** *(float, default=0.3)*  
  Tolerance added to the upper boundary of the last class to ensure edge values are included.  

- **`verbose`** *(bool, default=False)*  
  If `True`, prints detailed information about image shape, min/max values, and fire boundaries.  

Inputs
- **Type:** `str`, `int`, `float`, `bool`  
- **Description:** The function reads the sample and binary TIFF images, determines fire pixel locations, and calculates class boundaries for labeling.  

Outputs
- **`tiffSampleArray`** *(np.ndarray)*  
  A labeled image array of the same size as the input TIFF:  
  - Fire pixels are assigned integer class IDs `1…num_classes` according to their intensity ranges.  
  - Non-fire pixels are assigned `0` (background).  

Notes
- Internally calls `divideRange()` to compute class boundaries.  
- Internally calls `rangeLabel()` to assign labels based on the boundaries.  
- Prints warnings for any fire pixel values that do not fit into a class range.

---

#### Function: `apply_colormap_and_save()` <br />
`apply_colormap_and_save(input_filename, output_filename, num_classes)` <br />

Applies a **consistent color mapping** to a labeled image and saves it as a colored PNG. Ensures that the **same class ID always maps to the same color**, with the background (class 0) set to black.  

Arguments
- **`input_filename`** *(str)*  
  Path to the labeled input image (PNG) containing integer class IDs from 0 to `num_classes - 1`.  

- **`output_filename`** *(str)*  
  Path where the resulting colored PNG will be saved.  

- **`num_classes`** *(int)*  
  Total number of classes, including the background class (0).  

Inputs
- **Type:** `str`, `int`  
- **Description:** The function reads a labeled PNG image where pixel values indicate class IDs.  

Outputs
- **Colored PNG file** saved to `output_filename`  
  - Each pixel’s class ID is mapped to a consistent color.  
  - The output image is in **RGBA format**, with the background class (0) as black.  

Notes
- Can be used on a **single image or a batch of images**, producing consistent coloring across all outputs.  
- Uses `matplotlib`’s colormaps internally to assign colors.

---

#### Function: `checkLabels()` <br />  
`checkLabels(image_path, num_classes)` <br />  

Verifies that a labeled image contains valid class IDs within the expected range. Checks that all pixel values are between **0** (background) and `num_classes` (inclusive) and prints a message indicating whether the image is labeled correctly.  

Arguments
- **`image_path`** *(str)*  
  Path to the labeled image (PNG or TIFF) to be checked.  

- **`num_classes`** *(int)*  
  Total number of classes (including the background class 0).  

Inputs
- **Type:** `str`, `int`  
- **Description:** The function reads the labeled image and converts it to a NumPy array for validation.  

Outputs
- **`thermal_array`** *(np.ndarray)*  
  The NumPy array representation of the labeled image.  

Notes
- Prints `LABELED CORRECTLY` if all pixel values are in `0…num_classes`.  
- Prints `NOT LABELED PROPERLY` if any pixel value falls outside this range.  
- Can be used as a **sanity check** after labeling or applying a colormap.

---


## License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.
