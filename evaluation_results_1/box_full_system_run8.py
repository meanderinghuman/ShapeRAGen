import trimesh
import numpy as np

def create_hollow_box(outer_dimensions, wall_thickness):
    outer_box = trimesh.primitives.Box(extents=outer_dimensions)
    inner_dimensions = np.array(outer_dimensions) - 2 * wall_thickness
    inner_box = trimesh.primitives.Box(extents=inner_dimensions)
    hollow_box = outer_box.difference(inner_box)
    
    hollow_box.fill_holes()
    hollow_box.process()
    
    if not hollow_box.is_watertight:
        raise ValueError("Mesh is not watertight - cannot be 3D printed")
    
    return hollow_box

outer_dimensions = [20, 30, 40]
wall_thickness = 2.0

try:
    hollow_box = create_hollow_box(outer_dimensions, wall_thickness)
    
    # Verify minimum wall thickness
    if wall_thickness < 1.0:
        print("Warning: Wall thickness below recommended minimum of 1mm")
    
    # Export directly using trimesh
    hollow_box.export('output.stl')
    
except Exception as e:
    print(f"Error creating 3D model: {str(e)}")