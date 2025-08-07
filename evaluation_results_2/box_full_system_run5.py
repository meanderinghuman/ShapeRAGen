import trimesh
import numpy as np
from stl import mesh

def create_hollow_box():
    # Dimensions in mm
    outer_length = 30
    outer_width = 20
    outer_height = 40
    wall_thickness = 1.2  # Recommended minimum for FDM printing
    
    # Validate minimum wall thickness
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness below 1.0mm may not be printable")

    # Calculate inner dimensions
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - 2 * wall_thickness

    # Create boxes
    outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))
    inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))
    
    # Position inner box
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

    # Create hollow box
    hollow_box = outer_box.difference(inner_box)

    # Repair mesh
    hollow_box.fill_holes()
    hollow_box.fix_normals()
    
    # Validate mesh
    if not hollow_box.is_watertight:
        raise ValueError("Mesh is not watertight - cannot be 3D printed")
    if hollow_box.volume < 0.1:
        raise ValueError("Mesh has degenerate volume")

    # Export STL using trimesh's built-in exporter (more reliable)
    hollow_box.export('output.stl')

if __name__ == '__main__':
    create_hollow_box()