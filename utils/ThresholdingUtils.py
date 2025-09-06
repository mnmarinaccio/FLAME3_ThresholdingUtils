import torch
from torchvision import transforms
from PIL import Image
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from skimage import data, color
import sys
from scipy.signal import convolve2d
from utils.OtsuUtils import otsu_threshold, otsu_threshold_thermal
'''
Convert TIFF file into appropriate binary ground truth for segmentation based on one of the following methods:

1.) Standard Binary Thresholding
2.) Hysteresis
3.) Otsu's Method 

Required Parameters
    -input_image_path = string path to input image filename
    -output_image_path = string path to output image filename
    -imageType = can be 'BINARY', 'HYST', or 'OTSU' to specify which thresholding technique to use
    -saveImage = If True, then the image will be saved, if False, then the image will not be saved

Optional Parameters
Standard Binary Parameters:
    -binThresh = Default is 50 (in degrees Celsius) if not specified
    
Hysteresis Parameters:
    -low_threshold = Default is 50 (in degrees Celsius) if not specified
    -high_threshold = Default is 150 (in degrees Celsius) if not specified
    
Otsu Parameters:
    -plotHist = If True, then the pixel intensity histogram will be plotted, if False, then the image the 
                pixel intensity histogram will not be plotted, default is set to False
'''
def tiff_image_convert(input_image_path, output_image_path, imageType, saveImage=True, thermal_image=None, low_threshold=50, high_threshold=150, binThresh=50, plotHist=False):
    tiff_bin_image = None
    tiff_grey_image = None
    
    if imageType == 'BINARY':
        # Open the TIFF image
        image = Image.open(input_image_path)

        # Convert image to numpy array
        image_array = np.array(image)
        
        #index through image pixels
        for i in range(image_array.shape[0]):  # Iterate over rows
            for j in range(image_array.shape[1]):  # Iterate over columns
                pixel = image_array[i, j]  
                # Binary thresholding
                if pixel > binThresh:
                    image_array[i, j] = 255  # Set pixel to white (255)
                else:
                    image_array[i, j] = 0  # Set pixel to black (0)

        #tiff_bin_image = Image.fromarray(image_array)
        tiff_bin_image = Image.fromarray(image_array.astype('uint8'))
    
    
        # Save the binary image if specified
        if saveImage:
            saveString = output_image_path + '_' + str(binThresh) + '.TIFF'
            tiff_bin_image.save(saveString)
            print(f'Image Saved in {saveString}')
        return tiff_bin_image
    elif imageType == 'HYST':
        # Open the image file
        with Image.open(input_image_path) as image:
            # Convert the image to a PyTorch tensor
            tiff = transforms.ToTensor()(image)

            # Convert the RGB tensor to grayscale using torchvision's Grayscale transform
            transform = transforms.Grayscale()
            tiff_grey = transform(tiff)

            #convert to numpy array and get rid of 0th channel dimension
            tiff_grey_numpy = tiff_grey[0].numpy()

            #--------------START HYSTERESIS THRESHOLDING--------------------------
            print(f'Hysteresis Thresholds -> Low: {low_threshold}, High: {high_threshold}')
             # Smooth the image using Gaussian filter
            smoothed_image = gaussian_filter(tiff_grey_numpy, sigma=1)

            
            # Apply gradient calculation (Sobel operator)
            sobelx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            sobely = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])


            gradient_x = convolve2d(smoothed_image, sobelx, mode='same')
            gradient_y = convolve2d(smoothed_image, sobely, mode='same')
            

            # Compute gradient magnitude and direction
            gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
            gradient_direction = np.arctan2(gradient_y, gradient_x)

            # Initialize output image
            output_image = np.zeros_like(tiff_grey_numpy)

            # Apply hysteresis thresholding
            strong_edge = (gradient_magnitude > high_threshold)
            weak_edge = (gradient_magnitude >= low_threshold) & (gradient_magnitude <= high_threshold)

            output_image[strong_edge] = 255
            for i in range(1, output_image.shape[0]-1):
                for j in range(1, output_image.shape[1]-1):
                    if weak_edge[i, j]:
                        local_gradient = gradient_direction[i-1:i+2, j-1:j+2]
                        local_magnitude = gradient_magnitude[i-1:i+2, j-1:j+2]
                        adjacent_pixels = local_magnitude > low_threshold
                        if np.any(adjacent_pixels):
                            output_image[i, j] = 255
            #--------------END HYSTERESIS THRESHOLDING--------------------------
            
            tiff_hyst_image = Image.fromarray(output_image.astype('uint8'))
    
            # Save the output grayscale image
            if saveImage:
                saveString = output_image_path + '.TIFF'
                tiff_hyst_image.save(saveString)
                #plt.imsave(saveString, output_image, cmap='gray')
                print(f'Image Saved in {saveString}')
        return output_image

    elif imageType == 'OTSU':
        if thermal_image == True:
            tiff_otsu_image, optimal_threshold = otsu_threshold_thermal(input_image_path, plotHist)
        else:
            tiff_otsu_image, optimal_threshold = otsu_threshold(input_image_path, plotHist)
         
        if saveImage: 
            # Save the binary image
            saveString = output_image_path + '_' + str(optimal_threshold) + '.TIFF'
            tiff_otsu_image.save(saveString)
            #plt.imsave(saveString, tiff_otsu_image, cmap='gray')
            print(f'Image Saved in {saveString}')
        return tiff_otsu_image        
        
    #if imageType is invalid return -1
    return -1


'''
Convert entire TIFF folder into appropriate binary ground truth for segmentation based on one of the following methods:

1.) Standard Binary Thresholding
2.) Hysteresis
3.) Otsu's Method 

Required Parameters
    -input_folder = string path to input image filename
    -output_folder = string path to output image filename
    -imageType = can be 'BINARY', 'HYST', or 'OTSU' to specify which thresholding technique to use

Optional Parameters
Standard Binary Parameters:
    -binThresh = Default is 50 (in degrees Celsius) if not specified
    
Hysteresis Parameters:
    -low_threshold = Default is 50 (in degrees Celsius) if not specified
    -high_threshold = Default is 150 (in degrees Celsius) if not specified
    
Otsu Parameters:
    -None
'''
def tiff_folder_convert(input_folder, output_folder, imageType, thermal_image=None, low_threshold=50, high_threshold=150, binThresh=50, saveImage=True):
    tiff_bin_image = None
    tiff_grey_image = None
    
    if imageType == 'BINARY':
        image_filenames = os.listdir(input_folder)
        image_filenames.sort()
        print(f'Grabbing images from: {input_folder}')
        print(f'Saving images to: {output_folder}')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        idx = 1
        for filename in image_filenames:
            if filename.endswith(('.tiff', '.TIFF')):
                with Image.open(os.path.join(input_folder, filename)) as image:
                    # Convert image to numpy array
                    image_array = np.array(image)

                    #index through image pixels
                    for i in range(image_array.shape[0]):  # Iterate over rows
                        for j in range(image_array.shape[1]):  # Iterate over columns
                            pixel = image_array[i, j]  
                            # Binary thresholding
                            if pixel > binThresh:
                                image_array[i, j] = 255  # Set pixel to white (255)
                            else:
                                image_array[i, j] = 0  # Set pixel to black (0)

                    tiff_bin_image = Image.fromarray(image_array.astype('uint8'))
                    
                    #remove .TIFF extension and grab just the filename 
                    filename_no_ext = os.path.splitext(filename)[0]
                    outputFolderName = os.path.join(output_folder, filename_no_ext) + '.TIFF'
                    # Save the binary image in the proper output folder
                    tiff_bin_image.save(outputFolderName)
                
            if idx == 1:
                print(f'Number of Images Processed : {idx}')
            if idx % 50 == 0:
                print(f'Number of Images Processed : {idx}')
            idx += 1
    elif imageType == 'HYST':
        image_filenames = os.listdir(input_folder)
        image_filenames.sort()
        print(f'Grabbing images from: {input_folder}')
        print(f'Saving images to: {output_folder}')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        idx = 1
        for filename in image_filenames:
            if filename.endswith(('.tiff', '.TIFF')):
                with Image.open(os.path.join(input_folder, filename)) as image:
                    # Convert the image to a PyTorch tensor
                    tiff = transforms.ToTensor()(image)

                    # Convert the RGB tensor to grayscale using torchvision's Grayscale transform
                    transform = transforms.Grayscale()
                    tiff_grey = transform(tiff)

                    #convert to numpy array and get rid of 0th channel dimension
                    tiff_grey_numpy = tiff_grey[0].numpy()

                    #--------------START HYSTERESIS THRESHOLDING--------------------------
                    #print(f'Hysteresis Thresholds -> Low: {low_threshold}, High: {high_threshold}')
                     # Smooth the image using Gaussian filter
                    smoothed_image = gaussian_filter(tiff_grey_numpy, sigma=1)


                    # Apply gradient calculation (Sobel operator)
                    sobelx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
                    sobely = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])


                    gradient_x = convolve2d(smoothed_image, sobelx, mode='same')
                    gradient_y = convolve2d(smoothed_image, sobely, mode='same')


                    # Compute gradient magnitude and direction
                    gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
                    gradient_direction = np.arctan2(gradient_y, gradient_x)

                    # Initialize output image
                    output_image = np.zeros_like(tiff_grey_numpy)

                    # Apply hysteresis thresholding
                    strong_edge = (gradient_magnitude > high_threshold)
                    weak_edge = (gradient_magnitude >= low_threshold) & (gradient_magnitude <= high_threshold)

                    output_image[strong_edge] = 255
                    for i in range(1, output_image.shape[0]-1):
                        for j in range(1, output_image.shape[1]-1):
                            if weak_edge[i, j]:
                                local_gradient = gradient_direction[i-1:i+2, j-1:j+2]
                                local_magnitude = gradient_magnitude[i-1:i+2, j-1:j+2]
                                adjacent_pixels = local_magnitude > low_threshold
                                if np.any(adjacent_pixels):
                                    output_image[i, j] = 255
                    #--------------END HYSTERESIS THRESHOLDING--------------------------

                    tiff_hyst_image = Image.fromarray(output_image.astype('uint8'))
                    
                    #remove .TIFF extension and grab just the filename 
                    filename_no_ext = os.path.splitext(filename)[0]
                    outputFolderName = os.path.join(output_folder, filename_no_ext) + '.TIFF'
                    # Save the binary image in the proper output folder
                    tiff_hyst_image.save(outputFolderName)
                    #plt.imsave(outputFolderName, output_image, cmap='gray')
                
            if idx == 1:
                print(f'Number of Images Processed : {idx}')
            if idx % 50 == 0:
                print(f'Number of Images Processed : {idx}')
            idx += 1
            
    elif imageType == 'OTSU':
        csv_data_save = []
        optimal_list = []
        image_filenames = os.listdir(input_folder)
        image_filenames.sort()
        print(f'Grabbing images from: {input_folder}')
        print(f'Saving images to: {output_folder}')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        idx = 1
        for filename in image_filenames:
            if filename.lower().endswith(('.tiff', '.tif', '.jpg', '.jpeg')):
                with Image.open(os.path.join(input_folder, filename)) as image:
                    if thermal_image == True:
                        tiff_otsu_image, optimal_threshold = otsu_threshold_thermal(os.path.join(input_folder, filename), plotHist=False, printThresh=False)
                    else:
                        tiff_otsu_image, optimal_threshold = otsu_threshold(os.path.join(input_folder,filename), plotHist=False, printThresh=False)
                    
                    
                    # save optimal threshold and filename to csv 
                    csv_data_save.append([filename, optimal_threshold])
                    
                    # save optimal threshold list for mean computation at end of function
                    optimal_list.append(optimal_threshold)
                    #remove .TIFF extension and grab just the filename 
                    filename_no_ext = os.path.splitext(filename)[0]
                    outputFolderName = os.path.join(output_folder, filename_no_ext) + '.TIFF'
                    if saveImage == True:
                        # Save the binary image in the proper output folder
                        tiff_otsu_image.save(outputFolderName)
                    #plt.imsave(outputFolderName, tiff_otsu_image, cmap='gray')  
            if idx == 1:
                print(f'Number of Images Processed : {idx}')
            if idx % 50 == 0:
                print(f'Number of Images Processed : {idx}')
            idx += 1
        mean_optimal = sum(optimal_list) / len(optimal_list)
        print(f'Mean Optimal Threshold = {mean_optimal}')
        
        # Write data to CSV
        with open(f'./{output_folder}/optimal_thresholds.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['Filename', 'Optimal Threshold'])
            # Write all the rows
            writer.writerows(csv_data_save)

        print(f'Data written to ./{output_folder}/optimal_thresholds.csv.')
    return None

