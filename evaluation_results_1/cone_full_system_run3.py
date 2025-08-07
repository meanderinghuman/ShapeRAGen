import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (with slightly smaller radius to make walls)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Hollow out the cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and valid for 3D printing
hollow_cone.process(validate=True)
hollow_cone.fill_holes()

# Add a base plate for better printing stability
base = trimesh.creation.cylinder(radius=20, height=1, sections=64)
base.apply_translation([0, 0, -0.5])  # Center the base at z=0

# Combine the hollow cone with base
final_mesh = trimesh.util.concatenate([hollow_cone, base])

# Ensure normals are consistent for printing
final_mesh.fix_normals()

# Export as STL
final_mesh.export('output.stl')