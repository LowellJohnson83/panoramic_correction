import numpy as np


def spherical_to_cartesian(theta, phi):
    x = -np.sin(2 * np.pi * theta) * np.sin(np.pi * phi)
    y = -np.sin(2 * np.pi * theta) * np.cos(np.pi * phi)
    z = theta
    return x, y, z



# Example: Convert spherical coordinates (0.5, 0.25) to Cartesian coordinates
theta = 0.5  # Latitude
phi = 0.25   # Longitude
x, y, z = spherical_to_cartesian(theta, phi)
print("Cartesian Coordinates (x, y, z):", x, y, z)
