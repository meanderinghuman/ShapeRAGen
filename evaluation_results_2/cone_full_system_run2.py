import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (with slightly smaller radius for wall thickness)
inner_cone = trimesh.creation.cone(radius=18, height=34)  # 2mm wall thickness
inner_cone.apply_translation([0, 0, 0.5])  # Slightly raise inner cone to ensure manifold

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and valid for 3D printing
hollow_cone.fill_holes()
hollow_cone.process()

# Export as STL file
hollow_cone.export('output.stl')