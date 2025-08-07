import trimesh
import numpy as np
from stl import mesh

MIN_WALL_THICKNESS = 1.0  # mm

outer_length_mm = 30
outer_width_mm = 20
outer_height_mm = 40
wall_thickness_mm = 2

if wall_thickness_mm < MIN_WALL_THICKNESS:
    raise ValueError(f"Wall thickness must be at least {MIN_WALL_THICKNESS}mm for FDM printing")

outer_box = trimesh.creation.box((outer_length_mm, outer_width_mm, outer_height_mm))

inner_length_mm = outer_length_mm - 2 * wall_thickness_mm
inner_width_mm = outer_width_mm - 2 * wall_thickness_mm
inner_height_mm = outer_height_mm - wall_thickness_mm

inner_box = trimesh.creation.box((inner_length_mm, inner_width_mm, inner_height_mm))
inner_box.apply_translation([wall_thickness_mm, wall_thickness_mm, wall_thickness_mm])

try:
    hollow_box = outer_box.difference(inner_box)
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight - not suitable for 3D printing")
    hollow_box.export('output.stl')
except Exception as e:
    print(f"Error during mesh operation: {str(e)}")
    raise