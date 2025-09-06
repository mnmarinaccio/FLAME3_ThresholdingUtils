# FLAME 3 - Wildfire Thresholding Utilities

This repository contains utilities and Jupyter Notebook examples, which can be used for leveraging the radiometric TIFF data and Thermal JPG imagery included in the aerial (drone-collected) multispectral wildfire imagery dataset, [FLAME 3](https://ieee-dataport.org/open-access/flame-3-radiometric-thermal-uav-imagery-wildfire-management), based on the [FLAME 3 Paper](https://arxiv.org/abs/2412.02831). The tools found in this repository are implementations of different thresholding techniques, but also include some supplemental functions for handling the radiometric TIFF data.

These tools were developed by [Michael Marinaccio](https://github.com/mnmarinaccio) and used for work from the [SAM-TIFF Paper](https://arxiv.org/abs/2505.01638). The implementation for SAM-TIFF is found [here](https://arxiv.org/abs/2505.01638).

<p align="center">
  <img src="readme_images/imgoriginal.PNG" alt="Paired RGB and Thermal Image" />
</p>
<p align="center">
  <img src="readme_images/imgbinary.PNG" alt="Thresholded Images" />
</p>

---

## Table of Contents
- [FLAME 3 - Wildfire Thresholding Utilities](#flame-3---wildfire-thresholding-utilities)
  - [Table of Contents](#table-of-contents)
  - [Documentation](#documentation)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

---

## Documentation
Please refer to the documentation, found [here](/Documentation.md), for any syntax or code-related questions.

## Requirements
- matplotlib==3.7.5
- numpy==1.24.4
- Pillow==10.4.0
- scipy==1.10.0
- scikit-image==0.21.0
- torch==2.4.1
- torchvision==0.19.1


## Installation
git clone https://github.com/mnmarinaccio/FLAME3_ThresholdingUtils.git <br />
cd ThresholdingUtils

You can install the dependencies with: <br />
pip install -r requirements.txt

## Usage
For the examples, open the notebook in Jupyter and run all cells <br />
jupyter notebook ThresholdingUtilsUsage.ipynb

For using the FLAME 3 Thresholding Utilities package, please import from the utils folder.

from utils.OtsuUtils import * <br />
from utils.ThresholdingUtils import * <br />
from utils.TIFF_Utilities import * <br />

## License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.
