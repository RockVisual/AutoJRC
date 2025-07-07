import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt


def remove_outliers(point_cloud, nb_neighbors=20, std_ratio=2.0):
    """
    Remove outliers from the point cloud using Open3D's statistical outlier removal filter.
    :param point_cloud: Open3D PointCloud object.
    :param nb_neighbors: Number of neighboring points to analyze for each point.
    :param std_ratio: The standard deviation multiplier to classify points as outliers.
    :return: Filtered point cloud without outliers.
    """
    cl, ind = point_cloud.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    inlier_cloud = point_cloud.select_by_index(ind)
    return inlier_cloud


def fit_plane_to_point_cloud(point_cloud):
    """
    Fits a plane to the point cloud using RANSAC.
    :param point_cloud: Open3D PointCloud object.
    :return: Plane parameters (a, b, c, d) for the plane equation ax + by + cz + d = 0.
    """
    plane_model, inlier_indices = point_cloud.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
    return plane_model


def create_square_on_plane(center, normal, side_length=90):
    """
    Creates a square on the plane given the center and normal of the plane.
    :param center: The center point of the square (X, Y, Z).
    :param normal: The normal vector of the plane (a, b, c).
    :param side_length: The side length of the square.
    :return: Vertices of the square on the plane.
    """
    # Define half side length
    half_side = side_length / 2

    # Create square vertices (in X, Y coordinates)
    square = np.array([
        [half_side, half_side],  # Top right corner
        [-half_side, half_side],  # Top left corner
        [-half_side, -half_side],  # Bottom left corner
        [half_side, -half_side]  # Bottom right corner
    ])

    # Rotate square points to align with the plane normal
    # We assume the plane normal is the Z-axis, so the square is initially along the XY plane.
    # Perform a rotation matrix to align the square with the plane normal.
    normal = normal / np.linalg.norm(normal)  # Normalize normal

    # Since the square is in the XY plane, calculate corresponding Z values based on the plane equation
    a, b, c = normal[:3]

    # Translate square vertices to the plane center
    square_3d = np.zeros((4, 3))  # Create a 4x3 matrix (X, Y, Z)
    square_3d[:, :2] = square  # Add X, Y coordinates
    square_3d[:, 0] += center[0]  # Add X translation
    square_3d[:, 1] += center[1]  # Add Y translation

    # Calculate Z values based on the plane equation ax + by + cz + d = 0
    d = -np.dot(normal, center)  # Plane offset
    square_3d[:, 2] = (-d - a * square_3d[:, 0] - b * square_3d[:, 1]) / c  # Solve for Z

    return square_3d


def filter_points_inside_square(point_cloud, square_vertices):
    """
    Filters out points that are outside the square in the plane and retains color.
    :param point_cloud: Open3D PointCloud object with XYZ data.
    :param square_vertices: The vertices of the square in 3D space.
    :return: Filtered point cloud containing points inside the square with original colors.
    """
    # Get points and colors from the original point cloud
    points = np.asarray(point_cloud.points)
    colors = np.asarray(point_cloud.colors)

    square_min_x, square_max_x = np.min(square_vertices[:, 0]), np.max(square_vertices[:, 0])
    square_min_y, square_max_y = np.min(square_vertices[:, 1]), np.max(square_vertices[:, 1])

    # Find points within the bounds of the square
    mask = (points[:, 0] >= square_min_x) & (points[:, 0] <= square_max_x) & \
           (points[:, 1] >= square_min_y) & (points[:, 1] <= square_max_y)

    # Filter the points that lie inside the square and their corresponding colors
    filtered_points = points[mask]
    filtered_colors = colors[mask]

    # Create a new point cloud for the filtered points and colors
    filtered_point_cloud = o3d.geometry.PointCloud()
    filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)

    return filtered_point_cloud


def main(input_ply_file, output_ply_file):
    # Load point cloud
    point_cloud = o3d.io.read_point_cloud(input_ply_file)

    # Step 1: Remove outliers
    print("Removing outliers...")
    filtered_point_cloud = remove_outliers(point_cloud)

    # Step 2: Fit a plane to the point cloud
    print("Fitting a plane...")
    plane_model = fit_plane_to_point_cloud(filtered_point_cloud)

    # Get the plane parameters (a, b, c, d)
    a, b, c, d = plane_model
    print(f"Plane model parameters: a={a}, b={b}, c={c}, d={d}")

    # Step 3: Create a square on the plane
    print("Creating a square on the plane...")
    center = np.mean(np.asarray(filtered_point_cloud.points), axis=0)  # Center point of the cloud
    square_vertices = create_square_on_plane(center, [a, b, c])

    # Step 4: Filter points inside the square and retain colors
    print("Filtering points inside the square...")
    final_point_cloud = filter_points_inside_square(filtered_point_cloud, square_vertices)

    # Step 5: Export the result to a new PLY file
    print(f"Saving filtered point cloud to {output_ply_file}...")
    o3d.io.write_point_cloud(output_ply_file, final_point_cloud)

    print("Process completed successfully.")


# Main processing
input_ply_file = "E:/biyelunwen/SAM/DATA/biaozhutupian_yanzheng/output/27_rockface.ply"
output_ply_file = "E:/biyelunwen/SAM/DATA/biaozhutupian_yanzheng/output/27_rockface_filtered.ply"

main(input_ply_file, output_ply_file)
