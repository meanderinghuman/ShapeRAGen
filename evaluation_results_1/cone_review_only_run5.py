import trimesh
import numpy as np
from stl import mesh

# Parameters
base_radius = 20.0
height = 35.0
wall_thickness = max(1.0, 1.2)  # Enforce minimum wall thickness (1.2mm for FDM)
base_thickness = 2.0  # Thick base for better adhesion
segments = 64  # Number of segments for the circular base

# Create outer cone
outer_cone = trimesh.creation.cone(radius=base_radius, height=height, sections=segments)

# Create inner cone (smaller radius to create hollow space)
inner_radius = base_radius - wall_thickness
inner_height = height - (wall_thickness * (height / base_radius))
inner_cone = trimesh.creation.cone(radius=inner_radius, height=inner_height, sections=segments)

# Position inner cone correctly
inner_cone.apply_translation([0, 0, wall_thickness])

# Create base plate
base_cylinder = trimesh.creation.cylinder(radius=base_radius, height=base_thickness)
base_cylinder.apply_translation([0, 0, -base_thickness/2])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Combine with base plate
model = hollow_cone.union(base_cylinder)

# Create support structure (45 degree rule)
support_height = height * 0.4  # Support for lower 40% of cone
support_thickness = 0.8  # Thinner than walls for easier removal
support_cone = trimesh.creation.cone(
    radius=inner_radius + support_thickness,
    height=support_height,
    sections=segments)
support_cone.apply_translation([0, 0, base_thickness])

# Subtract main model from support to get proper support structure
support = support_cone.difference(trimesh.creation.cone(
    radius=inner_radius,
    height=support_height,
    sections=segments))
support.apply_translation([0, 0, base_thickness])

# Combine model with support
final_model = model.union(support)

# Validate and repair mesh
if not final_model.is_watertight:
    final_model.fill_holes()
    final_model.fix_normals()
    if not final_model.is_watertight:
        final_model = final_model.convex_hull  # Fallback if still not watertight

# Export as STL
final_model.export('output.stl')