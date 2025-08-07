import trimesh
import numpy as np

# Parameters (all in mm)
OUTER_RADIUS = 15
WALL_THICKNESS = 2
HEIGHT = 40
BASE_THICKNESS = 2

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=OUTER_RADIUS, height=HEIGHT)

# Create inner cylinder (hollow part) with slight height extension for clean boolean
inner_cylinder = trimesh.creation.cylinder(
    radius=OUTER_RADIUS - WALL_THICKNESS,
    height=HEIGHT + 0.1)

# Create base plate
base = trimesh.creation.cylinder(radius=OUTER_RADIUS, height=BASE_THICKNESS)
base.apply_translation([0, 0, -BASE_THICKNESS])

# Subtract inner cylinder from outer cylinder to create hollow shape
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Combine with base plate
model = hollow_cylinder.union(base)

# Validate mesh is watertight
if not model.is_watertight:
    raise ValueError("Model is not watertight - cannot be 3D printed")

# Export the model as STL
model.export('output.stl')