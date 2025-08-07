import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (slightly smaller to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=34.9)

# Position the inner cone slightly inside the outer cone
inner_cone.apply_translation([0, 0, 0.05])

# Create the hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Clean up the mesh for 3D printing
hollow_cone = hollow_cone.process()
hollow_cone.update_faces(hollow_cone.nondegenerate_faces())
hollow_cone.update_faces(hollow_cone.unique_faces())
hollow_cone.remove_unreferenced_vertices()

# Ensure the mesh is watertight (important for 3D printing)
if not hollow_cone.is_watertight:
    hollow_cone.fill_holes()

# Export as STL
hollow_cone.export('output.stl')