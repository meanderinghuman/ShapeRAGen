import trimesh
import numpy as np
from stl import mesh

base_size = 25
height = 30
wall_thickness = 2  # 2mm wall thickness for FDM printing

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],                   # Base vertex 0
    [base_size, 0, 0],           # Base vertex 1
    [base_size, base_size, 0],   # Base vertex 2
    [0, base_size, 0],           # Base vertex 3
    [base_size/2, base_size/2, height]  # Apex
])

# Create inner pyramid vertices (for hollowing)
inner_size = base_size - 2 * wall_thickness
inner_height = height - wall_thickness  # Maintain consistent wall thickness
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, base_size - wall_thickness, 0],
    [wall_thickness, base_size - wall_thickness, 0],
    [base_size/2, base_size/2, inner_height]  # Inner apex
])

# Define faces for outer pyramid
outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2], [0, 2, 1]  # Base
])

# Define faces for inner pyramid (inverted normals)
inner_faces = np.array([
    [0, 4, 1],  # Front face
    [1, 4, 2],  # Right face
    [2, 4, 3],  # Back face
    [3, 4, 0],  # Left face
    [0, 2, 3], [0, 1, 2]  # Base
]) + 5  # Offset by number of outer vertices

# Create connecting faces between outer and inner pyramids
connectors = np.array([
    [0, 5, 1], [1, 5, 6],
    [1, 6, 2], [2, 6, 7],
    [2, 7, 3], [3, 7, 8],
    [3, 8, 0], [0, 8, 5]
])

# Combine all vertices and faces
all_vertices = np.vstack((outer_vertices, inner_vertices))
all_faces = np.vstack((outer_faces, inner_faces, connectors))

# Create the mesh using trimesh for better handling
mesh_trimesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)

# Verify watertightness and fix if needed
if not mesh_trimesh.is_watertight:
    mesh_trimesh.fill_holes()
    mesh_trimesh.fix_normals()

# Export to STL using numpy-stl
pyramid_mesh = mesh.Mesh(np.zeros(mesh_trimesh.faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(mesh_trimesh.faces):
    pyramid_mesh.vectors[i] = mesh_trimesh.vertices[f]

# Save the mesh
pyramid_mesh.save('hollow_pyramid.stl')

# Print verification info
print(f"Is watertight: {mesh_trimesh.is_watertight}")
print(f"Volume: {mesh_trimesh.volume}")