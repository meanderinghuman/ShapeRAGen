import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],          # Base vertex 0
    [25, 0, 0],         # Base vertex 1
    [25, 25, 0],       # Base vertex 2
    [0, 25, 0],        # Base vertex 3
    [12.5, 12.5, 30]   # Apex
])

# Create outer pyramid faces
outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Create inner pyramid vertices (scaled down version)
inner_vertices = np.array([
    [5, 5, 0],         # Base vertex 0
    [20, 5, 0],        # Base vertex 1
    [20, 20, 0],       # Base vertex 2
    [5, 20, 0],        # Base vertex 3
    [12.5, 12.5, 25]   # Apex (slightly lower)
])

# Create inner pyramid faces (same structure as outer)
inner_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Create trimesh objects
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Ensure both meshes are watertight
outer_mesh.fix_normals()
outer_mesh.fill_holes()
inner_mesh.fix_normals()
inner_mesh.fill_holes()

# Create hollow pyramid using difference
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Export as STL
hollow_pyramid.export('output.stl')