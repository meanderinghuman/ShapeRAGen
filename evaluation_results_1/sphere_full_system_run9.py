import trimesh
import numpy as np

def create_printable_hollow_sphere(outer_radius=45, wall_thickness=2, subdivisions=4):
    # Validate minimum wall thickness for FDM printing
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1mm for FDM printing")
    
    # Create spheres
    outer_sphere = trimesh.creation.icosphere(radius=outer_radius, subdivisions=subdivisions)
    inner_sphere = trimesh.creation.icosphere(radius=outer_radius - wall_thickness, subdivisions=subdivisions)
    
    # Create hollow sphere
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    # Process mesh for printing
    hollow_sphere.fill_holes()
    hollow_sphere.process()
    
    # Verify mesh is watertight
    if not hollow_sphere.is_watertight:
        raise ValueError("Resulting mesh is not watertight - not suitable for 3D printing")
    
    # Verify volume is positive
    if hollow_sphere.volume <= 0:
        raise ValueError("Resulting mesh has invalid volume")
    
    return hollow_sphere

# Create and export the hollow sphere
hollow_sphere = create_printable_hollow_sphere()
hollow_sphere.export('output.stl')