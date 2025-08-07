import trimesh
import numpy as np

def create_hollow_sphere(outer_radius=45, wall_thickness=1, subdivisions=4, output_file='output.stl'):
    # Validate parameters
    if wall_thickness < 1:
        raise ValueError("Wall thickness must be at least 1mm for FDM printing")
    
    if outer_radius <= wall_thickness:
        raise ValueError("Outer radius must be greater than wall thickness")
    
    # Create spheres
    outer_sphere = trimesh.creation.icosphere(radius=outer_radius, subdivisions=subdivisions)
    inner_sphere = trimesh.creation.icosphere(radius=outer_radius - wall_thickness, subdivisions=subdivisions)
    
    # Create hollow sphere
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    # Process mesh to ensure watertightness
    hollow_sphere = hollow_sphere.process()
    
    # Validate mesh
    if not hollow_sphere.is_watertight:
        raise ValueError("Resulting mesh is not watertight")
    
    if hollow_sphere.is_empty:
        raise ValueError("Resulting mesh is empty")
    
    # Calculate volume to validate wall thickness
    volume = hollow_sphere.volume
    theoretical_volume = (4/3) * np.pi * (outer_radius**3 - (outer_radius - wall_thickness)**3)
    
    if abs(volume - theoretical_volume) > theoretical_volume * 0.1:
        print("Warning: Actual volume differs significantly from theoretical volume")
    
    # Add a small flat base for better printability
    base = trimesh.creation.cylinder(radius=outer_radius/3, height=1)
    base.apply_translation([0, 0, -outer_radius - 0.5])
    hollow_sphere = hollow_sphere.union(base)
    
    # Export
    hollow_sphere.export(output_file)
    return hollow_sphere

# Example usage
if __name__ == "__main__":
    hollow_sphere = create_hollow_sphere()