import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid (base 25mm x 25mm, height 30mm)
outer_pyramid = trimesh.creation.cone(
    radius=12.5,  # half of 25mm
    height=30,
    sections=4  # 4 sides makes a pyramid instead of cone
)

# Create inner pyramid (smaller dimensions to make it hollow)
inner_pyramid = trimesh.creation.cone(
    radius=10,  # thickness of walls will be 2.5mm (12.5 - 10)
    height=28,  # slightly shorter than outer pyramid
    sections=4
)

# Position the inner pyramid slightly above the base to ensure manifold geometry
inner_pyramid.apply_translation([0, 0, 1])

# Subtract inner pyramid from outer pyramid to create hollow pyramid
hollow_pyramid = outer_pyramid.difference(inner_pyramid)

# Ensure the mesh is watertight for 3D printing
hollow_pyramid.fill_holes()
hollow_pyramid.fix_normals()

# Export as STL
hollow_pyramid.export('output.stl')