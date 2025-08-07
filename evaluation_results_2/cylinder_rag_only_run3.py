import trimesh
import numpy as np
from stl import mesh

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (with slightly smaller radius for wall thickness)
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40)

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure mesh is watertight and valid for 3D printing
hollow_cylinder.process(validate=True)
hollow_cylinder.fill_holes()

# Export as STL file
hollow_cylinder.export('output.stl')