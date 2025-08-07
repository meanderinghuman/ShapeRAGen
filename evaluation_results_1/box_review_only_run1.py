import trimesh
import numpy as np

# Dimensions and printing parameters
outer_length = 30
outer_width = 20
outer_height = 40
wall_thickness = 2
bottom_thickness = 2

# Validate minimum wall thickness
if wall_thickness < 1.5:
    raise ValueError("Wall thickness below recommended minimum (1.5mm) for FDM printing")

# Create outer box
outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))

# Calculate inner dimensions
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - bottom_thickness

# Create and position inner box
inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))
inner_box.apply_translation([wall_thickness, wall_thickness, bottom_thickness])

# Perform boolean difference with error handling
try:
    hollow_box = outer_box.difference(inner_box)
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight - not suitable for 3D printing")
    hollow_box.export('output.stl')
except Exception as e:
    print(f"Boolean operation failed: {str(e)}")
    # Fallback to non-hollow version if needed
    outer_box.export('output_solid.stl')