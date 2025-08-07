import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (with slightly smaller radius for wall thickness)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Make the inner cone slightly shorter to ensure manifold geometry
inner_cone.apply_translation([0, 0, 0.1])

# Create the hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and valid for printing
hollow_cone.fill_holes()
hollow_cone.process()

# Export as STL
hollow_cone.export('output.stl')