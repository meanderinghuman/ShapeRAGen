import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (slightly smaller to create wall thickness)
inner_cone = trimesh.creation.cone(radius=18, height=34.5)

# Move inner cone up slightly to ensure proper wall thickness
inner_cone.apply_translation([0, 0, 0.25])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Clean up the mesh for 3D printing
hollow_cone = hollow_cone.process(validate=True)
hollow_cone.remove_unreferenced_vertices()
hollow_cone.update_faces(hollow_cone.nondegenerate_faces())
hollow_cone.update_faces(hollow_cone.unique_faces())

# Ensure mesh is watertight (important for 3D printing)
if not hollow_cone.is_watertight:
    hollow_cone.fill_holes()

# Export as STL
hollow_cone.export('output.stl')