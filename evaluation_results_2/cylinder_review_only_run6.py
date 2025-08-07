import trimesh
import numpy as np

# Create outer cylinder with explicit segment count
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40, sections=64)

# Create inner cylinder with slightly smaller radius (2mm wall thickness)
inner_cylinder = trimesh.creation.cylinder(radius=13, height=42, sections=64)

# Position the inner cylinder with Z-offset
inner_cylinder.apply_translation([0, 0, -1])

# Perform boolean difference with validation
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

if hollow_cylinder.is_empty:
    raise ValueError("Boolean difference operation failed")

# Process the mesh
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Verify mesh is watertight before export
if not hollow_cylinder.is_watertight:
    raise ValueError("Mesh is not watertight - not suitable for 3D printing")

# Export as STL file
hollow_cylinder.export('output.stl')