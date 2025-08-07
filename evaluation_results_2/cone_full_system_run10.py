import trimesh
import numpy as np

# Parameters with explicit units (assuming mm)
outer_radius = 20.0
wall_thickness = 2.0
height = 35.0
base_thickness = 2.0  # Increased for better bed adhesion
sections = 64  # More sections for smoother curves

# Create outer cone
outer_cone = trimesh.creation.cone(
    radius=outer_radius,
    height=height,
    sections=sections
)

# Create inner cone with explicit wall thickness
inner_cone = trimesh.creation.cone(
    radius=outer_radius - wall_thickness,
    height=height - 1.0,  # Slightly shorter
    sections=sections
)

# Position inner cone slightly above base
inner_cone.apply_translation([0, 0, 0.5])

# Create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Process and validate
hollow_cone.fill_holes()
hollow_cone.process(validate=True)

# Add base with more thickness
base = trimesh.creation.cylinder(
    radius=outer_radius,
    height=base_thickness,
    sections=sections
)

# Combine with base
combined = hollow_cone.union(base)

# Final validation
if not combined.is_watertight:
    combined.fill_holes()
if not combined.is_watertight:
    raise ValueError("Mesh is not watertight and cannot be 3D printed")

# Export
combined.export('output.stl')