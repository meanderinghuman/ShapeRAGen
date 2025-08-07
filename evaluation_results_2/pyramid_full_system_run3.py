import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid (25x25mm base, 30mm height)
outer_vertices = np.array([
    [0, 0, 0],          # Base vertex 0
    [25, 0, 0],         # Base vertex 1
    [25, 25, 0],        # Base vertex 2
    [0, 25, 0],         # Base vertex 3
    [12.5, 12.5, 30]    # Apex
])

outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Create inner pyramid (smaller dimensions for hollow effect)
wall_thickness = 2.0  # 2mm wall thickness
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [25-wall_thickness, wall_thickness, 0],
    [25-wall_thickness, 25-wall_thickness, 0],
    [wall_thickness, 25-wall_thickness, 0],
    [12.5, 12.5, 30-wall_thickness]  # Slightly lower apex
])

inner_faces = np.array([
    [0, 4, 1],  # Front face (note reversed winding for normals)
    [1, 4, 2],  # Right face
    [2, 4, 3],  # Back face
    [3, 4, 0],  # Left face
    [0, 2, 3],  # Base triangle 1
    [0, 1, 2]   # Base triangle 2
])

# Create mesh objects
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = trimesh.util.concatenate([outer_mesh, inner_mesh])

# Ensure mesh is watertight (important for 3D printing)
hollow_pyramid.fill_holes()
hollow_pyramid.process()

# Export as STL
hollow_pyramid.export('output.stl')