import torch
from torchvision import transforms
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, color
import sys
import torchvision.transforms as transforms

def otsu_threshold(input_image_path, plotHist=False, printThresh=True):
    with Image.open(input_image_path) as image:
        # Convert the image to a PyTorch tensor
        tiff = transforms.ToTensor()(image)
        # Convert the RGB tensor to grayscale using torchvision's Grayscale transform
        transform = transforms.Grayscale()
        tiff_grey = transform(tiff)

        # Convert to numpy array and get rid of 0th channel dimension
        tiff_grey_numpy = tiff_grey[0].numpy()
        tiff_grey_rounded = np.round(tiff_grey_numpy).astype(int)

        # Create histogram 
        hist, bins = np.histogram(tiff_grey_rounded.ravel(), bins=256, range=[0, 256])

        if plotHist == True:
            plt.figure(figsize=(8, 6))
            plt.hist(tiff_grey_rounded.ravel(), bins=256, range=[0, 256], color='blue', alpha=0.7)
            plt.title('Histogram of Rounded Grey TIFF Image')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.show()

        
        # Compute probabilities
        prob = hist.astype(np.float32) / np.sum(hist)

        # Compute the cumulative sum 
        cum_sum = np.cumsum(prob)
        cum_mean = np.cumsum(prob * np.arange(256))
        
        # Compute the between-class variance
        epsilon = np.finfo(float).eps  # Machine epsilon
        valid_indices = np.logical_and(cum_sum > 0, cum_sum < 1)
        between_class_variance = np.zeros_like(cum_mean)
        between_class_variance[valid_indices] = (cum_mean[-1] * cum_sum[valid_indices] - cum_mean[valid_indices])**2 / (cum_sum[valid_indices] * (1 - cum_sum[valid_indices]) + epsilon)

        # Compute the optimal threshold
        optimal_threshold = np.argmax(between_class_variance)
        if printThresh == True:
            print(f'Optimal Threshold Found = {optimal_threshold}')
  
        # Binarize the image using the optimal threshold
        #tiff_bin_image = (tiff_grey_numpy > optimal_threshold).astype(np.uint8)
        
        #index through image pixels
        for i in range(tiff_grey_numpy.shape[0]):  # Iterate over rows
            for j in range(tiff_grey_numpy.shape[1]):  # Iterate over columns
                pixel = tiff_grey_numpy[i, j]  
                # Binary thresholding
                if pixel > optimal_threshold:
                    tiff_grey_numpy[i, j] = 255  # Set pixel to white (255)
                else:
                    tiff_grey_numpy[i, j] = 0  # Set pixel to black (0)

        
        tiff_bin_image_final = Image.fromarray(tiff_grey_numpy.astype('uint8'))
        
    return tiff_bin_image_final, optimal_threshold




def otsu_threshold_thermal(input_image_path, plotHist=False, printThresh=True):
    # Load the image and convert it to grayscale
    with Image.open(input_image_path) as image:
        image_gray = image.convert("L")  # Convert to grayscale

        # Convert to NumPy array
        gray_array = np.array(image_gray, dtype=np.uint8)  

        # Compute histogram
        hist, bins = np.histogram(gray_array.ravel(), bins=256, range=[0, 256])

        if plotHist:
            plt.figure(figsize=(8, 6))
            plt.hist(gray_array.ravel(), bins=256, range=[0, 256], color='blue', alpha=0.7)
            plt.title('Histogram of Grayscale Thermal Image')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.show()

        # Compute probabilities
        prob = hist.astype(np.float32) / np.sum(hist)

        # Compute cumulative sum and mean
        cum_sum = np.cumsum(prob)
        cum_mean = np.cumsum(prob * np.arange(256))

        # Compute between-class variance
        epsilon = np.finfo(float).eps  # Machine epsilon to avoid division by zero
        valid_indices = np.logical_and(cum_sum > 0, cum_sum < 1)
        between_class_variance = np.zeros_like(cum_mean)
        between_class_variance[valid_indices] = (
            (cum_mean[-1] * cum_sum[valid_indices] - cum_mean[valid_indices]) ** 2 /
            (cum_sum[valid_indices] * (1 - cum_sum[valid_indices]) + epsilon)
        )

        # Compute the optimal threshold
        optimal_threshold = np.argmax(between_class_variance)
        if printThresh:
            print(f'Optimal Threshold Found = {optimal_threshold}')

        # Apply threshold to binarize the image
        binarized_image = (gray_array > optimal_threshold).astype(np.uint8) * 255

        # Convert back to PIL image
        binarized_image_pil = Image.fromarray(binarized_image)

    return binarized_image_pil, optimal_threshold


