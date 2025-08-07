import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],          # base vertex 0
    [25, 0, 0],         # base vertex 1
    [25, 25, 0],        # base vertex 2
    [0, 25, 0],         # base vertex 3
    [12.5, 12.5, 30]    # apex
])

# Create inner pyramid vertices (offset by 1mm)
inner_vertices = np.array([
    [1, 1, 0],          # base vertex 0
    [24, 1, 0],         # base vertex 1
    [24, 24, 0],        # base vertex 2
    [1, 24, 0],         # base vertex 3
    [12.5, 12.5, 29]    # apex (1mm below outer apex)
])

# Combine vertices
vertices = np.vstack((outer_vertices, inner_vertices))

# Define faces for outer pyramid
outer_faces = np.array([
    [0, 1, 4],  # front face
    [1, 2, 4],   # right face
    [2, 3, 4],   # back face
    [3, 0, 4],   # left face
    [3, 2, 1],   # base triangle 1
    [3, 1, 0]    # base triangle 2
])

# Define faces for inner pyramid (with vertex indices offset by 5)
inner_faces = np.array([
    [5, 6, 9],  # front face
    [6, 7, 9],   # right face
    [7, 8, 9],   # back face
    [8, 5, 9],   # left face
    [8, 7, 6],   # base triangle 1
    [8, 6, 5]    # base triangle 2
])

# Create connecting walls between outer and inner pyramids
wall_faces = np.array([
    [0, 5, 1], [1, 5, 6],  # front wall
    [1, 6, 2], [2, 6, 7],  # right wall
    [2, 7, 3], [3, 7, 8],  # back wall
    [3, 8, 0], [0, 8, 5],  # left wall
])

# Combine all faces
faces = np.vstack((outer_faces, inner_faces, wall_faces))

# Create the mesh
pyramid_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        pyramid_mesh.vectors[i][j] = vertices[f[j]]

# Save the STL file
pyramid_mesh.save('output.stl')