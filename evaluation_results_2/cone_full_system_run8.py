import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (with slightly smaller radius to make walls 2mm thick)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and valid for 3D printing
hollow_cone.process(validate=True)
hollow_cone.fill_holes()

# Export as STL file
hollow_cone.export('output.stl')