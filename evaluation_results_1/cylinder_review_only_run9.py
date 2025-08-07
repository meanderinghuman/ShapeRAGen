import trimesh
import numpy as np

def create_printable_hollow_cylinder():
    outer_radius = 15.0
    inner_radius = 12.0
    height = 40.0
    base_thickness = 2.0
    
    wall_thickness = outer_radius - inner_radius
    if wall_thickness < 3.0:
        raise ValueError("Wall thickness must be at least 3mm for FDM printing")
    
    outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)
    inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)
    
    base_plate = trimesh.creation.cylinder(radius=outer_radius, height=base_thickness)
    base_plate.apply_translation([0, 0, -base_thickness/2])
    
    hollow_cylinder = outer_cylinder.difference(inner_cylinder)
    final_mesh = hollow_cylinder.union(base_plate)
    
    if not final_mesh.is_watertight:
        raise ValueError("Generated mesh is not watertight - not suitable for 3D printing")
    
    final_mesh.export('hollow_cylinder_with_base.stl')

create_printable_hollow_cylinder()