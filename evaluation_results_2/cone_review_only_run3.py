import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to create wall thickness)
inner_cone = trimesh.creation.cone(radius=18, height=34.9)  # Slightly shorter to ensure manifold mesh

# Hollow out the cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Remove degenerate faces using the updated method
hollow_cone.update_faces(hollow_cone.nondegenerate_faces())

# Ensure mesh is watertight and valid for printing
hollow_cone.fill_holes()
hollow_cone.fix_normals()

# Export as STL
hollow_cone.export('output.stl')