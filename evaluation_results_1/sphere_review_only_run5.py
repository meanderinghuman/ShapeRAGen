import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere():
    outer_radius = 45
    wall_thickness = 3
    subdivisions = 3
    
    outer_sphere = trimesh.creation.icosphere(
        subdivisions=subdivisions,
        radius=outer_radius)
    
    inner_sphere = trimesh.creation.icosphere(
        subdivisions=subdivisions,
        radius=outer_radius - wall_thickness)
    
    try:
        hollow_sphere = outer_sphere.difference(inner_sphere)
        hollow_sphere.process()
        
        if not hollow_sphere.is_watertight:
            raise ValueError("Resulting mesh is not watertight")
            
        if hollow_sphere.area < 1e-6:
            raise ValueError("Boolean operation failed - resulting mesh has no volume")
            
        hollow_sphere.export('hollow_sphere_45mm.stl')
        return hollow_sphere
        
    except Exception as e:
        print(f"Error creating hollow sphere: {str(e)}")
        raise

if __name__ == "__main__":
    create_hollow_sphere()