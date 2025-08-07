import trimesh
import numpy as np

# Create outer cone with parameters
outer_radius = 20
inner_radius = 18
height = 35
min_wall_thickness = 1.0  # Minimum recommended wall thickness for FDM printing

# Validate wall thickness
wall_thickness = outer_radius - inner_radius
if wall_thickness < min_wall_thickness:
    raise ValueError(f"Wall thickness {wall_thickness}mm is below minimum recommended {min_wall_thickness}mm")

# Create cones with additional segments for better print quality
outer_cone = trimesh.creation.cone(radius=outer_radius, height=height, segments=64)
inner_cone = trimesh.creation.cone(radius=inner_radius, height=height, segments=64)

# Create a base plate for stability
base = trimesh.creation.cylinder(radius=outer_radius, height=2, sections=64)
base.apply_translation([0, 0, -1])  # Position below the cone

# Perform boolean operations with padding
hollow_cone = outer_cone.difference(inner_cone)

# Combine with base plate
final_mesh = trimesh.util.concatenate([hollow_cone, base])

# Process and validate mesh
final_mesh.process()
if not final_mesh.is_watertight:
    final_mesh.fill_holes()
    final_mesh.process()

# Verify mesh is printable
if not final_mesh.is_watertight:
    raise ValueError("Mesh is not watertight and cannot be 3D printed")

if final_mesh.volume < 0.1:
    raise ValueError("Mesh has no volume - boolean operation may have failed")

# Export as binary STL for smaller file size
final_mesh.export('hollow_cone_with_base.stl')