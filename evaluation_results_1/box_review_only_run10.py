import trimesh
import numpy as np

def create_hollow_box(outer_length, outer_width, outer_height, wall_thickness):
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1.0mm for FDM printing")
    if any(dim <= 0 for dim in [outer_length, outer_width, outer_height]):
        raise ValueError("All dimensions must be positive")
    if outer_length <= 2 * wall_thickness or outer_width <= 2 * wall_thickness:
        raise ValueError("Outer dimensions must be greater than twice the wall thickness")

    outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - wall_thickness
    
    inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])
    
    hollow_box = outer_box.difference(inner_box)
    hollow_box.fill_holes()
    hollow_box.fix_normals()
    
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight - cannot be 3D printed")
    
    return hollow_box

hollow_box = create_hollow_box(30, 20, 40, 2)
hollow_box.export('output.stl')