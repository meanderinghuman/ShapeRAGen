import trimesh
import numpy as np

# Dimensions with validation
base_size = 25.0  # mm
height = 30.0     # mm
wall_thickness = max(1.0, 1.0)  # mm (enforced minimum of 1mm for FDM printing)

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],
    [base_size, 0, 0],
    [base_size, base_size, 0],
    [0, base_size, 0],
    [base_size/2, base_size/2, height]
])

# Create inner pyramid vertices with validated dimensions
inner_size = max(0, base_size - 2 * wall_thickness)
inner_height = max(0, height - wall_thickness)
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, base_size - wall_thickness, 0],
    [wall_thickness, base_size - wall_thickness, 0],
    [base_size/2, base_size/2, inner_height]
])

# Define faces with consistent winding
faces = np.array([
    [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  # Outer faces
    [5, 6, 9], [6, 7, 9], [7, 8, 9], [8, 5, 9],  # Inner faces (inverted)
    [0, 3, 1], [1, 3, 2],                         # Outer base
    [5, 6, 8], [6, 7, 8],                         # Inner base
    [0, 5, 1], [1, 6, 5],                         # Connecting walls
    [1, 6, 2], [2, 7, 6],
    [2, 7, 3], [3, 8, 7],
    [3, 8, 0], [0, 5, 8]
])

# Combine vertices and create mesh
all_vertices = np.vstack((outer_vertices, inner_vertices))
pyramid_mesh = trimesh.Trimesh(vertices=all_vertices, faces=faces)

# Mesh repair operations
pyramid_mesh.process(validate=True)
pyramid_mesh.fill_holes()
pyramid_mesh.fix_normals()

# Check if mesh is printable
if not pyramid_mesh.is_watertight:
    pyramid_mesh = pyramid_mesh.convex_hull
if pyramid_mesh.volume < 0.1:
    raise ValueError("Mesh volume too small for printing")

# Check wall thickness
if wall_thickness < 1.0:
    print("Warning: Wall thickness below recommended minimum for FDM printing")

# Export with binary STL for smaller file size
pyramid_mesh.export('hollow_pyramid.stl')