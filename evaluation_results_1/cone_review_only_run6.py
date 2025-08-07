import trimesh
import numpy as np

# Define parameters with explicit wall thickness (3mm for better printability)
outer_radius = 20
wall_thickness = 3
height = 35
base_thickness = 2

# Create outer cone
outer_cone = trimesh.creation.cone(radius=outer_radius, height=height)

# Create inner cone with wall thickness accounted for
inner_cone = trimesh.creation.cone(radius=outer_radius - wall_thickness, 
                                  height=height - wall_thickness)

# Create base cylinder
base = trimesh.creation.cylinder(radius=outer_radius, 
                                height=base_thickness)

# Combine outer cone with base
outer_with_base = outer_cone.union(base)

# Perform difference operation with error handling
try:
    hollow_cone = outer_with_base.difference(inner_cone)
    if not hollow_cone.is_watertight:
        raise ValueError("Resulting mesh is not watertight")
except Exception as e:
    print(f"Boolean operation failed: {str(e)}")
    raise

# Process and validate mesh
hollow_cone.process()
hollow_cone.fill_holes()

# Export the hollow cone
hollow_cone.export('output.stl')