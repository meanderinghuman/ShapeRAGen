import trimesh
import numpy as np

# Parameters with better printing defaults
outer_radius = 15.0  # mm
wall_thickness = 2.0  # mm (minimum recommended for FDM printing)
inner_radius = outer_radius - wall_thickness
height = 40.0  # mm
base_thickness = 2.0  # mm for better bed adhesion

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)

# Create inner cylinder (with proper wall thickness)
inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)

# Create hollow cylinder by subtracting inner from outer
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Create base plate
base = trimesh.creation.cylinder(radius=outer_radius, height=base_thickness)
base.apply_translation([0, 0, -base_thickness])

# Combine hollow cylinder with base
model = hollow_cylinder.union(base)

# Validate and repair mesh
if not model.is_watertight:
    model.fill_holes()
    model.process()

# Verify minimum wall thickness
if wall_thickness < 1.5:
    print("Warning: Wall thickness may be too thin for reliable FDM printing")

# Export with proper settings
model.export('output.stl', file_type='stl_ascii')