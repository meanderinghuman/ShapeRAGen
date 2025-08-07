import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (hollow part) with slightly smaller radius
inner_cone = trimesh.creation.cone(radius=18, height=34)

# Position the inner cone slightly inside the outer cone
inner_cone.apply_translation([0, 0, 0.5])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and manifold
hollow_cone.process()

# Export as STL file
hollow_cone.export('output.stl')