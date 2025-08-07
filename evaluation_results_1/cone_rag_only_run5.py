import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=34.9)  # Slightly shorter to ensure manifold mesh

# Position the inner cone slightly inside the outer cone
inner_cone.apply_translation([0, 0, 0.05])

# Create the hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and manifold
hollow_cone.process()

# Add a base to make it printable
base = trimesh.creation.cylinder(radius=20, height=1)
hollow_cone = hollow_cone.union(base)

# Export as STL
hollow_cone.export('output.stl')