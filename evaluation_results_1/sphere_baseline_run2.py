import trimesh
import numpy as np
from stl import mesh

# Create a hollow sphere (45mm outer radius, 3mm wall thickness)
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)
inner_sphere = trimesh.creation.icosphere(radius=42, subdivisions=3)
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and valid for 3D printing
hollow_sphere.process()
hollow_sphere.fill_holes()
hollow_sphere.export('output.stl')