import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions (20x30x40mm)
outer_dimensions = [20, 30, 40]

# Create inner box dimensions (subtract 2mm from each dimension for 1mm wall thickness)
inner_dimensions = [d - 2 for d in outer_dimensions]

# Create outer and inner boxes
outer_box = trimesh.creation.box(outer_dimensions)
inner_box = trimesh.creation.box(inner_dimensions)

# Position inner box at center of outer box
inner_box.apply_translation([1, 1, 1])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and valid for 3D printing
hollow_box.process()

# Export as STL file
hollow_box.export('output.stl')