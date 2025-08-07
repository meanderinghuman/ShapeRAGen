import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (with slightly smaller radius for wall thickness)
inner_cone = trimesh.creation.cone(radius=18, height=34.9)  # 2mm wall thickness
inner_cone.apply_translation([0, 0, 0.05])  # Slight vertical offset

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight for printing
hollow_cone = hollow_cone.process(validate=True)

# Export as STL
hollow_cone.export('output.stl')