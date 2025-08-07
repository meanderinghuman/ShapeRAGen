import trimesh
import numpy as np
from stl import mesh

# Create outer box
outer_box = trimesh.primitives.Box(extents=[20, 30, 40])

# Create inner box (hollow space) with 2mm wall thickness
inner_box = trimesh.primitives.Box(extents=[16, 26, 38])

# Position inner box centered within outer box
inner_box.apply_translation([0, 0, 0])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight and manifold for printing
hollow_box.fill_holes()
hollow_box.process()

# Export as STL
hollow_box.export('output.stl')