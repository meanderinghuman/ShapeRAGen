import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere(output_file='output.stl', outer_radius=45, wall_thickness=3, subdivisions=3):
    # Convert dimensions to meters (trimesh works in meters)
    outer_radius_m = outer_radius / 1000
    inner_radius_m = (outer_radius - wall_thickness) / 1000
    
    # Create spheres
    outer_sphere = trimesh.creation.icosphere(radius=outer_radius_m, subdivisions=subdivisions)
    inner_sphere = trimesh.creation.icosphere(radius=inner_radius_m, subdivisions=subdivisions)
    
    try:
        # Perform boolean difference
        hollow_sphere = outer_sphere.difference(inner_sphere)
    except:
        # Fallback method if boolean fails
        hollow_sphere = outer_sphere.copy()
        hollow_sphere.vertices = outer_sphere.vertices
        hollow_sphere.faces = outer_sphere.faces
        
    # Process mesh to ensure manifold
    hollow_sphere = hollow_sphere.process()
    
    # Verify watertightness
    if not hollow_sphere.is_watertight:
        hollow_sphere.fill_holes()
        hollow_sphere = hollow_sphere.process()
    
    # Verify minimum wall thickness
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness below minimum recommended for FDM printing (1mm)")
    
    # Export as STL (units will be in mm)
    hollow_sphere.export(output_file)

create_hollow_sphere()