import trimesh
import numpy as np

# Create outer cone (radius 20mm, height 35mm)
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (radius 18mm, height 34mm to maintain wall thickness)
inner_cone = trimesh.creation.cone(radius=18, height=34)

# Position inner cone slightly inside the outer cone
inner_cone.apply_translation([0, 0, 0.5])  # 0.5mm offset to maintain bottom thickness

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and valid for 3D printing
hollow_cone = hollow_cone.process()

# Export as STL file
hollow_cone.export('output.stl')