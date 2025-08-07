import trimesh
import numpy as np

# Parameters with validation
outer_radius = 15.0
height = 40.0
thickness = max(2.0, 1.0)  # Ensure minimum wall thickness of 1.0mm
inner_radius = outer_radius - thickness
base_thickness = 2.0
resolution = 64  # Number of segments for circular parts

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(
    radius=outer_radius,
    height=height,
    sections=resolution
)

# Create inner cylinder (hollow part)
inner_cylinder = trimesh.creation.cylinder(
    radius=inner_radius,
    height=height,
    sections=resolution
)

# Create base plate
base = trimesh.creation.cylinder(
    radius=outer_radius,
    height=base_thickness
)

# Perform boolean operations with error handling
try:
    hollow_cylinder = outer_cylinder.difference(inner_cylinder)
    final_mesh = hollow_cylinder.union(base)
except Exception as e:
    print(f"Boolean operation failed: {str(e)}")
    raise

# Check mesh validity
if not final_mesh.is_watertight:
    print("Warning: Mesh is not watertight - may cause printing issues")

# Export as STL
final_mesh.export('output.stl')