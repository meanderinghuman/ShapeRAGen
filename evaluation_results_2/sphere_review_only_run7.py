import trimesh
import numpy as np
from stl import mesh

def create_printable_hollow_sphere():
    try:
        sphere = trimesh.creation.icosphere(subdivisions=3, radius=45)
        inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=43)
        hollow_sphere = sphere.difference(inner_sphere)
        
        hollow_sphere.fill_holes()
        hollow_sphere = hollow_sphere.process(validate=True)
        
        if not hollow_sphere.is_watertight:
            raise ValueError("Mesh is not watertight after processing")
            
        if hollow_sphere.area < 1e-6:
            raise ValueError("Mesh has zero area after processing")
            
        hollow_sphere.export('output.stl')
        return hollow_sphere
        
    except Exception as e:
        print(f"Error creating printable model: {str(e)}")
        raise

if __name__ == "__main__":
    create_printable_hollow_sphere()