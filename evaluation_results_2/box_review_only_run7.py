import trimesh
import numpy as np

def create_hollow_box():
    outer_dimensions = [30, 20, 40]
    wall_thickness = 2
    
    outer_box = trimesh.primitives.Box(extents=outer_dimensions)
    
    inner_dimensions = [
        outer_dimensions[0] - 2 * wall_thickness,
        outer_dimensions[1] - 2 * wall_thickness,
        outer_dimensions[2] - 2 * wall_thickness
    ]
    
    inner_box = trimesh.primitives.Box(extents=inner_dimensions)
    
    hollow_box = outer_box.difference(inner_box)
    
    if not hollow_box.is_watertight:
        hollow_box = hollow_box.fill_holes()
        hollow_box = hollow_box.fix_normals()
    
    if hollow_box.is_watertight:
        hollow_box.export('hollow_box.stl', file_type='stl')
        return True
    else:
        print("Error: Resulting mesh is not watertight and cannot be printed")
        return False

if __name__ == "__main__":
    create_hollow_box()