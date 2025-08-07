import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere():
    try:
        outer_sphere = trimesh.creation.icosphere(subdivisions=3, radius=45)
        inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=43)
        
        hollow_sphere = outer_sphere.difference(inner_sphere)
        hollow_sphere = hollow_sphere.process()
        
        if not hollow_sphere.is_watertight:
            raise ValueError("Mesh is not watertight - not suitable for 3D printing")
            
        hollow_sphere.show()
        hollow_sphere.export('hollow_sphere_45mm_2mm_wall.stl')
        
        return hollow_sphere
        
    except Exception as e:
        print(f"Error creating hollow sphere: {str(e)}")
        return None

create_hollow_sphere()