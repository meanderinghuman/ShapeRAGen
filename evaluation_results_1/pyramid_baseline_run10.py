import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],        # base vertex 0
    [25, 0, 0],       # base vertex 1
    [25, 25, 0],      # base vertex 2
    [0, 25, 0],       # base vertex 3
    [12.5, 12.5, 30]  # apex
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

# Combine outer and inner vertices
vertices = np.vstack((outer_vertices, inner_vertices))

# Define faces (triangles) for the pyramid
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

# Create the mesh
pyramid_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

# Ensure the mesh is watertight and valid for 3D printing
pyramid_mesh.fill_holes()
pyramid_mesh.fix_normals()

# Export as STL
pyramid_mesh.export('output.stl')