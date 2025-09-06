#Thermal TIFF Utilities
import torch
from torchvision import transforms
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt


def tiff_single_info(input_image_path, print_flag):
    # Open the image file
    with Image.open(input_image_path) as image:
        tiff = transforms.ToTensor()(image)
        tiff_rounded = tiff.floor()
        unique_list = tiff_rounded.unique()
        nUnique = len(unique_list)
        if print_flag:
            print(f'Image {input_image_path} Shape : {tiff.shape}')
            print(f'Number of {input_image_path} Unique Classes (after rounding): {nUnique}')
        return unique_list

def tiff_max_min(input_folder):
    image_filenames = os.listdir(input_folder)
    image_filenames.sort()
    
    i = 1
    MAX = 0
    MIN = 0
    for filename in image_filenames:
        if filename.endswith(('.TIFF', '.tiff')):
            with Image.open(os.path.join(input_folder, filename)) as image:
                tiff = transforms.ToTensor()(image)
                tiff_rounded = tiff.floor()
                tempMax = torch.max(tiff_rounded)
                tempMin = torch.min(tiff_rounded)

                if tempMax > MAX:
                    MAX = tempMax 
                if tempMin < MIN:
                    MIN = tempMin

                if i == 1:
                    print(f'Number of Images Processed : {i}')
                if i % 50 == 0:
                    print(f'Number of Images Processed : {i}')
                i += 1
    return MAX, MIN  


'''
Function that will take in an input folder and resize all images in that folder to the specified
dimensions
'''
def tiff_resize_images(input_folder, output_folder, height, width):
    image_filenames = os.listdir(input_folder)
    image_filenames.sort()
    print(f'Grabbing images from: {input_folder}')
    print(f'Saving images to: {output_folder}')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    idx = 1
    for filename in image_filenames:
        if filename.endswith(('.jpg', '.JPG', '.jpeg', '.JPEG')):
            with Image.open(os.path.join(input_folder, filename)) as image:
                #resize image according to params
                image_resized = image.resize((width, height))
                #save resized image in specified output directory
                image_resized.save(os.path.join(output_folder, filename))                
        elif filename.endswith(('.TIFF', '.tiff')):
            with Image.open(os.path.join(input_folder, filename)) as image:
                #resize image according to params
                image_resized = image.resize((width, height))
                #save resized image in specified output directory
                image_resized.save(os.path.join(output_folder, filename)) 
                  
        if idx == 1:
            print(f'Number of Images Processed : {idx}')
        if idx % 50 == 0:
            print(f'Number of Images Processed : {idx}')
        idx += 1
    return None



def tiff_binary_image_convert(input_image_path, output_image_path, thresh, saveImage):
    # Open the TIFF image
    image = Image.open(input_image_path)
    
    # Convert image to numpy array
    image_array = np.array(image)
    
    #index through image pixels
    for i in range(image_array.shape[0]):  # Iterate over rows
        for j in range(image_array.shape[1]):  # Iterate over columns
            pixel = image_array[i, j]  
            # Binary thresholding
            if pixel > thresh:
                image_array[i, j] = 255  # Set pixel to white (255)
            else:
                image_array[i, j] = 0  # Set pixel to black (0)
    
    #tiff_bin_image = Image.fromarray(image_array)
    tiff_bin_image = Image.fromarray(image_array.astype('uint8'))
    
    # Save the binary image if specified
    if saveImage:
        tiff_bin_image.save(output_image_path + '_' + str(thresh) + '.jpg')
     
    return tiff_bin_image


'''
Function that will take in an input folder of TIFFs and convert all of the images in that folder to 
a binary image based on the threshold (in Celsius)
'''
def tiff_binary_folder_convert(input_folder, output_folder, thresh):
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
                        if pixel > thresh:
                            image_array[i, j] = 255  # Set pixel to white (255)
                        else:
                            image_array[i, j] = 0  # Set pixel to black (0)

                #tiff_bin_image = Image.fromarray(image_array)
                tiff_bin_image = Image.fromarray(image_array.astype('uint8'))
                
                #remove .TIFF extension and grab just the filename 
                filename_no_ext = os.path.splitext(filename)[0]
                
                # Save the binary image 
                tiff_bin_image.save(os.path.join(output_folder, filename_no_ext) + '.jpg')
        
        if idx == 1:
            print(f'Number of Images Processed : {idx}')
        if idx % 50 == 0:
            print(f'Number of Images Processed : {idx}')
        idx += 1
    return None

# function to convert TIFF to greyscale, save it if necessary, and display it
def tiff_convert_to_greyscale(input_image_path, output_image_path, display=True, saveImage=True):    
    
    # Open the image file
    with Image.open(input_image_path) as image:
        # Convert the image to a PyTorch tensor
        tiff = transforms.ToTensor()(image)
        
        # Convert the RGB tensor to grayscale using torchvision's Grayscale transform
        transform = transforms.Grayscale()
        tiff_grey = transform(tiff)
        
        # Convert the grayscale tensor back to a PIL image for display
        tiff_grey_image = transforms.ToPILImage()(tiff_grey)
        
        if display:
            plt.imshow(tiff_grey_image)
            plt.axis('off')
            plt.show()
            #tiff_grey_image.show()
                
        if saveImage:
            # Save the grayscale image
            tiff_grey_image.save(output_image_path)

    
        return tiff_grey_image