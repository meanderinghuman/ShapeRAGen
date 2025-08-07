import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions
outer_dimensions = [0.03, 0.02, 0.04]  # 30mm, 20mm, 40mm (converted to meters)

# Set wall thickness (1.2mm is good for FDM printing)
wall_thickness = 0.0012

# Create inner box dimensions by subtracting wall thickness from each side
inner_dimensions = [d - 2 * wall_thickness for d in outer_dimensions]

# Create the outer and inner boxes
outer_box = trimesh.primitives.Box(extents=outer_dimensions)
inner_box = trimesh.primitives.Box(extents=inner_dimensions)

# Subtract the inner box from the outer box to create a hollow box
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight (important for 3D printing)
hollow_box = hollow_box.process(validate=True)

# Export as STL file
hollow_box.export('output.stl')