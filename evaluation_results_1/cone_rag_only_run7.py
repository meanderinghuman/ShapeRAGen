import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius for wall thickness)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Make the inner cone hollow by flipping its normals
inner_cone.invert()

# Combine the outer and inner cones to create a hollow cone
hollow_cone = outer_cone + inner_cone

# Clean up the mesh for better 3D printing
hollow_cone = hollow_cone.process(validate=True)
hollow_cone.remove_unreferenced_vertices()
hollow_cone.update_faces(hollow_cone.nondegenerate_faces())
hollow_cone.update_faces(hollow_cone.unique_faces())

# Ensure the mesh is watertight (important for 3D printing)
hollow_cone.fill_holes()

# Export the hollow cone as an STL file
hollow_cone.export('output.stl')