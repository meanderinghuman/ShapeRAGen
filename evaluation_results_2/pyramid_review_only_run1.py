import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],         # Base vertex 0
    [25, 0, 0],        # Base vertex 1
    [25, 25, 0],       # Base vertex 2
    [0, 25, 0],        # Base vertex 3
    [12.5, 12.5, 30]   # Apex vertex
])

# Create inner pyramid vertices (offset by 2mm for wall thickness)
inner_vertices = np.array([
    [2, 2, 0],         # Base vertex 0
    [23, 2, 0],        # Base vertex 1
    [23, 23, 0],       # Base vertex 2
    [2, 23, 0],        # Base vertex 3
    [12.5, 12.5, 28]   # Apex vertex (reduced height to maintain thickness)
])

# Combine vertices
all_vertices = np.vstack((outer_vertices, inner_vertices))

# Define faces (triangles)
faces = [
    # Outer pyramid faces
    [0, 1, 4],
    [1, 2, 4],
    [2, 3, 4],
    [3, 0, 4],
    # Inner pyramid faces (pointing inward)
    [5, 6, 9],
    [6, 7, 9],
    [7, 8, 9],
    [8, 5, 9],
    # Base faces (connecting outer and inner)
    [0, 1, 5],
    [1, 5, 6],
    [1, 2, 6],
    [2, 6, 7],
    [2, 3, 7],
    [3, 7, 8],
    [3, 0, 8],
    [0, 8, 5]
]

# Create mesh
pyramid_mesh = trimesh.Trimesh(vertices=all_vertices, faces=faces)

# Ensure mesh is watertight and valid for 3D printing
pyramid_mesh.fill_holes()
pyramid_mesh.fix_normals()

# Export as STL
pyramid_mesh.export('output.stl')