import trimesh
import numpy as np

def create_hollow_box(outer_dimensions, wall_thickness):
    outer_box = trimesh.creation.box(extents=outer_dimensions)
    
    inner_dimensions = np.array(outer_dimensions) - 2 * wall_thickness
    inner_box = trimesh.creation.box(extents=inner_dimensions)
    inner_box.apply_translation([wall_thickness] * 3)
    
    hollow_box = outer_box.difference(inner_box)
    
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
    hollow_box.fix_normals()
    
    return hollow_box

outer_dimensions = [30, 20, 40]
wall_thickness = 2.0

hollow_box = create_hollow_box(outer_dimensions, wall_thickness)

if hollow_box.is_watertight:
    hollow_box.export('output.stl', file_type='stl_ascii')
    print("Mesh exported successfully")
    print(f"Mesh volume: {hollow_box.volume:.2f} mm³")
    print(f"Wall thickness: {wall_thickness} mm (minimum recommended for FDM)")
else:
    print("Error: Mesh is not watertight and cannot be printed")