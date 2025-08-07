import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere():
    outer_radius = 45
    wall_thickness = 3
    subdivisions = 3
    
    sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=outer_radius)
    inner_sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=outer_radius - wall_thickness)
    
    hollow_sphere = sphere.difference(inner_sphere)
    
    hollow_sphere.process()
    hollow_sphere.fill_holes()
    
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - cannot be 3D printed")
    
    if not hollow_sphere.is_winding_consistent:
        hollow_sphere.fix_normals()
    
    hollow_sphere.export('output.stl')

create_hollow_sphere()