import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (hollow part) with slightly smaller radius
inner_cone = trimesh.creation.cone(radius=19, height=34.9)

# Position the inner cone slightly above the base to ensure manifold geometry
inner_cone.apply_translation([0, 0, 0.05])

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and valid for 3D printing
hollow_cone.process(validate=True)

# Export as STL file
hollow_cone.export('output.stl')