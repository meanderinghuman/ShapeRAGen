import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius for hollow effect)
inner_cone = trimesh.creation.cone(radius=18, height=35)  # 2mm wall thickness

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight for printing
hollow_cone = hollow_cone.process(validate=True)

# Add a base plate for better printability
base = trimesh.creation.cylinder(radius=20, height=1)  # 1mm thick base
base.apply_translation([0, 0, -0.5])  # Center the base at z=0

# Combine cone with base
final_mesh = trimesh.util.concatenate([hollow_cone, base])

# Ensure normals are consistent
final_mesh.fix_normals()

# Export as STL
final_mesh.export('output.stl')