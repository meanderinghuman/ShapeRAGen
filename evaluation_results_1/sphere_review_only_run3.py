import trimesh
import numpy as np
from stl import mesh

def create_printable_hollow_sphere():
    radius = 45.0
    thickness = 2.0  # minimum recommended wall thickness for FDM printing
    
    # Create spheres with controlled resolution
    outer_sphere = trimesh.creation.icosphere(radius=radius, subdivisions=3)
    inner_sphere = trimesh.creation.icosphere(radius=radius - thickness, subdivisions=3)
    
    # Boolean difference operation with validation
    try:
        hollow_sphere = outer_sphere.difference(inner_sphere)
    except:
        raise ValueError("Boolean operation failed - check mesh validity")
    
    # Process and validate mesh
    hollow_sphere.process(validate=True)
    if not hollow_sphere.is_watertight:
        hollow_sphere.fill_holes()
        hollow_sphere.process(validate=True)
    
    # Verify minimum thickness
    if thickness < 1.0:
        print("Warning: Wall thickness below recommended minimum for FDM printing")
    
    # Verify dimensions
    print(f"Model dimensions (mm): {hollow_sphere.extents}")
    
    # Export
    hollow_sphere.export('output.stl')

create_printable_hollow_sphere()