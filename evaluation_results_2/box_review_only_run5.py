import trimesh
import numpy as np

def create_printable_hollow_box(length=30.0, width=20.0, height=40.0, wall_thickness=2.0):
    MIN_WALL_THICKNESS = 0.8
    
    if wall_thickness < MIN_WALL_THICKNESS:
        raise ValueError(f"Wall thickness must be ≥{MIN_WALL_THICKNESS}mm for FDM printing")
    
    if any(dim <= 0 for dim in [length, width, height, wall_thickness]):
        raise ValueError("All dimensions must be positive")
    
    outer_box = trimesh.creation.box((length, width, height))
    
    inner_length = max(0.1, length - 2 * wall_thickness)
    inner_width = max(0.1, width - 2 * wall_thickness)
    inner_height = max(0.1, height - wall_thickness)
    inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))
    
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])
    
    hollow_box = outer_box.difference(inner_box)
    
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
        hollow_box.fix_normals()
    
    if not hollow_box.is_watertight:
        raise ValueError("Failed to create watertight mesh")
    
    hollow_box.export('output.stl')
    return hollow_box

hollow_box = create_printable_hollow_box()