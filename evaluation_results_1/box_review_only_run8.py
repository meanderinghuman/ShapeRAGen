import trimesh
import numpy as np

# Define dimensions and wall thickness
outer_dimensions = [20, 30, 40]
wall_thickness = 2.0

# Verify minimum wall thickness
if wall_thickness < 2.0:
    raise ValueError("Wall thickness below minimum recommended for FDM printing (2mm)")

# Create boxes with explicit wall thickness
outer_box = trimesh.creation.box(extents=outer_dimensions)
inner_dimensions = np.array(outer_dimensions) - 2 * wall_thickness
inner_box = trimesh.creation.box(extents=inner_dimensions)

# Perform boolean difference with error handling
try:
    hollow_box = outer_box.difference(inner_box)
except Exception as e:
    raise RuntimeError(f"Boolean operation failed: {str(e)}")

# Ensure mesh quality
hollow_box.fill_holes()
hollow_box.fix_normals()

# Verify watertightness before export
if not hollow_box.is_watertight:
    raise ValueError("Mesh is not watertight - not suitable for 3D printing")

# Export with unit information
hollow_box.units = 'mm'
hollow_box.export('output.stl')