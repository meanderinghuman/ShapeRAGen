import trimesh
import numpy as np

def create_printable_hollow_box():
    # Define dimensions and minimum printable thickness
    outer_dimensions = [20, 30, 40]
    min_wall_thickness = 0.8
    wall_thickness = max(2.0, min_wall_thickness)
    
    # Create outer box
    outer_box = trimesh.creation.box(extents=outer_dimensions)
    
    # Create inner box with proper wall thickness
    inner_dimensions = [
        outer_dimensions[0] - 2 * wall_thickness,
        outer_dimensions[1] - 2 * wall_thickness,
        outer_dimensions[2] - wall_thickness
    ]
    inner_box = trimesh.creation.box(extents=inner_dimensions)
    
    # Position inner box with proper offset
    inner_box.apply_translation([0, 0, wall_thickness/2])
    
    # Create hollow box and ensure it's printable
    hollow_box = outer_box.difference(inner_box)
    
    # Repair mesh for printing
    hollow_box = hollow_box.process(validate=True)
    hollow_box.fix_normals()
    
    # Verify mesh is watertight
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
    
    # Export as STL
    hollow_box.export('output.stl')

create_printable_hollow_box()