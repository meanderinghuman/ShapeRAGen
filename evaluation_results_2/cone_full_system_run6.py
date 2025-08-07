import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius for hollow effect)
inner_cone = trimesh.creation.cone(radius=18, height=34.5)  # Slightly shorter to ensure manifold mesh

# Position inner cone slightly inside outer cone
inner_cone.apply_translation([0, 0, 0.25])  # Small offset to ensure proper thickness

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and suitable for printing
hollow_cone = hollow_cone.process(validate=True)

# Export as STL
hollow_cone.export('output.stl')