import trimesh
import numpy as np
from stl import mesh

# Outer pyramid dimensions
base_size = 25.0
height = 30.0
wall_thickness = 2.0  # Adjust wall thickness as needed for printing

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],                    # Base vertex 0
    [base_size, 0, 0],            # Base vertex 1
    [base_size, base_size, 0],    # Base vertex 2
    [0, base_size, 0],            # Base vertex 3
    [base_size/2, base_size/2, height]  # Apex vertex
])

# Create outer pyramid faces (triangles)
outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Create inner pyramid vertices (smaller by wall thickness)
inner_size = base_size - 2 * wall_thickness
inner_height = height - wall_thickness

inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],                    # Base vertex 0
    [inner_size + wall_thickness, wall_thickness, 0],       # Base vertex 1
    [inner_size + wall_thickness, inner_size + wall_thickness, 0],  # Base vertex 2
    [wall_thickness, inner_size + wall_thickness, 0],       # Base vertex 3
    [base_size/2, base_size/2, inner_height]                # Apex vertex
])

# Create inner pyramid faces (inverted normals)
inner_faces = np.array([
    [0, 4, 1],  # Front face (inverted)
    [1, 4, 2],  # Right face (inverted)
    [2, 4, 3],  # Back face (inverted)
    [3, 4, 0],  # Left face (inverted)
    [0, 2, 3],  # Base triangle 1 (inverted)
    [0, 1, 2]   # Base triangle 2 (inverted)
])

# Create meshes
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = trimesh.util.concatenate([outer_mesh, inner_mesh])

# Ensure mesh is watertight and valid for 3D printing
hollow_pyramid.fill_holes()
hollow_pyramid.process()

# Export as STL
hollow_pyramid.export('output.stl')