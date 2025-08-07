import trimesh
import numpy as np
from stl import mesh

# Parameters with printing considerations
OUTER_RADIUS = 15.0
WALL_THICKNESS = 2.5  # Minimum recommended for FDM printing
HEIGHT = 40.0

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=OUTER_RADIUS, height=HEIGHT)

# Create inner cylinder with proper wall thickness
inner_cylinder = trimesh.creation.cylinder(
    radius=OUTER_RADIUS - WALL_THICKNESS,
    height=HEIGHT
)

# Perform boolean difference with error handling
try:
    hollow_cylinder = outer_cylinder.difference(inner_cylinder)
except Exception as e:
    raise RuntimeError(f"Boolean operation failed: {str(e)}")

# Ensure mesh is printable
hollow_cylinder.fill_holes()
hollow_cylinder.fix_normals()

# Verify mesh is watertight before export
if not hollow_cylinder.is_watertight:
    raise ValueError("Mesh is not watertight - cannot print")

# Export with higher resolution
hollow_cylinder.export('output.stl')