import trimesh
import numpy as np

# Create outer box
outer_box = trimesh.primitives.Box(extents=[30, 20, 40])

# Create inner box (slightly smaller to create walls)
inner_box = trimesh.primitives.Box(extents=[28, 18, 38])

# Subtract inner box from outer box to create hollow box
hollow_box = outer_box.difference(inner_box)

# Export as STL file
hollow_box.export('output.stl')