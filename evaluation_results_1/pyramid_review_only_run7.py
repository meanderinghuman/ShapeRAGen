import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
base_size = 25
height = 30
outer_vertices = np.array([
    [0, 0, 0],                  # base vertex 0
    [base_size, 0, 0],          # base vertex 1
    [base_size, base_size, 0],  # base vertex 2
    [0, base_size, 0],          # base vertex 3
    [base_size/2, base_size/2, height]  # apex vertex 4
])

# Create inner pyramid vertices (smaller by 2mm)
wall_thickness = 2
inner_size = base_size - 2 * wall_thickness
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],                  # base vertex 5
    [base_size-wall_thickness, wall_thickness, 0],        # base vertex 6
    [base_size-wall_thickness, base_size-wall_thickness, 0],  # base vertex 7
    [wall_thickness, base_size-wall_thickness, 0],        # base vertex 8
    [base_size/2, base_size/2, height-wall_thickness]     # apex vertex 9
])

# Combine all vertices
all_vertices = np.vstack((outer_vertices, inner_vertices))

# Define faces (triangles)
# Outer pyramid faces
outer_faces = np.array([
    [0, 1, 4],  # front face
    [1, 2, 4],  # right face
    [2, 3, 4],  # back face
    [3, 0, 4],  # left face
    [0, 3, 2],  # base bottom
    [0, 2, 1]   # base top (same as bottom but reversed)
])

# Inner pyramid faces (inverted normals)
inner_faces = np.array([
    [5, 9, 6],  # front face
    [6, 9, 7],  # right face
    [7, 9, 8],  # back face
    [8, 9, 5],  # left face
    [5, 8, 7],  # base top
    [5, 7, 6]   # base bottom (same as top but reversed)
])

# Side walls connecting outer and inner pyramids
side_faces = np.array([
    [0, 5, 1], [1, 5, 6],
    [1, 6, 2], [2, 6, 7],
    [2, 7, 3], [3, 7, 8],
    [3, 8, 0], [0, 8, 5]
])

# Combine all faces
all_faces = np.vstack((outer_faces, inner_faces, side_faces))

# Create the mesh
pyramid_mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)

# Ensure the mesh is watertight and valid for 3D printing
pyramid_mesh.fill_holes()
pyramid_mesh.fix_normals()

# Export as STL
pyramid_mesh.export('output.stl')