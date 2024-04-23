# Evaluation over lost time getting confused:
    # look up stuff on wikipedia more
    # ask ChatGPT more about math, coding, commeting culture
    # use desmos more
    # use modules like tabulate more (don't muck about with string formatting)
    # Break function down into smaller steps (if it's included within a def func())
    # Use ChatGPT to consolidate into one function
    # Use Google Notes (not physical paper!!)
    # Don't waste time on Google Docs making pretty formulas (google Notes will fulfil that function)

import cv2
import numpy as np
from tabulate import tabulate
import math

# Interesting facts:
#   - 'Phi' and 'pan' begin with 'P'
#   - Theta and tilt begin with 'T'



# Set file path and open image
file_path = r"Panoramic_Correction/images/hdr_test_ireland_small.jpg"
image_orig = cv2.imread(file_path)

# Convert the image to a NumPy array
array_pano_orig = np.array(image_orig)

# Define theta and phi based on the shape of the image array
height, width = image_orig.shape[:2]

# Define theta and phi based on the shape of the image array
height, width = image_orig.shape[:2]
v = np.linspace(0, height, height)[:, np.newaxis]  # 2D array of theta values
u = np.linspace(0, width, width)  # 1D array of phi values



height, width = 4000, 8000


def panoramic_correction_steps(u, v, pan, tilt, width, height):
    # Panoramic to Panoramic-Normalised:
    u_norm = (2*(u/width)) - 1
    v_norm = (2*(v/height)) - 1

    # Panoramic-Normalised to Spherical:
    phi = np.pi * u_norm
    theta = np.arcsin(v_norm)
    # theta = arcsin(v_norm), however theta will be redundant as z = sin(arcsin(v_norm)) therefore canceing out meaning z = v_norm)

    # Spherical to Spherical-Panned (rotate around Z axis):
    # Pan the image (using "pan" argument) to get tilted defect lined to zero: 
    phi_pan = (phi - pan + np.pi) % 2*np.pi
    theta_pan = theta
    
    # Panoramic-Panned to Cartesian-Panned
    x_pan = np.cos(theta_pan) * np.sin(phi_pan)
    y_pan = np.cos(theta_pan) * np.cos(phi_pan)
    z_pan = np.sin(theta_pan)

    # Cartesian-Panned to Cartesian-Panned-Tilted
    x_pan_tilt = x_pan
    y_pan_tilt = y_pan * np.cos(tilt)
    z_pan_tilt = z_pan * np.sin(tilt)

    # Cartesian-Panned-Tilted to Spherical_Panned_Tilted:
    phi_pan_tilt = (np.pi/2) - np.arctan2(y_pan_tilt, x_pan_tilt)
    theta_pan_tilt = (np.pi/2) - np.arccos(z_pan_tilt)

    # Spherical_Panned_Tilted to Spherical_Tilted
    phi_tilt = phi_pan_tilt + pan
    theta_tilt = theta_pan_tilt

    # Spherical_Tilted to Panoramic-Normalised-Tilted:
    u_norm_tilt = phi_tilt/np.pi
    v_norm_tilt = np.sin(theta_tilt)

    # Panoramic-Normalised-Tilted to Panoramic-Corrected (Panoramic-Tilted):
    u_correct = (width/2) * (u_norm_tilt + 1)
    v_correct = (height/2) * (v_norm_tilt + 1)

    return u_correct, v_correct






def panoramic_correction_steps_simplified_mine(u, v, pan, tilt):
    # Panoramic-Normalised-Tilted to Panoramic-Corrected (Panoramic-Tilted):
    u_correct = (width/2) * (((((np.pi/2) - np.arctan2(
        ((np.cos(np.arcsin((2*(v/height)) - 1)) * np.cos(np.pi*(((np.pi * ((2*(u/width)) - 1)) - pan + np.pi) % 2*np.pi))) * np.cos(tilt)),
        (np.cos(np.arcsin((2*(v/height)) - 1)) * np.sin(np.pi*(((np.pi * ((2*(u/width)) - 1)) - pan + np.pi) % 2*np.pi))))) + pan) / np.pi) + 1)
    v_correct = (height/2) * ((np.sin((np.pi/2) - np.arccos(((np.sin(np.arcsin((2*(v/height)) - 1))) * np.sin(tilt))))) + 1)

    return u_correct, v_correct


def panoramic_correction_simplified(u, v, pan, tilt, width, height):
    u_correct = (width / 2) * ((((np.pi / 2) - np.arctan2(
        ((np.cos(np.arcsin((2 * (v / height)) - 1)) * np.cos(np.pi * (((np.pi * ((2 * (u / width)) - 1)) - pan + np.pi) % (2 * np.pi)))) * np.cos(tilt)),
        (np.cos(np.arcsin((2 * (v / height)) - 1)) * np.sin(np.pi * (((np.pi * ((2 * (u / width)) - 1)) - pan + np.pi) % (2 * np.pi))))))) + pan) / np.pi + 1
    v_correct = (height / 2) * ((np.sin((np.pi / 2) - np.arccos(((np.sin(np.arcsin((2 * (v / height)) - 1))) * np.sin(tilt))))) + 1)
    return u_correct, v_correct



print(panoramic_correction_steps(2000, 3000, 0, 0, width, height))
print(panoramic_correction_steps(2000, 3000, (np.pi/2), (np.pi/6), width, height))