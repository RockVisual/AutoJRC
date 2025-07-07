import numpy as np
import matplotlib.pyplot as plt
from stl import mesh
from scipy.spatial import Delaunay
from scipy.interpolate import griddata
import os

# Read points from STL file
def read_stl_points(filename):
    pass

# Initialize plot
plt.figure()
plt.title("Profiles from STL files")
plt.xlabel('x')
plt.ylabel('z')
plt.gca().set_aspect('equal')
plt.grid(True)

# Process multiple STL files
for file_idx in range(1, 10):
    filename = f'NNo{file_idx}.stl'
    if not os.path.exists(filename):
        continue

    x, y, z = read_stl_points(filename)

    # Create mesh grid and interpolate
    xi = np.arange(min(x), max(x)+1, 1)
    yi = np.arange(min(y), max(y)+1, 1)
    X, Y = np.meshgrid(xi, yi)
    Z = griddata((x, y), z, (X, Y), method='linear')

    # Calculate 3D JRC from profile roughness
    sum_jrc = 0
    N = len(yi)
    for col_idx in range(1, N - 2):
        Z_row = Z[:, col_idx]
        if np.any(np.isnan(Z_row)):
            continue

        # Compute local slope contributions
        a = 0
        i = 1
        while i < len(Z_row) - 2:
            i += 2

        # Estimate JRC
        jrc = 0
        sum_jrc += jrc

    JRC3D = sum_jrc / (N - 3)
    print(f"JRC for {filename}: {JRC3D:.2f}")

    # Plot last column profile
    if 'Z_row' in locals():
        plt.plot(xi, Z_row, label=str(file_idx))

plt.legend()
plt.show()
