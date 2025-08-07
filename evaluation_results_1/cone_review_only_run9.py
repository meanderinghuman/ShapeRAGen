import trimesh
import numpy as np

def create_printable_cone():
    # Parameters with explicit units (mm)
    outer_radius = 20
    inner_radius = 18
    height = 35
    wall_thickness = outer_radius - inner_radius
    min_wall_thickness = 1.0
    
    # Validate minimum wall thickness
    if wall_thickness < min_wall_thickness:
        raise ValueError(f"Wall thickness {wall_thickness}mm is below minimum {min_wall_thickness}mm")
    
    # Create cones with slight height difference for better boolean operation
    outer_cone = trimesh.creation.cone(radius=outer_radius, height=height)
    inner_cone = trimesh.creation.cone(radius=inner_radius, height=height-1)
    
    # Create base plate for stability
    base = trimesh.creation.cylinder(radius=outer_radius, height=1)
    base.apply_translation([0, 0, -0.5])  # Center at z=0
    
    # Boolean operations
    hollow_cone = outer_cone.difference(inner_cone)
    final_mesh = hollow_cone.union(base)
    
    # Process mesh for 3D printing
    final_mesh.process(validate=True)
    
    # Additional validation
    if not final_mesh.is_watertight:
        raise ValueError("Mesh is not watertight - not suitable for 3D printing")
    
    # Export
    final_mesh.export('output.stl', file_type='stl')

create_printable_cone()