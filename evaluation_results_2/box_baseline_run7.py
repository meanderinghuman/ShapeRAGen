import trimesh
import numpy as np

# Create outer box
outer_box = trimesh.primitives.Box(extents=[30, 20, 40])

# Create inner box (smaller by 2mm in each dimension for wall thickness)
inner_box = trimesh.primitives.Box(extents=[26, 16, 38])

# Position inner box at the center
inner_box.apply_translation([0, 0, 0])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight and correct normals
hollow_box = hollow_box.process()

# Export as STL
hollow_box.export('output.stl')