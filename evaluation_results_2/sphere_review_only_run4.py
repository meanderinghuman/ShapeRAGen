import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere():
    outer_radius = 45
    wall_thickness = 3
    inner_radius = outer_radius - wall_thickness
    
    outer_mesh = trimesh.creation.icosphere(radius=outer_radius)
    inner_mesh = trimesh.creation.icosphere(radius=inner_radius)
    
    hollow_sphere = outer_mesh.difference(inner_mesh)
    processed_sphere = hollow_sphere.process()
    
    if not processed_sphere.is_watertight:
        raise ValueError("Resulting mesh is not watertight - not suitable for 3D printing")
    
    if wall_thickness < 1.0:
        print("Warning: Wall thickness may be too thin for FDM printing")
    
    processed_sphere.export('hollow_sphere.stl')

create_hollow_sphere()