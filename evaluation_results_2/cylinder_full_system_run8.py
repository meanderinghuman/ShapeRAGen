import trimesh
import numpy as np

# Parameters with units in millimeters
outer_radius = 15
wall_thickness = 1  # Minimum recommended for FDM printing
height = 40
base_thickness = 2  # For better bed adhesion

# Validate wall thickness
if wall_thickness < 1:
    raise ValueError("Wall thickness must be at least 1mm for FDM printing")

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)

# Create inner cylinder with exact wall thickness
inner_cylinder = trimesh.creation.cylinder(
    radius=outer_radius - wall_thickness,
    height=height + 0.2  # Small overlap to ensure clean boolean
)

# Create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Create base plate
base = trimesh.creation.cylinder(
    radius=outer_radius,
    height=base_thickness,
    sections=64
)

# Combine hollow cylinder with base
model = trimesh.util.concatenate([hollow_cylinder, base])

# Process the mesh
model.process()
model.fill_holes()

# Verify mesh is watertight
if not model.is_watertight:
    raise ValueError("Mesh is not watertight - not suitable for 3D printing")

# Export
model.export('hollow_cylinder_with_base.stl')