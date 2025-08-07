import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (90% of outer radius, 95% of height for wall thickness)
inner_cone = trimesh.creation.cone(radius=18, height=33.25)

# Position inner cone slightly above base to create bottom thickness
inner_cone.apply_translation([0, 0, 1.75])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and valid for printing
hollow_cone.process(validate=True)
hollow_cone.fill_holes()

# Export as STL
hollow_cone.export('output.stl')