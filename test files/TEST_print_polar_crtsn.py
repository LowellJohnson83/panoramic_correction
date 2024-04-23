# import cv2
import numpy as np
from tabulate import tabulate
# import math

# Set file path and open image
# file_path = r"HDR_Correction/images/hdr_test_ireland.jpg"
# image_orig = cv2.imread(file_path)

image_height = 4000
image_width = 8000

h_north_pole = 1 * (image_height)
h_equator = 0.5 * (image_height)
h_south_pole = 0 * (image_height)
h_london_lat = (51.5072/180)*np.pi * (image_height)

w_anti_mer = 0 * (image_width)
w_green_mer = 0.5 * (image_width)
w_90east_mer = 0.75 * (image_width)


def spherical_deg_to_cartesian(theta, phi):
    x = np.cos(np.pi*(theta/180)) * np.sin(np.pi*(phi/180))
    y = np.cos(np.pi*(theta/180)) * np.cos(np.pi*(phi/180))
    z = np.sin(np.pi*(theta/180))
    return x, y, z

def cartesian_to_spherical_deg(x, y, z):
    theta = 90 - (np.arccos(z) * (180 / np.pi))
    if z not in [-1, 1]:
        phi = 90 - (np.arctan2(y, x) * (180 / np.pi))
    else:
        phi = 0
    return theta, phi


iter_steps_neg = -8
iter_steps = 8


print()


# North, "in front":
coords_angles_ottowa =     ["Ottowa",        45.42, -75.70]
# South, "in front":
coords_angles_sao_paolo =  ["Sao Paulo",    -23.56, -46.64]
# North, "at the back":
coords_angles_osaka =      ["Osaka",         34.69, 135.50]
# South, "at the back":
coords_angles_auckland =   ["Auckland",     -36.85, 174.76]
# North on Greenwich Mer:
coords_angles_london =     ["London",        51.50,   0   ]
# Equator "in front":
coords_angles_quito =      ["Quito",          0,    -78.47]
# Equator "at the back":
coords_angles_singapore =  ["Singapore",      0,    103.81]
coords_angles_north_pole = ["(North Pole)",  90,      0   ]
coords_angles_south_pole = ["(South Pole)", -90,      0   ]
coords_angles_null_point = ["(Null Point)",   0,      0   ]

cities_angles_list = [
    coords_angles_ottowa,
    coords_angles_sao_paolo,
    coords_angles_osaka,
    coords_angles_auckland,
    coords_angles_london,
    coords_angles_quito,
    coords_angles_singapore,
    coords_angles_north_pole,
    coords_angles_south_pole,
    coords_angles_null_point,
]

coords_angles_various_cities = [
    [
        f"City: {city[0]}",
        f"City: {city[1]}",
        f"City: {city[2]}",
        ]
    for city in cities_angles_list]
print("Various Cities' Long / Lat coordinates:\n")
print(tabulate(coords_angles_various_cities, headers=["City", "Latitude ('Theta')", "Longtitude ('Phi')"], tablefmt="grid"))
print()

coords_x_y_z_various_cities = [
    [
        f"City: {city[0]}",
        f"Crtsn X: {round(spherical_deg_to_cartesian(city[1], city[2])[0], 3)}",
        f"Crtsn Y: {round(spherical_deg_to_cartesian(city[1], city[2])[1], 3)}",
        f"Crtsn Z: {round(spherical_deg_to_cartesian(city[1], city[2])[2], 3)}",
        ]
    for city in cities_angles_list]
print("Various Cities' Long / Lat coordinates:\n")
print(tabulate(coords_x_y_z_various_cities, headers=["City", "Cartesian X Coords", "Cartesian Y Coords", "Cartesian Z Coords"], tablefmt="grid"))
print()


# North, "in front":
coords_x_y_z_ottowa =     ["Ottowa",      -0.68,   0.173,  0.712]
# South, "in front":
coords_x_y_z_sao_paolo =  ["Sao Paulo",   -0.666,  0.629, -0.4  ]
# North, "at the back":
coords_x_y_z_osaka =      ["Osaka",        0.576, -0.586,  0.569]
# South, "at the back":
coords_x_y_z_auckland =   ["Auckland",     0.073, -0.797, -0.6  ]
# North on Greenwich Mer:
coords_x_y_z_london =     ["London",       0,      0.623,  0.783]
# Equator "in front":
coords_x_y_z_quito =      ["Quito",       -0.98,   0.2,    0    ]
# Equator "at the back":
coords_x_y_z_singapore =  ["Singapore",    0.971, -0.239,  0    ]
coords_x_y_z_north_pole = ["(North Pole)", 0,      0,      1    ]
coords_x_y_z_south_pole = ["(South Pole)", 0,      0,     -1    ]
coords_x_y_z_null_point = ["(Null Point)", 0,      1,      0    ]

cities_x_y_z_list = [
    coords_x_y_z_ottowa,
    coords_x_y_z_sao_paolo,
    coords_x_y_z_osaka,
    coords_x_y_z_auckland,
    coords_x_y_z_london,
    coords_x_y_z_quito,
    coords_x_y_z_singapore,
    coords_x_y_z_north_pole,
    coords_x_y_z_south_pole,
    coords_x_y_z_null_point,
]

coords_angles_various_cities_check = [
    [
        f"City: {city[0]}",
        f"Latitude: {round(cartesian_to_spherical_deg(city[1], city[2], city[3])[0], 3)}",
        f"Longtitude: {round(cartesian_to_spherical_deg(city[1], city[2], city[3])[1], 3)}",
        ]
    for city in cities_x_y_z_list
]

print("Various Cities' X/Y/Z coordinates (CHECK to see if correct):\n")
print(tabulate(coords_angles_various_cities_check, headers=["City", "Latitude ('Theta')", "Longtitude ('Phi')"], tablefmt="grid"))
print()