import trimesh
import numpy as np

def create_hollow_sphere(outer_radius=45, wall_thickness=2, subdivisions=3):
    inner_radius = outer_radius - wall_thickness
    
    if inner_radius <= 0:
        raise ValueError("Wall thickness cannot exceed outer radius")
    
    outer_sphere = trimesh.creation.icosphere(radius=outer_radius, subdivisions=subdivisions)
    inner_sphere = trimesh.creation.icosphere(radius=inner_radius, subdivisions=subdivisions)
    
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    hollow_sphere = hollow_sphere.process(validate=True)
    
    if not hollow_sphere.is_watertight:
        hollow_sphere.fill_holes()
        hollow_sphere = hollow_sphere.process(validate=True)
    
    if hollow_sphere.volume < 0:
        hollow_sphere.invert()
    
    return hollow_sphere

hollow_sphere = create_hollow_sphere()
hollow_sphere.export('output.stl', file_type='stl_ascii')