import trimesh
import numpy as np

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],         # Base vertex 0
    [25, 0, 0],        # Base vertex 1
    [25, 25, 0],       # Base vertex 2
    [0, 25, 0],        # Base vertex 3
    [12.5, 12.5, 30]   # Apex
])

outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)

# Create inner pyramid (smaller version for hollowing)
scale_factor = 0.9  # Makes inner pyramid 90% size of outer
inner_vertices = outer_vertices.copy()
inner_vertices[:-1] = (outer_vertices[:-1] - [12.5, 12.5, 0]) * scale_factor + [12.5, 12.5, 0]
inner_vertices[-1][2] = outer_vertices[-1][2] * 0.95  # Slightly lower apex

inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=outer_faces)

# Make pyramid hollow by subtracting inner mesh
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Ensure the mesh is watertight and valid for printing
hollow_pyramid.fill_holes()
hollow_pyramid.process()

# Export as STL
hollow_pyramid.export('output.stl')