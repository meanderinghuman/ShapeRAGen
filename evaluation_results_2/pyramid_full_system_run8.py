import numpy as np
from stl import mesh
import trimesh

# Define pyramid dimensions with printing considerations
base_size = 25.0
height = 30.0
wall_thickness = 2.0  # Minimum recommended wall thickness for FDM printing
apex_radius = 1.0  # Radius to blunt the sharp apex for better printing

# Create outer pyramid vertices with blunted apex
outer_vertices = np.array([
    [0, 0, 0],                      # Base vertex 0
    [base_size, 0, 0],              # Base vertex 1
    [base_size, base_size, 0],      # Base vertex 2
    [0, base_size, 0],              # Base vertex 3
    [base_size/2, base_size/2, height - apex_radius]  # Apex vertex 4 (blunted)
])

# Create inner pyramid vertices (scaled down)
inner_scale = (base_size - 2*wall_thickness)/base_size
inner_vertices = outer_vertices.copy()
inner_vertices[:4] *= inner_scale  # Scale base vertices
offset = (base_size - (base_size * inner_scale)) / 2
inner_vertices[:4, :2] += offset

# Define faces for outer pyramid
outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [3, 2, 0],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Define faces for inner pyramid (reversed normals)
inner_faces = np.array([
    [0, 4, 1],  # Front face (reversed)
    [1, 4, 2],  # Right face (reversed)
    [2, 4, 3],  # Back face (reversed)
    [3, 4, 0],  # Left face (reversed)
    [3, 0, 2],  # Base triangle 1 (reversed)
    [0, 1, 2]   # Base triangle 2 (reversed)
])

# Create mesh objects using numpy-stl
outer_mesh = mesh.Mesh(np.zeros(outer_faces.shape[0], dtype=mesh.Mesh.dtype))
inner_mesh = mesh.Mesh(np.zeros(inner_faces.shape[0], dtype=mesh.Mesh.dtype))

for i, f in enumerate(outer_faces):
    outer_mesh.vectors[i] = outer_vertices[f]

for i, f in enumerate(inner_faces):
    inner_mesh.vectors[i] = inner_vertices[f]

# Combine the meshes
combined_mesh = mesh.Mesh(np.concatenate([outer_mesh.data, inner_mesh.data]))

# Create the base to close the pyramid
base_vertices = np.concatenate([outer_vertices[:4], inner_vertices[:4]])
base_faces = np.array([
    [0, 1, 5], [5, 1, 6],
    [1, 2, 6], [6, 2, 7],
    [2, 3, 7], [7, 3, 4],
    [3, 0, 4], [4, 0, 5]
])

base_mesh = mesh.Mesh(np.zeros(base_faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(base_faces):
    base_mesh.vectors[i] = base_vertices[f]

# Combine all parts
final_mesh = mesh.Mesh(np.concatenate([combined_mesh.data, base_mesh.data]))

# Convert to trimesh for validation and repair
tri_mesh = trimesh.Trimesh(vertices=final_mesh.vectors.reshape(-1, 3),
                          faces=np.arange(len(final_mesh.vectors)*3).reshape(-1, 3))

# Validate and repair mesh for 3D printing
tri_mesh.process()  # Merge vertices and remove duplicate faces
tri_mesh.fill_holes()  # Ensure watertightness
tri_mesh.fix_normals()  # Ensure consistent normals

# Check wall thickness
if wall_thickness < 1.0:
    print("Warning: Wall thickness below recommended minimum for FDM printing")

# Save the final mesh
tri_mesh.export('output.stl')