import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],         # Base vertex 1
    [25, 0, 0],        # Base vertex 2
    [25, 25, 0],       # Base vertex 3
    [0, 25, 0],        # Base vertex 4
    [12.5, 12.5, 30]   # Apex
])

# Create outer pyramid faces
outer_faces = np.array([
    [0, 1, 4],  # Side 1
    [1, 2, 4],  # Side 2
    [2, 3, 4],  # Side 3
    [3, 0, 4],  # Side 4
    [0, 3, 2],  # Base 1
    [0, 2, 1]   # Base 2
])

# Create inner pyramid vertices (smaller by 2mm for wall thickness)
inner_vertices = np.array([
    [2, 2, 0],         # Base vertex 1
    [23, 2, 0],        # Base vertex 2
    [23, 23, 0],       # Base vertex 3
    [2, 23, 0],        # Base vertex 4
    [12.5, 12.5, 28]   # Apex (2mm shorter)
])

# Create inner pyramid faces
inner_faces = np.array([
    [0, 1, 4],  # Side 1
    [1, 2, 4],  # Side 2
    [2, 3, 4],  # Side 3
    [3, 0, 4],  # Side 4
    [0, 3, 2],  # Base 1
    [0, 2, 1]   # Base 2
])

# Create meshes
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Create hollow pyramid by difference
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Export to STL
hollow_pyramid.export('output.stl')