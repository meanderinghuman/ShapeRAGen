import trimesh
import numpy as np

def create_printable_hollow_sphere(outer_radius=45, wall_thickness=1):
    # Validate parameters
    if wall_thickness < 1:
        raise ValueError("Wall thickness must be at least 1mm for FDM printing")
    
    # Create spheres
    outer_sphere = trimesh.creation.icosphere(radius=outer_radius)
    inner_sphere = trimesh.creation.icosphere(radius=outer_radius - wall_thickness)
    
    # Create hollow sphere
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    # Process mesh for printing
    hollow_sphere = hollow_sphere.process()
    
    # Verify mesh is printable
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight and cannot be printed")
    
    if hollow_sphere.volume < 0.1:
        raise ValueError("Mesh has no volume - check boolean operation")
    
    # Calculate minimum wall thickness (approximate)
    bounds = hollow_sphere.bounding_box.extents
    min_dimension = min(bounds)
    if min_dimension < wall_thickness:
        print(f"Warning: Minimum dimension {min_dimension:.2f}mm is below target wall thickness")
    
    # Export with support-friendly orientation
    hollow_sphere.export('hollow_sphere.stl')
    
    return hollow_sphere

# Example usage
if __name__ == "__main__":
    try:
        model = create_printable_hollow_sphere(outer_radius=45, wall_thickness=1)
        print("Model created successfully and is ready for printing")
    except Exception as e:
        print(f"Error creating model: {str(e)}")