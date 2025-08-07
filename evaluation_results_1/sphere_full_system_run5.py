import trimesh
import numpy as np

def create_printable_hollow_sphere(outer_radius=45, wall_thickness=2, min_thickness=1):
    # Create spheres
    outer_sphere = trimesh.creation.icosphere(radius=outer_radius)
    inner_sphere = trimesh.creation.icosphere(radius=outer_radius - wall_thickness)
    
    # Create hollow sphere by subtracting inner from outer
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    # Process the mesh to ensure it's manifold
    hollow_sphere = hollow_sphere.process()
    
    # Validate the mesh is watertight
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - not suitable for 3D printing")
        
    # Check if wall thickness meets minimum requirements
    if wall_thickness < min_thickness:
        raise ValueError(f"Wall thickness {wall_thickness}mm is below minimum printable thickness of {min_thickness}mm")
    
    return hollow_sphere

# Create and export the hollow sphere
hollow_sphere = create_printable_hollow_sphere(outer_radius=45, wall_thickness=2, min_thickness=1)
hollow_sphere.export('hollow_sphere.stl', file_type='stl')