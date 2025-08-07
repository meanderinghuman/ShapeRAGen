import numpy as np
import trimesh
from stl import mesh

# Outer pyramid dimensions
base_size = 25.0  # mm
height = 30.0     # mm
wall_thickness = 2.0  # mm

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],                     # Base vertex 0
    [base_size, 0, 0],             # Base vertex 1
    [base_size, base_size, 0],     # Base vertex 2
    [0, base_size, 0],             # Base vertex 3
    [base_size/2, base_size/2, height]  # Apex vertex
])

# Create inner pyramid vertices (smaller by wall thickness)
inner_size = base_size - 2 * wall_thickness
inner_height = height - wall_thickness
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],                     # Base vertex 0
    [base_size - wall_thickness, wall_thickness, 0],         # Base vertex 1
    [base_size - wall_thickness, base_size - wall_thickness, 0],  # Base vertex 2
    [wall_thickness, base_size - wall_thickness, 0],         # Base vertex 3
    [base_size/2, base_size/2, inner_height]                 # Apex vertex
])

# Combine all vertices
all_vertices = np.vstack([outer_vertices, inner_vertices])

# Define faces for the outer pyramid (4 sides and 1 base)
outer_faces = np.array([
    [0, 1, 4],  # Side 1
    [1, 2, 4],  # Side 2
    [2, 3, 4],  # Side 3
    [3, 0, 4],  # Side 4
    [3, 2, 1],  # Base
    [1, 0, 3]   # Base (second triangle)
])

# Define faces for the inner pyramid (4 sides and 1 base)
inner_faces = np.array([
    [5, 9, 6],  # Side 1
    [6, 9, 7],  # Side 2
    [7, 9, 8],  # Side 3
    [8, 9, 5],  # Side 4
    [8, 7, 6],  # Base
    [6, 5, 8]   # Base (second triangle)
])

# Define faces for the walls between outer and inner pyramids
wall_faces = np.array([
    [0, 5, 1], [1, 5, 6],  # Bottom front wall
    [1, 6, 2], [2, 6, 7],  # Bottom right wall
    [2, 7, 3], [3, 7, 8],  # Bottom back wall
    [3, 8, 0], [0, 8, 5],  # Bottom left wall
    [4, 9, 5], [4, 5, 0],  # Front top wall
    [4, 6, 9], [4, 1, 6],  # Right top wall
    [4, 7, 9], [4, 2, 7],  # Back top wall
    [4, 8, 9], [4, 3, 8]   # Left top wall
])

# Combine all faces
all_faces = np.vstack([outer_faces, inner_faces, wall_faces])

# Create the mesh
pyramid_mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)

# Ensure the mesh is watertight (important for 3D printing)
pyramid_mesh.fill_holes()
pyramid_mesh.process()

# Export as STL
pyramid_mesh.export('output.stl')