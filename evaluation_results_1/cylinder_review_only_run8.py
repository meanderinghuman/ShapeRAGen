import trimesh
import numpy as np

def create_printable_hollow_cylinder():
    # Parameters in millimeters
    outer_radius = 15.0
    inner_radius = 12.0
    height = 40.0
    base_thickness = 2.0
    
    # Validate minimum wall thickness (3mm is generally safe for FDM)
    wall_thickness = outer_radius - inner_radius
    if wall_thickness < 3.0:
        raise ValueError(f"Wall thickness {wall_thickness}mm is below recommended minimum of 3mm")
    
    # Create outer cylinder
    outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)
    
    # Create inner cylinder (hollow part)
    inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)
    
    # Create base plate
    base = trimesh.creation.cylinder(radius=outer_radius, height=base_thickness)
    base.apply_translation([0, 0, -base_thickness])
    
    # Boolean operations
    hollow_cylinder = outer_cylinder.difference(inner_cylinder)
    final_mesh = hollow_cylinder.union(base)
    
    # Ensure mesh is watertight
    if not final_mesh.is_watertight:
        final_mesh.fill_holes()
    
    # Export as STL file
    final_mesh.export('output.stl')

create_printable_hollow_cylinder()