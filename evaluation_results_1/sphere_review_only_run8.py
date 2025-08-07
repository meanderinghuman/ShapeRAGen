import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere():
    radius = 45.0
    thickness = 2.0
    
    outer_sphere = trimesh.creation.icosphere(subdivisions=3, radius=radius)
    inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=radius-thickness)
    
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    hollow_sphere.process()
    hollow_sphere.fill_holes()
    hollow_sphere.fix_normals()
    
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - cannot be 3D printed")
    
    if hollow_sphere.extents.min() < thickness * 0.9:
        raise ValueError("Wall thickness below minimum recommended value")
    
    hollow_sphere.export('output.stl')

create_hollow_sphere()