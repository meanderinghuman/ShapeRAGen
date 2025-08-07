import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (slightly smaller to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=34)

# Align both cones
inner_cone.apply_translation([0, 0, 0.5])  # Slightly raise inner cone

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Clean up the mesh (using non-deprecated method)
hollow_cone.update_faces(hollow_cone.nondegenerate_faces())

# Ensure mesh is watertight and valid for printing
hollow_cone.fill_holes()
hollow_cone.process()

# Export as STL
hollow_cone.export('output.stl')