import cv2
import numpy as np


# Set file path and open image
file_path = r"HDR_Correction/images/hdr_test_ireland.jpg"
image_orig = cv2.imread(file_path)

# Test File Validity
""" if image is not None:
    # Image was loaded successfully
    print("Image loaded successfully!")
else:
    # Image loading failed
    print("Error: Unable to load image!") """

# Define row&column size (from image shape), centre, angle and preview downsize factor
rows, cols = image_orig.shape[:2]
center = (cols/2, rows/2)
angle = 90
preview_downscale = 0.1

# Define rotation matrix
matrix_rotate = cv2.getRotationMatrix2D(center, angle, 1) 

# Apply rotation trasnform
image_rotate = cv2.warpAffine(image_orig, matrix_rotate, (cols, rows))


# Prepare Preview Images
image_orig_small = cv2.resize(
    image_orig,
    (int(cols*preview_downscale),
     int(rows*preview_downscale))
     )
image_rotate_small = cv2.resize(
    image_rotate,
    (int(cols*preview_downscale),
     int(rows*preview_downscale))
     )

# Preview before and after images
cv2.imshow('Original Image', image_orig_small)
cv2.imshow('Rotated Image', image_rotate_small)
cv2.waitKey(0)

# Get rid of Windows
cv2.destroyAllWindows()




# Compute rotation matrix
M = cv2.getRotationMatrix2D(center, angle, 1)

# Apply rotation
rotated_img = cv2.warpAffine(img, M, (cols, rows))