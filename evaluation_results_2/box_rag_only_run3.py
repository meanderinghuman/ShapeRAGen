import trimesh
import numpy as np
from stl import mesh

# Create outer box
outer_box = trimesh.primitives.Box(extents=[20, 30, 40])

# Create inner box (with 1mm wall thickness)
inner_box = trimesh.primitives.Box(extents=[18, 28, 38])

# Position inner box at the center of outer box
inner_box.apply_translation([0, 0, 0])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and valid for printing
hollow_box.process()

# Export as STL
hollow_box.export('output.stl')