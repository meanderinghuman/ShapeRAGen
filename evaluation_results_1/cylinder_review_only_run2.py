import trimesh
import numpy as np

# Parameters with explicit units (mm)
outer_radius = 15.0
inner_radius = 12.0
height = 40.0
segments = 64  # Higher for smoother circles

# Validate minimum wall thickness (3mm minimum recommended for FDM)
wall_thickness = outer_radius - inner_radius
if wall_thickness < 3.0:
    raise ValueError(f"Wall thickness {wall_thickness}mm is below minimum recommended 3mm")

# Create cylinders with explicit segments and transform
outer_cylinder = trimesh.creation.cylinder(
    radius=outer_radius,
    height=height,
    sections=segments
)

inner_cylinder = trimesh.creation.cylinder(
    radius=inner_radius,
    height=height + 0.2,  # Slightly taller for clean boolean
    sections=segments
)

# Perform boolean difference
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Repair and validate mesh
hollow_cylinder.fill_holes()
hollow_cylinder.fix_normals()

if not hollow_cylinder.is_watertight:
    raise ValueError("Mesh is not watertight - cannot print")

if not hollow_cylinder.is_winding_consistent:
    hollow_cylinder.fix_normals()

# Ensure Z-up orientation
hollow_cylinder.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))

# Export with explicit unit
hollow_cylinder.export('output.stl', file_type='stl_ascii')