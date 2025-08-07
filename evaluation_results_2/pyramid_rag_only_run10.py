import trimesh
import numpy as np
from stl import mesh

# Outer pyramid dimensions
base_size = 25.0
height = 30.0

# Wall thickness for FDM printing (2mm is a good default)
wall_thickness = 2.0

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],                      # Base vertex 0
    [base_size, 0, 0],              # Base vertex 1
    [base_size, base_size, 0],      # Base vertex 2
    [0, base_size, 0],              # Base vertex 3
    [base_size/2, base_size/2, height]  # Apex vertex
])

# Create inner pyramid vertices (scaled down to create hollow space)
inner_scale = (base_size - 2*wall_thickness) / base_size
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, base_size - wall_thickness, 0],
    [wall_thickness, base_size - wall_thickness, 0],
    [base_size/2, base_size/2, height - wall_thickness*(height/base_size)]
])

# Define faces for the outer pyramid
outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [3, 2, 0],  # Bottom face 1
    [2, 1, 0]   # Bottom face 2
])

# Define faces for the inner pyramid (inverted normals)
inner_faces = np.array([
    [5, 6, 9],  # Front face (inverted)
    [6, 7, 9],  # Right face (inverted)
    [7, 8, 9],  # Back face (inverted)
    [8, 5, 9],  # Left face (inverted)
    [8, 7, 5],  # Bottom face 1 (inverted)
    [7, 6, 5]   # Bottom face 2 (inverted)
])

# Create side walls connecting outer and inner pyramids
side_faces = np.array([
    [0, 1, 5], [1, 5, 6],  # Front-right wall 1
    [1, 2, 6], [2, 6, 7],  # Right-back wall 1
    [2, 3, 7], [3, 7, 8],  # Back-left wall 1
    [3, 0, 8], [0, 8, 5],  # Left-front wall 1
    [0, 5, 1], [1, 6, 2],  # Front-right wall 2
    [2, 7, 3], [3, 8, 0]   # Back-left wall 2
])

# Combine all vertices and faces
all_vertices = np.vstack((outer_vertices, inner_vertices))
all_faces = np.vstack((outer_faces, inner_faces, side_faces))

# Create the mesh
pyramid_mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)

# Ensure the mesh is watertight (important for 3D printing)
pyramid_mesh.fill_holes()
pyramid_mesh.process()

# Export as STL
pyramid_mesh.export('output.stl')