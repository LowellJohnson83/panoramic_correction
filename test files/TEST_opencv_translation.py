import cv2
import numpy as np


# Set file path and open image
file_path = r"Panoramic_Correction/images/hdr_test_ireland.jpg"
# print(file_path)
image_orig = cv2.imread(file_path)


# Test File Validity
if image_orig is not None:
    # Image was loaded successfully
    print("Image loaded successfully!")
else:
    # Image loading failed
    print("Error: Unable to load image!")





# Define row&column size (from image shape), shiftx/shifty and preview downsize factor
rows, cols = image_orig.shape[:2]
dx, dy = 2000, 800
preview_downscale = 0.1

print(rows, cols)

# Define translation matrix
matrix_trans = np.float32([[1, 0, dx], [0, 1, dy]])

# Apply translation trasnform
image_trans = cv2.warpAffine(image_orig, matrix_trans, (cols, rows))


# Prepare Preview Images (Original AND Transfformed one)
image_orig_small = cv2.resize(
    image_orig,
    (int(cols*preview_downscale),
     int(rows*preview_downscale))
     )
image_trans_small = cv2.resize(
    image_trans,
    (int(cols*preview_downscale),
     int(rows*preview_downscale))
     )

# Preview before and after images (Original and Transformed )
cv2.imshow('Original Image', image_orig_small)
cv2.imshow('Translated Image', image_trans_small)
cv2.waitKey(0)

# Get rid of Windows
cv2.destroyAllWindows()



