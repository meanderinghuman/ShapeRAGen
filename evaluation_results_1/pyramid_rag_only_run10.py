import numpy as np
import trimesh
from stl import mesh

# Outer pyramid dimensions
base_size = 25.0
height = 30.0
wall_thickness = 2.0  # Adjust based on your printer's capabilities

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],                      # Base vertex 0
    [base_size, 0, 0],              # Base vertex 1
    [base_size, base_size, 0],      # Base vertex 2
    [0, base_size, 0],              # Base vertex 3
    [base_size/2, base_size/2, height]  # Apex vertex 4
])

# Create inner pyramid vertices (scaled down)
inner_scale = (base_size - 2*wall_thickness) / base_size
inner_vertices = outer_vertices.copy()
inner_vertices[:4] *= inner_scale  # Scale base vertices
inner_vertices[:4] += [wall_thickness, wall_thickness, 0]  # Offset to center
inner_vertices[4][2] = height - wall_thickness  # Adjust apex height

# Combine all vertices
all_vertices = np.vstack([outer_vertices, inner_vertices])

# Define faces for the pyramid (each face is a triangle)
faces = [
    # Outer pyramid faces
    [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],
    # Inner pyramid faces (inverted)
    [5, 6, 9], [6, 7, 9], [7, 8, 9], [8, 5, 9],
    # Base faces (top and bottom)
    [0, 1, 2], [0, 2, 3],  # Outer base
    [5, 6, 7], [5, 7, 8],  # Inner base
    # Side walls
    [0, 5, 1], [1, 5, 6],
    [1, 6, 2], [2, 6, 7],
    [2, 7, 3], [3, 7, 8],
    [3, 8, 0], [0, 8, 5]
]

# Create the mesh
pyramid_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        pyramid_mesh.vectors[i][j] = all_vertices[f[j], :]

# Save the STL file
pyramid_mesh.save('output.stl')

# Optional: Use trimesh for additional processing/validation
mesh_trimesh = trimesh.Trimesh(vertices=all_vertices, faces=faces)
if not mesh_trimesh.is_watertight:
    print("Warning: Mesh is not watertight - may not print correctly")
else:
    print("Mesh is watertight and ready for printing")