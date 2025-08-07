import trimesh
import numpy as np

# Create outer cylinder with more segments for smoother surface
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40, segments=64)

# Create inner cylinder with slight offset to ensure clean boolean operation
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40.2, segments=64)
inner_cylinder.apply_translation([0, 0, -0.1])  # Slight Z offset

# Create hollow cylinder by subtracting inner from outer
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Process and validate the mesh
hollow_cylinder.process()
if not hollow_cylinder.is_watertight:
    hollow_cylinder.fill_holes()
    hollow_cylinder.process()

# Verify minimum wall thickness (1mm in this case)
wall_thickness = 15 - 14
assert wall_thickness >= 1.0, "Wall thickness below minimum for FDM printing"

# Export as STL file
hollow_cylinder.export('output.stl')