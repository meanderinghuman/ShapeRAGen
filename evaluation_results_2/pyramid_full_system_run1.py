import numpy as np
import trimesh
from stl import mesh

# Outer pyramid dimensions
base_size = 25.0  # mm
height = 30.0  # mm
wall_thickness = 2.0  # mm

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],                     # Base vertex 0
    [base_size, 0, 0],             # Base vertex 1
    [base_size, base_size, 0],     # Base vertex 2
    [0, base_size, 0],             # Base vertex 3
    [base_size/2, base_size/2, height]  # Apex vertex
])

# Create inner pyramid vertices (scaled down to make walls)
inner_scale = (base_size - 2*wall_thickness) / base_size
inner_vertices = outer_vertices.copy()
inner_vertices[:4] *= inner_scale  # Scale base vertices
inner_vertices[:4] += [wall_thickness, wall_thickness, 0]  # Offset to center

# Combine all vertices
all_vertices = np.vstack((outer_vertices, inner_vertices))

# Define faces for the pyramid (each face is a triangle)
faces = np.array([
    # Outer pyramid faces
    [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],
    # Inner pyramid faces (pointing inward)
    [5, 6, 9], [6, 7, 9], [7, 8, 9], [8, 5, 9],
    # Base faces (connecting outer and inner)
    [0, 1, 5], [1, 5, 6],
    [1, 2, 6], [2, 6, 7],
    [2, 3, 7], [3, 7, 8],
    [3, 0, 8], [0, 8, 5]
])

# Create the mesh
pyramid_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        pyramid_mesh.vectors[i][j] = all_vertices[f[j], :]

# Save to STL file
pyramid_mesh.save('output.stl')