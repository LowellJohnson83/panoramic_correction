import cv2
import numpy as np
from tabulate import tabulate
import math




"""
The Function below takes in horizontal and vertical values (u, v) 
along with values to correct the pan and tilt.
The function will output the corrrected horizontal and vertical values
('u_correct' and 'v_correct')"""


# Version 1 (problems)
""" def panoramic_correction_steps(u, v, pan, tilt):

    # Spherical to Spherical-Panned (rotate around Z axis):
    phi_pan = (np.pi * u + pan)
    theta_pan = np.arcsin(2 * v - 1)   

    # Panoramic-Panned to Cartesian-Panned
    x_pan = np.cos(theta_pan) * np.sin(phi_pan)
    y_pan = np.cos(theta_pan) * np.cos(phi_pan)
    z_pan = np.sin(theta_pan)

    sqrt_x_pan2_y_pan2 = np.sqrt(x_pan**2 + y_pan**2)
    # inclin_angle = np.arctan(z_pan / sqrt_x_pan2_y_pan2)
    sqrt_yp_sq_zp_sq = np.sqrt(y_pan**2 + z_pan**2)
    # y_z_angle = np.arctan(z_pan / y_pan)
    y_z_angle = np.sign(y_pan) * np.arctan(z_pan / y_pan)               # THIS IS A CRUCIAL BIT (sign of zy angle)

    # Cartesian-Panned to Cartesian-Panned-Tilted
    x_pan_tilt = x_pan
    y_pan_tilt = sqrt_yp_sq_zp_sq * np.cos(y_z_angle - tilt)
    z_pan_tilt = sqrt_yp_sq_zp_sq * np.sin(y_z_angle - tilt)

    # Cartesian-Panned-Tilted to Spherical_Panned_Tilted:
    sqrt_xpt_sq_ypt_sq = np.sqrt(x_pan_tilt**2 + y_pan_tilt**2)
    phi_pan_tilt = - (np.sign(y_pan_tilt) * np.arccos(x_pan_tilt/sqrt_xpt_sq_ypt_sq))
    # phi_pan_tilt = - (1 * np.arccos(x_pan_tilt/sqrt_xpt_sq_ypt_sq))
    theta_pan_tilt = (np.pi/2) - np.arccos(z_pan_tilt)

    # Spherical_Panned_Tilted to Spherical_Tilted
    phi_tilt = phi_pan_tilt - pan
    theta_tilt = theta_pan_tilt

    # Panoramic-Normalised-Tilted to Panoramic-Corrected (Panoramic-Tilted):
    u_correct = (((phi_tilt * (2/np.pi)) + 1) / 2) % 1
    v_correct = (np.sin(theta_tilt) + 1) / 2

    # TEST ALL VARIABLES
    # u_correct = u_correct
    # v_correct = v_correct

    # For Testing non-array inputs (simple one-element integers or floats) ...
    # ... execute this function for analysing values:
    if np.all(u) and np.all(v) == int():
        print_pano_correct_steps(
            u, v,
            phi_pan, theta_pan, x_pan, y_pan, z_pan,
            sqrt_yp_sq_zp_sq,
            x_pan_tilt, y_pan_tilt, z_pan_tilt,
            sqrt_xpt_sq_ypt_sq,
            phi_pan_tilt, theta_pan_tilt,
            phi_tilt, theta_tilt,
            u_correct, v_correct)

    # Return Corrected Values:
    return u_correct, v_correct """

pi = np.pi
# pi = 3.141593
# pi = 3.1415
# pi = 3.14

def keep_in_bounds(value):
    bounded = np.max(np.min(value, 0.999), 0.001)
    # if value.any() >= 0.999:
    #     bounded = 0.999
    # elif value.any() <= 0.001:
    #     bounded = 0.001
    # else:
    #     bounded = value
    return bounded

def phi_to_horiz_range(angle):
    shrink = angle / (2 * pi)
    result = keep_in_bounds(shrink)
    return result

def theta_to_vert_range(angle):
    shrink = (np.sin(angle) + 1) / 2
    result = keep_in_bounds(shrink)
    return result

def half_add_half_range(cartesian):
    shrink = (cartesian / 2) + (1/2)
    result = keep_in_bounds(shrink)
    return result

number = 10

# Version 2
def panoramic_correction_steps(u, v, pan, tilt):

    # u = np.maximum(np.minimum(u, 0.999), 0.001)
    # v = np.maximum(np.minimum(v, 0.999), 0.001)

    # Panoramic to Spherical
    phi = (2 * pi * u) % pi
    # theta = max(min(np.arcsin(2 * v - 1), ((pi/2) - 0.001)), 0.001)
    theta = np.arcsin(2 * v - 1) % pi

    # Spherical to Spherical-Panned (rotate around Z axis):
    phi_pan = (phi + pan) % (2 * pi)                   # CHANGE: 2 * pi*u (NOT '1 * pi*u')
    theta_pan = theta   

    # Panoramic-Panned to Cartesian-Panned
    x_pan = -np.cos(theta_pan) * np.sin(phi_pan)        # CHANGE: negative sign added
    y_pan = np.cos(theta_pan) * np.cos(phi_pan)
    z_pan = np.sin(theta_pan)

    # Establish X lock and 
    x_axis_distance = np.sqrt(y_pan**2 + z_pan**2)     # ("X Lock")
    y_z_angle = (-np.arctan(z_pan / y_pan)) % pi       # CHANGE: 1) remove sgn(y) 2) add "%" of pi 3) negative sign arctan() 
    
    # Cartesian-Panned to Cartesian-Panned-Tilted
    x_pan_tilt = x_pan
    # CHANGE: "'+' tilt" (instead of '-')   2) theta sign
    y_pan_tilt = np.sign(theta) * x_axis_distance * np.cos(y_z_angle + tilt)
    # CHANGE:   "   "   "   "   "   "   "
    z_pan_tilt = np.sign(theta) * x_axis_distance * np.sin(y_z_angle + tilt)

    # Establish Z lock and 
    z_axis_distance = np.sqrt(x_pan_tilt**2 + y_pan_tilt**2)

    # Estblish Sign ('square' wave) function and Z lock radius
    # CHANGE: Below function created
    sign_coefficient = 2 * np.round((1 - 1/(2*pi)) * np.absolute(u - (pi * np.round(((-1/pi) * (tilt + theta)) + 1)))) - 1

    # Cartesian-Panned-Tilted to Spherical_Panned_Tilted:
    # CHANGE: 1) Add 3pi/2   2) '-' pan at the end   3) all to the '%' of 2pi 
    phi_tilt = - (((3/2) * pi) - (np.sign(y_pan_tilt) * np.arccos(x_pan_tilt/z_axis_distance)) - pan) % (2*pi)
    # CHANGE: 1) remove pi/2   2) change main function to '+' sign   3) multiply by sign_coefficient
    theta_tilt = sign_coefficient * np.arccos(z_pan_tilt)


    # Panoramic-Normalised-Tilted to Panoramic-Corrected (Panoramic-Tilted):
    u_correct = (phi_tilt / (2*pi))
    v_correct = (np.sin(theta_tilt) + 1) / 2

    # TEST ALL VARIABLES
    u_correct = phi / (2 * pi)
    v_correct = (np.sin(theta) + 1) / 2
    # u_correct = phi_to_horiz_range(phi)
    # v_correct = theta_to_vert_range(theta)
    # u_correct = half_add_half_range(x_pan)
    # v_correct = theta_to_vert_range(z_pan)

    # u_correct = max((min(((x_pan/2) + (1/2)), 0.999)), 0.001)
    # v_correct = max((min(((z_pan/2) + (1/2)), 0.999)), 0.001)
    # u_correct = 0.8 * ((x_pan/2) + (1/2))
    # v_correct = 0.8 * ((z_pan/2) + (1/2))

    # For Testing non-array inputs (simple one-element integers or floats) ...
    # ... execute this function for analysing values:
    """ if np.all(u) and np.all(v) == int():
        print_pano_correct_steps(
            u, v, phi, theta,
            phi_pan, theta_pan, x_pan, y_pan, z_pan,
            x_axis_distance,
            x_pan_tilt, y_pan_tilt, z_pan_tilt,
            z_axis_distance,
            phi_tilt, theta_tilt,
            u_correct, v_correct) """

    # Return Corrected Values:
    return u_correct, v_correct


""" 
The function below is used to monitor the values at each step of the way in the function
'panoramic_correction_steps(",",",")' to catch anomilies
"""
def print_pano_correct_steps(
    u, v, phi, theta,
    phi_pan, theta_pan, x_pan, y_pan, z_pan,
    x_axis_distance,
    x_pan_tilt, y_pan_tilt, z_pan_tilt,
    z_axis_distance,
    phi_tilt, theta_tilt,
    u_correct, v_correct):

    print()
    print(f"u,           v               : {(round(u,2))},\t{round(v,2)}")
    print()
    print(f"phi,         theta           : {(int(phi*(180/pi)))}°,\t{(int(theta*(180/pi)))}°")
    print(f"phi_pn,      theta_pn        : {(int(phi_pan*(180/pi)))}°,\t{(int(theta_pan*(180/pi)))}°")
    print(f"x_pn,     y_pn,     z_pn     : {(round(x_pan,2))},\t{round(y_pan,2)},\t{round(z_pan,2)}")
    print(f"z_axis_distance              : {(round(z_axis_distance,2))}")
    print(f"x_pn_tlt, y_pn_tlt, z_pn_tlt : {(round(x_pan_tilt,2))},\t{round(y_pan_tilt,2)},\t{round(z_pan_tilt,2)}")
    print(f"x_axis_distance              : {(round(x_axis_distance,2))}")
    print(f"phi_tlt,     theta_tilt      : {(int(phi_tilt*(180/pi)))}°,\t{(int(theta_tilt*(180/pi)))}°")
    print() 
    print(f"u_correct,   v_correct       : {(round(u_correct,2))},\t{round(v_correct,2)}")
    print()


panoramic_correction_steps(0.25, 0.375, 0, 0)
panoramic_correction_steps(0.25, 0.375, pi/2, pi/6)

for i in range(8 + 1):
    panoramic_correction_steps(0.25, (i * 0.0625), 0, pi/3)

# Define COrrection parameters 'pan' and 'tilt'
pan = 0
# tilt = pi/18
tilt = 0

# Load the original image
file_path = "Panoramic_Correction/images/Lambert Mapping Grid_2.jpg"
image_orig = cv2.imread(file_path)

# Convert the image to a NumPy array
array_pano_orig = np.array(image_orig)

# Define u and v based on the shape of the image array
height, width = image_orig.shape[:2]
u = np.linspace(0, 1, width)  # 1D array of phi values (normalized)
v = np.linspace(0, 1, height)[:, np.newaxis]  # 2D array of theta values (normalized)

# Initialise arrays to store 'u_correct_channels' and 'v_correct_channels' coordinates for each colour channel
u_correct, v_correct = panoramic_correction_steps(u, v, pan, tilt)

# Convert the corrected coordinates to pixel indices
u_correct_pixels = (u_correct * (width - 1)).astype(int)
v_correct_pixels = (v_correct * (height - 1)).astype(int)

# Initialize the corrected image
image_correct = np.zeros_like(image_orig)

# Map pixels from the original image to the corrected image
for i in range(height):
    for j in range(width):
        image_correct[v_correct_pixels[i, j], u_correct_pixels[i, j]] = image_orig[i, j]

cv2.imshow("Original Panorama", image_orig)
cv2.imshow("Corrected Panorama", image_correct)
cv2.waitKey(0)

cv2.destroyAllWindows()
