import trimesh
import numpy as np

def create_hollow_box(outer_dimensions, wall_thickness):
    outer_box = trimesh.primitives.Box(extents=outer_dimensions)
    inner_dimensions = np.array(outer_dimensions) - 2 * wall_thickness
    inner_box = trimesh.primitives.Box(extents=inner_dimensions)
    hollow_box = outer_box.difference(inner_box)
    
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight - cannot be 3D printed")
        
    min_thickness = 2 * wall_thickness  # Since we subtract from both sides
    if min_thickness < 1.0:
        print(f"Warning: Minimum wall thickness {min_thickness}mm is below recommended 1mm")
    
    return hollow_box

outer_dimensions = [20, 30, 40]
wall_thickness = 2.0  # mm

try:
    hollow_box = create_hollow_box(outer_dimensions, wall_thickness)
    hollow_box.export('output.stl')
except ValueError as e:
    print(f"Error creating printable mesh: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")