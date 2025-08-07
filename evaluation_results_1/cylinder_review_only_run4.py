import trimesh
import numpy as np

def create_printable_hollow_cylinder():
    # Define dimensions (all units in mm)
    outer_radius = 15.0
    wall_thickness = 3.0  # Minimum recommended wall thickness for FDM printing
    height = 40.0
    base_thickness = 2.0  # Added base for better print adhesion
    
    # Create outer cylinder
    outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)
    
    # Create inner cylinder with proper wall thickness
    inner_radius = outer_radius - wall_thickness
    inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)
    
    # Create base plate
    base = trimesh.creation.cylinder(radius=outer_radius, height=base_thickness)
    base.apply_translation([0, 0, -base_thickness])
    
    # Combine elements
    hollow_cylinder = outer_cylinder.difference(inner_cylinder)
    final_mesh = trimesh.util.concatenate([hollow_cylinder, base])
    
    # Ensure mesh is watertight and printable
    if not final_mesh.is_watertight:
        final_mesh = final_mesh.fill_holes()
        final_mesh = final_mesh.resolve_self_intersection()
    
    # Export as STL file
    final_mesh.export('output.stl')

create_printable_hollow_cylinder()