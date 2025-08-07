import trimesh
import numpy as np
from trimesh.repair import fix_normals, fix_inversion

def create_hollow_sphere():
    # Define parameters with explicit units (mm)
    outer_radius = 45.0
    wall_thickness = 2.0
    min_wall_thickness = 1.0
    
    # Validate wall thickness meets minimum requirements
    if wall_thickness < min_wall_thickness:
        raise ValueError(f"Wall thickness {wall_thickness}mm is below minimum {min_wall_thickness}mm")
    
    # Create spheres with higher subdivision for better quality
    outer_sphere = trimesh.creation.icosphere(subdivisions=4, radius=outer_radius)
    inner_sphere = trimesh.creation.icosphere(subdivisions=4, radius=outer_radius - wall_thickness)
    
    # Perform boolean difference with repair steps
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    # Repair mesh for 3D printing
    hollow_sphere.process()
    fix_normals(hollow_sphere)
    fix_inversion(hollow_sphere)
    
    # Verify mesh is watertight
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - not suitable for 3D printing")
    
    # Scale to millimeters (explicit units)
    hollow_sphere.apply_scale(1.0)
    
    return hollow_sphere

# Generate and export the model
model = create_hollow_sphere()
model.export('hollow_sphere.stl', file_type='stl')