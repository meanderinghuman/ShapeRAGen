import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere():
    # Create outer sphere (45mm radius)
    outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)
    
    # Create inner sphere (43mm radius for 2mm wall thickness)
    inner_sphere = trimesh.creation.icosphere(radius=43, subdivisions=3)
    
    # Create hollow sphere by subtracting inner from outer
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    # Process mesh to ensure watertight and correct normals
    hollow_sphere.process()
    
    # Add a small vent hole (4mm diameter) to prevent pressure buildup
    vent_cylinder = trimesh.creation.cylinder(radius=2, height=10)
    vent_cylinder.apply_translation([45, 0, 0])
    hollow_sphere = hollow_sphere.difference(vent_cylinder)
    
    # Verify mesh is watertight
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - cannot be 3D printed")
    
    # Export as STL
    hollow_sphere.export('output.stl')

create_hollow_sphere()