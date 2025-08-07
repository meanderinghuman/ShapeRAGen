import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],        # Base vertex 1
    [25, 0, 0],       # Base vertex 2
    [25, 25, 0],      # Base vertex 3
    [0, 25, 0],       # Base vertex 4
    [12.5, 12.5, 30]  # Apex
])

# Create inner pyramid vertices (scaled down by 80%)
scale_factor = 0.8
inner_vertices = np.array([
    [12.5 - 12.5*scale_factor, 12.5 - 12.5*scale_factor, 0],
    [12.5 + 12.5*scale_factor, 12.5 - 12.5*scale_factor, 0],
    [12.5 + 12.5*scale_factor, 12.5 + 12.5*scale_factor, 0],
    [12.5 - 12.5*scale_factor, 12.5 + 12.5*scale_factor, 0],
    [12.5, 12.5, 30*scale_factor]
])

# Combine vertices
vertices = np.vstack((outer_vertices, inner_vertices))

# Define faces for outer pyramid
outer_faces = [
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base face 1
    [0, 2, 1]   # Base face 2
]

# Define faces for inner pyramid (indices offset by 5)
inner_faces = [
    [5, 6, 9],  # Front face
    [6, 7, 9],  # Right face
    [7, 8, 9],  # Back face
    [8, 5, 9],  # Left face
    [5, 8, 7],  # Base face 1
    [5, 7, 6]   # Base face 2
]

# Define connecting faces between outer and inner pyramids
connector_faces = [
    [0, 1, 5], [1, 5, 6],  # Front bottom
    [1, 2, 6], [2, 6, 7],  # Right bottom
    [2, 3, 7], [3, 7, 8],  # Back bottom
    [3, 0, 8], [0, 8, 5],  # Left bottom
    [0, 4, 5], [4, 5, 9],  # Front left
    [1, 4, 6], [4, 6, 9],  # Front right
    [2, 4, 7], [4, 7, 9],  # Back right
    [3, 4, 8], [4, 8, 9]   # Back left
]

# Combine all faces
faces = outer_faces + inner_faces + connector_faces

# Create mesh
pyramid_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

# Ensure mesh is watertight and valid for 3D printing
pyramid_mesh.fill_holes()
pyramid_mesh.fix_normals()

# Export as STL
pyramid_mesh.export('output.stl')