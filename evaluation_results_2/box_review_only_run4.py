import trimesh
import numpy as np
from stl import mesh

def create_hollow_box():
    # Dimensions in mm
    outer_dimensions = [30, 20, 40]
    min_wall_thickness = 1.0  # Minimum for FDM printing
    wall_thickness = 2.0
    
    # Validate wall thickness
    if wall_thickness < min_wall_thickness:
        raise ValueError(f"Wall thickness must be at least {min_wall_thickness}mm for FDM printing")
    
    # Calculate inner dimensions
    inner_dimensions = [
        outer_dimensions[0] - 2 * wall_thickness,
        outer_dimensions[1] - 2 * wall_thickness,
        outer_dimensions[2] - wall_thickness  # Keep bottom solid
    ]
    
    # Validate inner dimensions
    if any(d <= 0 for d in inner_dimensions):
        raise ValueError("Inner dimensions would be negative or zero with current wall thickness")
    
    # Create outer box
    outer_box = trimesh.creation.box(outer_dimensions)
    
    # Create inner box (offset to keep bottom aligned)
    inner_box = trimesh.creation.box(inner_dimensions)
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])
    
    # Create hollow box by subtracting inner from outer
    hollow_box = outer_box.difference(inner_box)
    
    # Verify mesh is watertight before export
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight and may not print correctly")
    
    # Export as STL
    hollow_box.export('output.stl')

create_hollow_box()