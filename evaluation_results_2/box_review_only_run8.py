import trimesh
import numpy as np

# Define dimensions (mm)
length = 30
width = 20
height = 40
wall_thickness = 2  # Minimum recommended for FDM printing

# Validate wall thickness
if wall_thickness < 1:
    raise ValueError("Wall thickness must be at least 1mm for FDM printing")

# Calculate inner dimensions
inner_length = length - 2 * wall_thickness
inner_width = width - 2 * wall_thickness
inner_height = height - wall_thickness

# Validate inner dimensions
if any(d <= 0 for d in [inner_length, inner_width, inner_height]):
    raise ValueError("Inner dimensions must be positive - adjust wall thickness or overall size")

# Create outer box
outer_box = trimesh.creation.box((length, width, height))

# Create inner box (hollow space)
inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))

# Position inner box centered within outer box
inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight
hollow_box = hollow_box.process(validate=True)
hollow_box.fill_holes()

# Export as STL
hollow_box.export('output.stl')