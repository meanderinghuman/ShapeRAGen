import trimesh
import numpy as np

def create_printable_cone():
    # Parameters with units in mm
    outer_radius = 20.0
    wall_thickness = 2.0
    height = 35.0
    base_thickness = 2.0
    segments = 64  # For smoother curvature
    
    # Create main cone structure
    outer_cone = trimesh.creation.cone(
        radius=outer_radius,
        height=height,
        sections=segments
    )
    
    inner_cone = trimesh.creation.cone(
        radius=outer_radius - wall_thickness,
        height=height - wall_thickness,
        sections=segments
    )
    
    # Create base plate
    base_cylinder = trimesh.creation.cylinder(
        radius=outer_radius,
        height=base_thickness,
        sections=segments
    )
    
    # Position base plate
    base_cylinder.apply_translation([0, 0, -base_thickness])
    
    # Combine components
    hollow_cone = outer_cone.difference(inner_cone)
    final_mesh = hollow_cone.union(base_cylinder)
    
    # Validate mesh for 3D printing
    if not final_mesh.is_watertight:
        final_mesh.fill_holes()
    final_mesh.fix_normals()
    
    # Additional checks
    if final_mesh.volume < 0.1:
        raise ValueError("Mesh volume too small - check dimensions")
    
    if wall_thickness < 1.0:
        print("Warning: Wall thickness below recommended minimum for FDM printing")
    
    # Export with units in mm
    final_mesh.export('printable_cone.stl')

create_printable_cone()