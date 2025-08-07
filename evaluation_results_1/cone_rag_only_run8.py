import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius for hollow effect)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Add a base to make it printable (optional but recommended)
base = trimesh.creation.cylinder(radius=20, height=1)
base.apply_translation([0, 0, -0.5])  # Position at bottom
hollow_cone = hollow_cone.union(base)

# Clean up the mesh for printing
hollow_cone = hollow_cone.process(validate=True)
hollow_cone.update_faces(hollow_cone.nondegenerate_faces())
hollow_cone.update_faces(hollow_cone.unique_faces())
hollow_cone.remove_unreferenced_vertices()

# Export as STL
hollow_cone.export('output.stl')