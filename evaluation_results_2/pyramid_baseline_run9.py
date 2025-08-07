import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],       # Base vertex 0
    [25, 0, 0],      # Base vertex 1
    [25, 25, 0],     # Base vertex 2
    [0, 25, 0],      # Base vertex 3
    [12.5, 12.5, 30] # Apex vertex 4
])

# Create inner pyramid vertices (offset by 2mm for wall thickness)
inner_vertices = np.array([
    [2, 2, 0],       # Base vertex 0
    [23, 2, 0],      # Base vertex 1
    [23, 23, 0],     # Base vertex 2
    [2, 23, 0],      # Base vertex 3
    [12.5, 12.5, 28] # Apex vertex 4 (2mm below outer apex)
])

# Define faces for outer pyramid
outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [3, 2, 0],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Define faces for inner pyramid (inverted normals)
inner_faces = np.array([
    [0, 4, 1],  # Front face
    [1, 4, 2],  # Right face
    [2, 4, 3],  # Back face
    [3, 4, 0],  # Left face
    [3, 0, 2],  # Base triangle 1
    [0, 1, 2]   # Base triangle 2
]) + 5  # Offset by number of outer vertices

# Combine all vertices
all_vertices = np.vstack((outer_vertices, inner_vertices))

# Define connecting faces between outer and inner pyramids
connector_faces = np.array([
    [0, 5, 4], [4, 5, 9],    # Front bottom right
    [0, 4, 3], [3, 4, 8],     # Front bottom left
    [1, 6, 5], [5, 6, 9],     # Right bottom front
    [1, 2, 6], [6, 2, 7],     # Right bottom back
    [2, 7, 6], [6, 7, 9],     # Back bottom right
    [2, 3, 7], [7, 3, 8],     # Back bottom left
    [3, 8, 7], [7, 8, 9],     # Left bottom back
    [3, 0, 8], [8, 0, 5]      # Left bottom front
])

# Combine all faces
all_faces = np.vstack((outer_faces, inner_faces, connector_faces))

# Create mesh from vertices and faces
pyramid_mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)

# Repair mesh to ensure watertightness
pyramid_mesh.fill_holes()
pyramid_mesh.fix_normals()

# Export as STL
pyramid_mesh.export('output.stl')