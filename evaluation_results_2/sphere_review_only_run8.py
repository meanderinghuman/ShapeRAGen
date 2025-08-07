import trimesh
import numpy as np

def create_printable_hollow_sphere():
    outer_radius = 45.0
    wall_thickness = 2.0
    
    sphere = trimesh.creation.icosphere(subdivisions=3, radius=outer_radius)
    inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=outer_radius - wall_thickness)
    hollow_sphere = sphere.difference(inner_sphere)
    
    hollow_sphere.process()
    
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - cannot be 3D printed")
    
    if hollow_sphere.volume < 0.1:
        raise ValueError("Mesh has no volume - check boolean operation")
    
    support = trimesh.creation.box(extents=[100, 100, 5])
    support.apply_translation([0, 0, -outer_radius - 2.5])
    
    combined = hollow_sphere + support
    
    combined.export('hollow_sphere_with_support.stl')

create_printable_hollow_sphere()