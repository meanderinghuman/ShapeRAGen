import trimesh
import numpy as np
from stl import mesh

# Parameters with explicit units (mm)
OUTER_RADIUS = 15.0
WALL_THICKNESS = 2.0  # Minimum recommended for FDM printing
HEIGHT = 40.0
BASE_THICKNESS = 2.0
SEGMENTS = 64  # For smoother curvature

# Create main hollow cylinder
outer_cylinder = trimesh.creation.cylinder(
    radius=OUTER_RADIUS,
    height=HEIGHT + BASE_THICKNESS,
    sections=SEGMENTS
)

inner_cylinder = trimesh.creation.cylinder(
    radius=OUTER_RADIUS - WALL_THICKNESS,
    height=HEIGHT + BASE_THICKNESS + 0.2,  # Extra clearance
    sections=SEGMENTS
)

# Create base plate
base = trimesh.creation.cylinder(
    radius=OUTER_RADIUS,
    height=BASE_THICKNESS,
    sections=SEGMENTS
)

# Combine components
hollow_cylinder = outer_cylinder.difference(inner_cylinder)
final_model = trimesh.util.concatenate([base, hollow_cylinder])

# Validate and repair mesh
if not final_model.is_watertight:
    final_model.fill_holes()
    final_model.process()

assert final_model.is_watertight, "Mesh is not watertight after repair"
assert final_model.volume > 0, "Mesh has invalid volume"

# Export with units in metadata
final_model.export('output.stl', file_type='stl_ascii')