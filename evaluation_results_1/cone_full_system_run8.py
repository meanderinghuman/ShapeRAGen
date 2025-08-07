import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (with slightly smaller radius for wall thickness)
inner_cone = trimesh.creation.cone(radius=18, height=34.9)  # 2mm wall thickness

# Position inner cone slightly inside outer cone
inner_cone.apply_translation([0, 0, 0.05])  # Small offset to prevent z-fighting

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and valid for printing
hollow_cone.process(validate=True)

# Export as STL
hollow_cone.export('output.stl')