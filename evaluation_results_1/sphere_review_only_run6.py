import trimesh
import numpy as np

def create_hollow_sphere(outer_radius=45.0, wall_thickness=2.0, subdivisions=4):
    outer_sphere = trimesh.creation.icosphere(radius=outer_radius, subdivisions=subdivisions)
    inner_sphere = trimesh.creation.icosphere(
        radius=outer_radius - wall_thickness,
        subdivisions=subdivisions
    )
    hollow_sphere = outer_sphere.difference(inner_sphere)
    hollow_sphere = hollow_sphere.process()
    
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - not suitable for 3D printing")
    
    if wall_thickness < 1.5:
        print("Warning: Wall thickness below recommended minimum for FDM printing")
    
    return hollow_sphere

hollow_sphere = create_hollow_sphere()
hollow_sphere.export('hollow_sphere_45mm_2mm_wall.stl')