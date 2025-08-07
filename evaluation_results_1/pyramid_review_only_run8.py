import trimesh
import numpy as np
from stl import mesh

# Define pyramid dimensions
base_size = 25.0  # mm
height = 30.0     # mm
wall_thickness = 2.0  # mm

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],                     # base vertex 0
    [base_size, 0, 0],             # base vertex 1
    [base_size, base_size, 0],     # base vertex 2
    [0, base_size, 0],             # base vertex 3
    [base_size/2, base_size/2, height]  # apex
])

# Create inner pyramid vertices (offset by wall thickness)
inner_size = base_size - 2 * wall_thickness
inner_height = height - wall_thickness
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, base_size - wall_thickness, 0],
    [wall_thickness, base_size - wall_thickness, 0],
    [base_size/2, base_size/2, inner_height]
])

# Combine outer and inner vertices
vertices = np.vstack((outer_vertices, inner_vertices))

# Define faces (triangles)
faces = [
    # Outer pyramid faces
    [0, 1, 4],
    [1, 2, 4],
    [2, 3, 4],
    [3, 0, 4],
    # Inner pyramid faces (inverted)
    [5, 6, 9],
    [6, 7, 9],
    [7, 8, 9],
    [8, 5, 9],
    # Base faces
    [0, 1, 5],
    [1, 5, 6],
    [1, 2, 6],
    [2, 6, 7],
    [2, 3, 7],
    [3, 7, 8],
    [3, 0, 8],
    [0, 8, 5],
    # Top faces
    [4, 5, 6],
    [4, 6, 7],
    [4, 7, 8],
    [4, 8, 5]
]

# Create mesh
pyramid_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

# Ensure mesh is watertight and valid for 3D printing
pyramid_mesh.fill_holes()
pyramid_mesh.fix_normals()

# Export as STL
pyramid_mesh.export('output.stl')