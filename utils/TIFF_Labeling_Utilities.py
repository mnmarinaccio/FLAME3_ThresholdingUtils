import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def rangeLabel(tiffSampleArray, fireBoundaries, fire_rows, fire_cols, fire_values, height, width, labelTolerance=0.3):
    labels = []
    tolerance = labelTolerance
    # Go through each fire region value and label
    for val in fire_values:
        labeled = False
        for i in range(len(fireBoundaries) - 1):
            lowerBound = fireBoundaries[i]
            upperBound = fireBoundaries[i + 1]

            # For the last boundary, include the upper bound + a tolerance
            if i == len(fireBoundaries) - 2:
                if lowerBound <= val <= (upperBound + tolerance):
                    labels.append(i + 1)
                    labeled = True
                    break
            # For all other boundaries, exclude the upper bound
            else:
                if (lowerBound-tolerance) <= val < upperBound:
                    labels.append(i + 1)
                    labeled = True
                    break 
        
        if not labeled:
            #labels.append(0)
            print(f'Value {val} was not labeled within the boundaries!')
            
    # modify the original array with the label
    for row, col, label  in zip(fire_rows, fire_cols, labels):
        if label > len(fireBoundaries) - 1 or label < 0:  # Ensure no label exceeds number of classes
            print(f'Error: Label {label} for pixel ({row}, {col}) exceeds the number of classes!')
            #label = 0
        tiffSampleArray[row, col] = label
        #print(f'LABEL FOR ({row}, {col}) = {label}')
        
          
    # assign all non labeled pixels to be 0 (background)
    # Create all possible indices
    all_indices = {(r, c) for r in range(height) for c in range(width)}

    # Create the set of fire indices
    fire_indices = set(zip(fire_rows, fire_cols))

    # Find the indices that are not in fire_indices
    non_fire_indices = all_indices - fire_indices

    # Label non-fire indices as 0 (background)
    for row, col in non_fire_indices:
        tiffSampleArray[row, col] = 0
    
    
    return tiffSampleArray
    

def divideRange(fireValues, num_classes, decimal_places=14, verbose=False):
    minFire = np.amin(fireValues)
    maxFire = np.amax(fireValues)
    rangeFire = maxFire - minFire
    intervalFire = (rangeFire) / num_classes
    
    if verbose:
        print()
        print(f'FIRE REGION DATA')
        print(f'MIN FIRE = {minFire}')
        print(f'MAX FIRE = {maxFire}')
        print(f'RANGE FIRE = {rangeFire}')
        print(f'FIRE INTERVAL = {intervalFire}')
    boundaries = [round(minFire + i * intervalFire, decimal_places) for i in range(num_classes + 1)]
    return boundaries
    
def labelTiff(tiffSamplePath, tiffBinaryPath, num_classes, height, width, verbose=False):
    
    print(f'Labeling {tiffSamplePath}')
    # open image
    tiffSample = Image.open(tiffSamplePath)
    tiffBinary = Image.open(tiffBinaryPath)
    # convert to numpy array 
    tiffSampleArray = np.array(tiffSample)
    tiffBinaryArray = np.array(tiffBinary)

    if verbose:
        print()
        print(f'TIFF FULL IMAGE DATA')
        print(f'SHAPE: {tiffSampleArray.shape}')
        print(f'ABSOLUTE MIN VALUE: {np.amin(tiffSampleArray)}')
        print(f'ABSOLUTE MAX VALUE: {np.amax(tiffSampleArray)}')
        print(f'SHAPE: {tiffBinaryArray.shape}')
        print(f'ABSOLUTE MIN VALUE: {np.amin(tiffBinaryArray)}')
        print(f'ABSOLUTE MAX VALUE: {np.amax(tiffBinaryArray)}')
    
    # find locations of fire based on thresholded image
    fire_indices = np.where(tiffBinaryArray == 255)
    fire_rows = fire_indices[0]
    fire_cols = fire_indices[1]
    
    fireValuesList = []

    # Iterate over the indices using zip to pair the rows and columns correctly
    for row, col in zip(fire_rows, fire_cols):
        fireValuesList.append(tiffSampleArray[row, col])

    # Convert the list to a NumPy array at the end
    fireValues = np.array(fireValuesList)
    
    # determine range boundaries for classes
    fireBoundaries = divideRange(fireValues, num_classes)
    if verbose:
        print(f'FIRE RANGES = {fireBoundaries}')
    
    tiffSampleArray = rangeLabel(tiffSampleArray, fireBoundaries, fire_rows, fire_cols, fireValues, height, width)
    if verbose:
        print()
    return tiffSampleArray

def apply_colormap_and_save(input_filename, output_filename, num_classes):
    # Load the labeled PNG image as a NumPy array
    labeled_image = np.array(Image.open(input_filename))

    # Define a colormap with a specific number of classes
    # Create a custom colormap with black for background and other colors for classes
    cmap = plt.get_cmap('inferno', num_classes)  # 'tab20' is a good categorical colormap with up to 20 colors
    colors = cmap(np.arange(num_classes))
    
    # Ensure the background (value 0) is black
    colors[0] = [0, 0, 0, 1]  # RGBA: Black
    
    # Create a colormap from the colors
    custom_cmap = mcolors.ListedColormap(colors)
    
    # Apply the colormap directly
    color_mapped_image = custom_cmap(labeled_image)
    
    # Convert color-mapped image to 8-bit per channel image
    color_mapped_image = (color_mapped_image * 255).astype(np.uint8)
    
    # Convert to PIL Image and save
    output_image = Image.fromarray(color_mapped_image)
    output_image.save(output_filename)
    print(f'Colored and saved to {output_filename}')
 
    
def checkLabels(image_path, num_classes):
   
    # open image
    thermal_image = Image.open(image_path)
    # convert to numpy array 
    thermal_array = np.array(thermal_image)


    # print(f'SHAPE: {thermal_array.shape}')
    # print(f'ABSOLUTE MIN VALUE: {np.amin(thermal_array)}')
    # print(f'ABSOLUTE MAX VALUE: {np.amax(thermal_array)}')
    
    if np.amax(thermal_array) > num_classes or np.amin(thermal_array) != 0:
        print(f'{image_path} NOT LABELED PROPERLY')
    else:
        print(f'{image_path} LABELED CORRECTLY')
    #print(thermal_array)
    
    return thermal_array
    