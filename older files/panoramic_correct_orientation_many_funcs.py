# Evaluation over lost time getting confused:
    # look up stuff on wikipedia more
    # ask ChatGPT more about math, coding, commeting culture
    # use desmos more
    # use modules like tabulate more (don't muck about with string formatting)


import cv2
import numpy as np
from tabulate import tabulate
import math


# Set file path and open image
file_path = r"Panoramic_Correction/images/hdr_test_ireland.jpg"
image_orig = cv2.imread(file_path)

image_height = 4000
image_width = 8000

rotate_pan = 30
rotata_tilt = 15


def panoramic_to_cartesian(v, u, width, height):
    x = (np.sin(np.pi*((2*(u/width)) - 1))) * (np.sqrt(1 - ((2*(v/height)) - 1)**2))
    y = (np.cos(np.pi*((2*(u/width)) - 1))) * (np.sqrt(1 - ((2*(v/height)) - 1)**2))
    z = (2*(v/height)) - 1
    return x, y, z

def cartesian_to_panoramic(x, y, z, width, height):
    u = (width/2)  *  ((np.sign(y)*np.arctan2(y, x)/np.pi) + 1)
    v = (height/2)  *  (np.sqrt(1 - z**2) + 1)
    return u, v


def spherical_rad_to_cartesian(theta, phi):
    x = np.cos(theta) * np.sin(phi)
    y = np.cos(theta) * np.cos(phi)
    z = np.sin(np.pi*theta)
    return x, y, z

def correct_pan(x, y, z, pan):
    xyz_tuple = x, y, z
    # Construct the rotation matrix around the z-axis
    rotation_matrix = np.array([
        [np.cos(pan), -np.sin(pan), 0, 0],
        [np.sin(pan), np.cos(pan), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    point_homogeneous = np.array(xyz_tuple + (1,))      # Convert the point to homogeneous coordinates
    rot_point_homogeneous = np.dot(rotation_matrix, point_homogeneous)  # Apply the rotation
    xyz_panned_tuple = rot_point_homogeneous[:3]   # Convert back to Cartesian coordinates
    x = xyz_panned_tuple[0]
    y = xyz_panned_tuple[1]
    z = xyz_panned_tuple[2]
    return x, y, z     # Returns tuple with new coords (x_rot, y_rot, z_rot)

def correct_tilt(x, y, z, tilt):
    xyz_tuple = x, y, z
    # Construct the rotation matrix around the z-axis
    rotation_matrix = np.array([
        [np.cos(tilt), -np.sin(tilt), 0, 0],
        [np.sin(tilt), np.cos(tilt), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    point_homogeneous = np.array(xyz_tuple + (1,))      # Convert the point to homogeneous coordinates
    rot_point_homogeneous = np.dot(rotation_matrix, point_homogeneous)  # Apply the rotation
    xyz_tilted_tuple = rot_point_homogeneous[:3]   # Convert back to Cartesian coordinates
    x = xyz_tilted_tuple[0]
    y = xyz_tilted_tuple[1]
    z = xyz_tilted_tuple[2]
    return x, y, z    # Returns tuple with new coords (x_rot, y_rot, z_rot)

def cartesian_to_spherical_deg(x, y, z):
    theta = (np.pi/2) - np.arccos(z)
    if z not in [-1, 1]:
        phi = (np.pi/2) - np.arctan2(y, x)
    else:
        phi = 0
    return theta, phi



cv2.imshow