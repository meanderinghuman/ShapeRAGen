import trimesh
import numpy as np
from stl import mesh

base_x = 20
base_y = 30
height = 40
wall_thickness = 2.0
min_wall_thickness = 0.8

if wall_thickness < min_wall_thickness:
    raise ValueError(f"Wall thickness must be at least {min_wall_thickness}mm for FDM printing")

outer_box = trimesh.primitives.Box(extents=[base_x, base_y, height])

inner_x = base_x - 2 * wall_thickness
inner_y = base_y - 2 * wall_thickness
inner_height = height - wall_thickness

if inner_x <= 0 or inner_y <= 0 or inner_height <= 0:
    raise ValueError("Wall thickness too large for given dimensions")

inner_box = trimesh.primitives.Box(extents=[inner_x, inner_y, inner_height])
inner_box.apply_translation([0, 0, wall_thickness/2])

hollow_box = outer_box.difference(inner_box)

if not hollow_box.is_watertight:
    hollow_box.fill_holes()
    hollow_box.fix_normals()

hollow_box.apply_translation([0, 0, -height/2])
hollow_box.export('output.stl', file_type='stl')