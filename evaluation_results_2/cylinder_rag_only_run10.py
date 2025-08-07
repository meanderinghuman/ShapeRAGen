import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Parameters
outer_radius = 15.0  # mm
wall_thickness = 2.0  # mm (recommended for FDM printing)
height = 40.0  # mm
segments = 64  # Number of segments for smoothness

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(
    radius=outer_radius,
    height=height,
    sections=segments
)

# Create inner cylinder (hollow part)
inner_radius = outer_radius - wall_thickness
inner_cylinder = trimesh.creation.cylinder(
    radius=inner_radius,
    height=height,
    sections=segments
)

# Combine to make hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure mesh is watertight (important for 3D printing)
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL
hollow_cylinder.export('output.stl')