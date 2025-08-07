import trimesh
import numpy as np
from stl import mesh

def create_hollow_box():
    # Define dimensions with validation
    outer_length = 30
    outer_width = 20
    outer_height = 40
    wall_thickness = 2
    
    if wall_thickness < 1.5:
        raise ValueError("Wall thickness below minimum recommended for FDM printing (1.5mm)")
    
    # Create outer box
    outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))
    
    # Create inner box dimensions
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - wall_thickness
    
    # Create and position inner box
    inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])
    
    # Boolean difference with error handling
    try:
        hollow_box = outer_box.difference(inner_box)
        hollow_box.fix_normals()
        hollow_box.fill_holes()
    except Exception as e:
        raise RuntimeError(f"Mesh operation failed: {str(e)}")
    
    # Export with validation
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight - cannot print")
    
    hollow_box.export('output.stl')

create_hollow_box()