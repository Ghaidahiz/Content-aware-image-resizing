# Content-Aware Image Resizing

## Overview
Content-aware image resizing is a sophisticated technique that allows for the dynamic scaling of images. Unlike standard resizing methods, which simply distort images, this technique preserves important visual content while intelligently changing the size of the image. This is particularly useful for web design and other applications where image fit and quality are paramount.

## Key Features
- **Intelligent Resizing**: The algorithm focuses on preserving critical parts of the image while removing or altering less important areas.
- **Seam Carving**: This technique is a key feature, allowing for non-linear resizing by removing seams of pixels in a way that minimizes visual distortion.
- **User Input**: Users can select areas of the image they want to keep or remove, giving them control over the final output.

## Getting Started
To get started with the content-aware image resizing project, follow these steps:

### Prerequisites
- Python 3.x
- Required Libraries:
  - NumPy
  - OpenCV

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Ghaidahiz/Content-aware-image-resizing.git
   cd Content-aware-image-resizing
   ```
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
To use the image resizing functionality, run the following command:
```bash
python resize.py [options]
```

### Options:
- `-input <filepath>`: Path to the input image file.
- `-output <filepath>`: Path to save the resized image.
- `-width <width>`: Desired width for the output image.
- `-height <height>`: Desired height for the output image.

## Example
```bash
python resize.py -input my_image.jpg -output resized_image.jpg -width 800 -height 600
```

## Contributing
We welcome contributions to improve the content-aware image resizing project. Please follow these steps:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Special thanks to the researchers who developed the algorithms behind content-aware resizing.
- Thanks to the open-source community for providing valuable libraries that made this project possible.