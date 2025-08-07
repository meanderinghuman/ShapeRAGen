import trimesh
import numpy as np
from stl import mesh

# Create outer box
outer_box = trimesh.primitives.Box(extents=[20, 30, 40])

# Create inner box (offset by 1mm for wall thickness)
inner_box = trimesh.primitives.Box(extents=[18, 28, 38])

# Position inner box in the center of outer box
inner_box.apply_translation([0, 0, 0])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and manifold
hollow_box.fill_holes()
hollow_box.fix_normals()

# Export as STL
hollow_box.export('output.stl')