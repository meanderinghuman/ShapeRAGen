import trimesh
import numpy as np

# Create outer pyramid vertices
outer_base = 25.0
outer_height = 30.0
outer_vertices = np.array([
    [0, 0, 0],                     # base vertex 0
    [outer_base, 0, 0],            # base vertex 1
    [outer_base, outer_base, 0],    # base vertex 2
    [0, outer_base, 0],            # base vertex 3
    [outer_base/2, outer_base/2, outer_height]  # apex
])

# Create outer pyramid faces
outer_faces = np.array([
    [0, 1, 4],  # front face
    [1, 2, 4],  # right face
    [2, 3, 4],  # back face
    [3, 0, 4],  # left face
    [0, 3, 2],  # base triangle 1
    [0, 2, 1]   # base triangle 2
])

# Create inner pyramid vertices (smaller by 2mm wall thickness)
inner_offset = 2.0
inner_base = outer_base - 2 * inner_offset
inner_height = outer_height - inner_offset
inner_vertices = np.array([
    [inner_offset, inner_offset, 0],                     # base vertex 0
    [outer_base - inner_offset, inner_offset, 0],        # base vertex 1
    [outer_base - inner_offset, outer_base - inner_offset, 0],  # base vertex 2
    [inner_offset, outer_base - inner_offset, 0],        # base vertex 3
    [outer_base/2, outer_base/2, inner_height]           # apex
])

# Create inner pyramid faces
inner_faces = np.array([
    [0, 1, 4],  # front face
    [1, 2, 4],  # right face
    [2, 3, 4],  # back face
    [3, 0, 4],  # left face
    [0, 3, 2],  # base triangle 1
    [0, 2, 1]   # base triangle 2
])

# Create trimesh objects
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Create hollow pyramid by difference
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Export as STL
hollow_pyramid.export('output.stl')