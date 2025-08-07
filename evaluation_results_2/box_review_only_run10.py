import trimesh
import numpy as np

def create_hollow_box(length=30, width=20, height=40, wall_thickness=2):
    if wall_thickness < 1:
        raise ValueError("Wall thickness must be at least 1mm for FDM printing")
    
    inner_length = length - 2 * wall_thickness
    inner_width = width - 2 * wall_thickness
    inner_height = height - wall_thickness
    
    if any(d <= 0 for d in [inner_length, inner_width, inner_height]):
        raise ValueError("Wall thickness results in negative inner dimensions")
    
    outer_box = trimesh.primitives.Box(extents=[length, width, height])
    inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])
    inner_box.apply_translation([0, 0, wall_thickness/2])
    
    hollow_box = outer_box.difference(inner_box)
    
    if not hollow_box.is_watertight:
        hollow_box = hollow_box.fill_holes()
        hollow_box = hollow_box.fix_normals()
    
    hollow_box.export('output.stl')
    return hollow_box

hollow_box = create_hollow_box()