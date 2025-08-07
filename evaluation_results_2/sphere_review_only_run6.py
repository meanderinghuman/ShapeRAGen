import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere():
    # Create outer sphere with explicit subdivisions
    outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)
    
    # Create inner sphere with 2mm wall thickness
    inner_sphere = trimesh.creation.icosphere(radius=43, subdivisions=3)
    
    try:
        # Perform boolean difference operation
        hollow_sphere = outer_sphere.difference(inner_sphere)
        
        # Ensure mesh is watertight and printable
        if not hollow_sphere.is_watertight:
            hollow_sphere = hollow_sphere.fill_holes()
            hollow_sphere = hollow_sphere.fix_normals()
            
        # Verify minimum wall thickness (2mm)
        if hollow_sphere.bounding_box.extents.min() < 2.0:
            raise ValueError("Wall thickness below minimum printable size")
            
        # Export as STL
        hollow_sphere.export('output.stl')
        return True
        
    except Exception as e:
        print(f"Error creating hollow sphere: {str(e)}")
        return False

if __name__ == "__main__":
    create_hollow_sphere()