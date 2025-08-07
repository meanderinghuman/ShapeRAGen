import trimesh
import numpy as np
from stl import mesh

# Parameters
base_radius = 20.0
height = 35.0
thickness = 2.0
resolution = 50
min_thickness = 0.4  # Minimum printable thickness (0.4mm nozzle)

# Validate thickness
if thickness < min_thickness:
    raise ValueError(f"Thickness must be at least {min_thickness}mm for FDM printing")

# Create outer cone
outer_cone = trimesh.creation.cone(
    radius=base_radius,
    height=height,
    sections=resolution
)

# Create inner cone (smaller radius to create hollow space)
inner_radius = base_radius - thickness
inner_cone = trimesh.creation.cone(
    radius=inner_radius,
    height=height,
    sections=resolution
)

# Create base plate
base_plate = trimesh.creation.cylinder(
    radius=base_radius,
    height=thickness,
    sections=resolution
)
base_plate.apply_translation([0, 0, -thickness])

# Combine meshes
hollow_cone = outer_cone.difference(inner_cone)
final_mesh = trimesh.util.concatenate([hollow_cone, base_plate])

# Ensure the mesh is printable
final_mesh.fill_holes()
final_mesh.fix_normals()

if not final_mesh.is_watertight:
    raise ValueError("Mesh is not watertight and cannot be 3D printed")

# Export as STL
final_mesh.export('output.stl')