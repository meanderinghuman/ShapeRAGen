import trimesh
import numpy as np

def create_hollow_sphere():
    outer_radius = 45.0
    inner_radius = 43.0
    min_wall_thickness = 2.0
    
    outer_sphere = trimesh.creation.icosphere(radius=outer_radius, subdivisions=3)
    inner_sphere = trimesh.creation.icosphere(radius=inner_radius, subdivisions=3)
    
    hollow_sphere = outer_sphere.difference(inner_sphere)
    hollow_sphere.process()
    
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - not suitable for 3D printing")
    
    if (outer_radius - inner_radius) < min_wall_thickness:
        raise ValueError(f"Wall thickness below minimum {min_wall_thickness}mm requirement")
    
    hollow_sphere.export('hollow_sphere.stl')
    return hollow_sphere

if __name__ == "__main__":
    create_hollow_sphere()