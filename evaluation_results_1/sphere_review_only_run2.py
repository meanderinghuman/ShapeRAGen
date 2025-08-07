import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere():
    # Create outer sphere with explicit minimum wall thickness
    outer_radius = 45.0
    inner_radius = 43.0
    min_wall_thickness = 2.0
    
    if (outer_radius - inner_radius) < min_wall_thickness:
        raise ValueError(f"Wall thickness must be at least {min_wall_thickness}mm")
    
    outer_sphere = trimesh.creation.icosphere(subdivisions=3, radius=outer_radius)
    inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=inner_radius)
    
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    if not hollow_sphere.is_watertight:
        hollow_sphere.fill_holes()
        hollow_sphere.process(validate=True)
    
    hollow_sphere.fix_normals()
    
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight after processing")
    
    return hollow_sphere

hollow_sphere = create_hollow_sphere()
hollow_sphere.export('output.stl')