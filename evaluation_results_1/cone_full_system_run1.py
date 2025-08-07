import numpy as np
import trimesh
from stl import mesh as stl_mesh

# Parameters with validation
outer_radius = 20
height = 35
wall_thickness = 2  # Minimum recommended for FDM printing

# Validate wall thickness
min_wall_thickness = 1.0  # Absolute minimum for most FDM printers
if wall_thickness < min_wall_thickness:
    raise ValueError(f"Wall thickness must be at least {min_wall_thickness}mm for FDM printing")

# Create outer cone
outer_cone = trimesh.creation.cone(radius=outer_radius, height=height)

# Create inner cone (hollow space)
inner_radius = outer_radius - wall_thickness
inner_cone = trimesh.creation.cone(radius=inner_radius, height=height)

# Create base plate with proper thickness and overlap
base_thickness = wall_thickness * 1.5  # Thicker base for stability
base_outer = trimesh.creation.cylinder(radius=outer_radius, height=base_thickness)
base_inner = trimesh.creation.cylinder(radius=inner_radius, height=base_thickness*1.1)  # Slightly taller for clean difference

# Position the base at the bottom of the cone with small overlap
base_overlap = 0.1  # Small overlap to ensure watertight mesh
base_z = -base_thickness/2 - base_overlap
base_outer.apply_translation([0, 0, base_z])
base_inner.apply_translation([0, 0, base_z - base_overlap])

# Combine all parts to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)
base = base_outer.difference(base_inner)
hollow_cone = hollow_cone.union(base)

# Process and validate the mesh
hollow_cone.process()
if not hollow_cone.is_watertight:
    raise ValueError("Mesh is not watertight - cannot be 3D printed")
if not hollow_cone.is_volume:
    raise ValueError("Mesh is not a solid volume - check geometry")

# Convert trimesh to numpy-stl mesh more efficiently
vertices = hollow_cone.vertices
faces = hollow_cone.faces
data = np.zeros(faces.shape[0], dtype=stl_mesh.Mesh.dtype)
data['vectors'] = vertices[faces]
hollow_mesh = stl_mesh.Mesh(data)

# Save the STL file
hollow_mesh.save('hollow_cone.stl')