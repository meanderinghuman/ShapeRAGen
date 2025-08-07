import trimesh
import numpy as np
from stl import mesh as stl_mesh

base_radius = 20.0
height = 35.0
wall_thickness = 2.0
base_thickness = 2.0

outer_cone = trimesh.creation.cone(radius=base_radius, height=height)
inner_cone = trimesh.creation.cone(radius=base_radius - wall_thickness, 
                                 height=height - wall_thickness)

inner_cone.apply_translation([0, 0, wall_thickness])

base = trimesh.creation.cylinder(radius=base_radius, height=base_thickness)
base.apply_translation([0, 0, -base_thickness/2])

hollow_cone = outer_cone.difference(inner_cone)
model = hollow_cone.union(base)

model = model.process(validate=True)
print(f"Mesh is watertight: {model.is_watertight}")
print(f"Volume: {model.volume:.2f} mm³")

model.export('output.stl')