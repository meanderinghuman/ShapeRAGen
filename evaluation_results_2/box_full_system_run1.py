import trimesh
import numpy as np

def create_hollow_box(outer_length, outer_width, outer_height, wall_thickness):
    # Validate minimum wall thickness for FDM printing
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness below 1.0mm may not be printable with FDM")
    
    # Create outer box
    outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])
    
    # Create inner box dimensions
    inner_length = max(0.1, outer_length - 2 * wall_thickness)
    inner_width = max(0.1, outer_width - 2 * wall_thickness)
    inner_height = max(0.1, outer_height - 2 * wall_thickness)
    
    # Create inner box (hollow space)
    inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])
    
    # Subtract inner box from outer box to create hollow box
    hollow_box = outer_box.difference(inner_box)
    
    # Ensure the mesh is printable
    hollow_box.fill_holes()
    hollow_box.fix_normals()
    
    if not hollow_box.is_watertight:
        raise ValueError("Mesh is not watertight and may not print correctly")
    
    return hollow_box

# Parameters (mm)
outer_length = 30
outer_width = 20
outer_height = 40
wall_thickness = 1.2  # Minimum recommended for FDM

try:
    # Create the hollow box
    model = create_hollow_box(outer_length, outer_width, outer_height, wall_thickness)
    
    # Export as STL
    model.export('output.stl')
    
except ValueError as e:
    print(f"Error creating model: {str(e)}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")