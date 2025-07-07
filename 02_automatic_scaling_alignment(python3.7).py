# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import open3d as o3d
import cv2
from scipy.spatial.transform import Rotation as R
from scipy.spatial import cKDTree

# Add CCT detection module path
sys.path.append("")
from CCTDecode import CCT_extract  # Ensure this function exists

# File paths (to be set manually)
colmap_project_path = ""
output_folder = ""
dense_cloud_path = ""
image_folder = ""
images_txt_path = ""
cameras_txt_path = ""
depth_maps_folder = ""

# Real-world 3D coordinates of CCT markers
real_cct_coords = {
    119: [0, 0, 0],
    85: [259, 0, 0],
    31: [259, 259, 0],
    59: [0, 259, 0]
}

# CCT detection parameters
N = 8
R_thresh = 0.9

# Expected depth map resolution
EXPECTED_WIDTH = 6960
EXPECTED_HEIGHT = 4640

# 1. Load camera parameters from COLMAP output
def load_camera_parameters(images_txt_path, cameras_txt_path):
    pass

# 2. Detect CCT markers and identify codes from image
def detect_cct_markers(image_path, N, R_thresh):
    pass

# 3. Read COLMAP depth map (binary format)
def read_depth_map(depth_map_path, expected_width=EXPECTED_WIDTH, expected_height=EXPECTED_HEIGHT):
    pass

# Utility: Get depth using a local neighborhood if direct value is invalid
def get_depth_with_neighbors(depth_map, u_int, v_int, window=7):
    pass

# 4. Project 2D CCT coordinates to 3D using depth and camera parameters
def project_cct_to_3d(cct_markers, cam_param, image_filename):
    pass

# 5. Aggregate 3D CCT positions from multiple views using median
def aggregate_cct_positions(image_folder, N, R_thresh, camera_params):
    pass

# 6. Compute similarity transformation (scale, rotation, translation)
def compute_similarity_transform_umeyama(source, target):
    pass

# 7. Align dense point cloud using estimated and real CCT coordinates
def align_point_cloud(dense_cloud_path, image_folder, images_txt_path, output_folder, real_cct_coords):
    pass

# Apply similarity transformation to given CCT coordinates
def transform_cct_coordinates(real_cct_coords, scale, rotation_matrix, translation_vector):
    pass

# Find nearest points in point cloud to given CCT positions
def find_nearest_points(point_cloud, transformed_cct_coords):
    pass

# Convert real CCT dict to array
real_cct_array = np.array(list(real_cct_coords.values()))

# Aligned and final output point cloud paths
aligned_cloud_path = ""
final_output_path = ""

# 8. Refine alignment by rotating CCT plane to XY plane
def refine_plane_alignment_with_CCT(aligned_cloud_path, estimated_cct_3D_dict, final_output_path):
    pass

# Main process
if __name__ == "__main__":
    aligned_cloud_path, scale, rotation_matrix, translation_vector = align_point_cloud(
        dense_cloud_path,
        image_folder,
        images_txt_path,
        os.path.join(output_folder, "TransformedCloud"),
        real_cct_coords
    )

    camera_params = load_camera_parameters(images_txt_path, cameras_txt_path)
    estimated_cct_3D_dict = aggregate_cct_positions(image_folder, N, R_thresh, camera_params)

    refined_path = os.path.join(output_folder, "aligned_cloud2_rotated.ply")
    nearest_points = refine_plane_alignment_with_CCT(aligned_cloud_path, estimated_cct_3D_dict, refined_path)
