import trimesh
import numpy as np

def create_hollow_sphere(output_file='output.stl', radius=45.0, thickness=2.0):
    if thickness < 2.0:
        raise ValueError("Wall thickness should be at least 2mm for FDM printing")
    
    outer_sphere = trimesh.creation.icosphere(radius=radius)
    inner_sphere = trimesh.creation.icosphere(radius=radius - thickness)
    
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    hollow_sphere.process()
    hollow_sphere.fill_holes()
    hollow_sphere.fix_normals()
    
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - cannot be 3D printed")
    
    hollow_sphere.export(output_file)

create_hollow_sphere()