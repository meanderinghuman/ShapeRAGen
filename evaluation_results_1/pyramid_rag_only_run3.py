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
    [base_size/2, base_size/2, height]  # Apex
])

# Create inner pyramid vertices (scaled down to create hollow space)
inner_scale = (base_size - 2*wall_thickness) / base_size
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],                      # Base vertex 0
    [base_size - wall_thickness, wall_thickness, 0],          # Base vertex 1
    [base_size - wall_thickness, base_size - wall_thickness, 0],  # Base vertex 2
    [wall_thickness, base_size - wall_thickness, 0],          # Base vertex 3
    [base_size/2, base_size/2, height - wall_thickness]       # Apex
])

# Combine vertices
all_vertices = np.vstack((outer_vertices, inner_vertices))

# Define faces (triangles)
# Outer pyramid faces
outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Inner pyramid faces (inverted normals)
inner_faces = np.array([
    [5, 6, 9],  # Front face (inverted)
    [6, 7, 9],  # Right face (inverted)
    [7, 8, 9],  # Back face (inverted)
    [8, 5, 9],  # Left face (inverted)
    [5, 8, 7],  # Base triangle 1 (inverted)
    [5, 7, 6]   # Base triangle 2 (inverted)
])

# Connecting faces between outer and inner pyramids
connector_faces = np.array([
    [0, 5, 1], [1, 5, 6],
    [1, 6, 2], [2, 6, 7],
    [2, 7, 3], [3, 7, 8],
    [3, 8, 0], [0, 8, 5]
])

# Combine all faces
all_faces = np.vstack((outer_faces, inner_faces, connector_faces))

# Create the mesh
pyramid_mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)

# Ensure the mesh is watertight (important for 3D printing)
pyramid_mesh.fix_normals()
pyramid_mesh.fill_holes()
pyramid_mesh.process()

# Export as STL
pyramid_mesh.export('output.stl')