import trimesh
import numpy as np

def create_printable_hollow_box():
    # Dimensions with minimum printable thickness in mind
    outer_length = 30  # x dimension
    outer_width = 20   # y dimension
    outer_height = 40  # z dimension
    wall_thickness = 2  # minimum recommended for FDM
    
    # Validate minimum printable thickness
    if wall_thickness < 1:
        raise ValueError("Wall thickness must be at least 1mm for FDM printing")
    
    # Create inner dimensions (accounting for walls on all sides)
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - wall_thickness  # solid bottom
    
    # Create boxes
    outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))
    inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))
    
    # Position inner box
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])
    
    # Create hollow box
    hollow_box = outer_box.difference(inner_box)
    
    # Process mesh for printing
    hollow_box.fill_holes()
    hollow_box.process()
    
    # Verify mesh is printable
    if not hollow_box.is_watertight:
        raise ValueError("Mesh is not watertight - not suitable for 3D printing")
    
    # Export directly using trimesh
    hollow_box.export('output.stl')

if __name__ == '__main__':
    create_printable_hollow_box()