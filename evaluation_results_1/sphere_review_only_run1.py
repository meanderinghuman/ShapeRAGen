import trimesh
import numpy as np

def create_printable_hollow_sphere():
    # Parameters with printability in mind
    outer_radius = 45.0
    wall_thickness = 3.0  # Minimum recommended for FDM
    subdivisions = 3
    
    # Create spheres with sufficient wall thickness
    outer_sphere = trimesh.creation.icosphere(
        subdivisions=subdivisions,
        radius=outer_radius
    )
    inner_sphere = trimesh.creation.icosphere(
        subdivisions=subdivisions,
        radius=outer_radius - wall_thickness
    )
    
    # Perform boolean difference with error handling
    try:
        hollow_sphere = outer_sphere.difference(inner_sphere)
    except Exception as e:
        print(f"Boolean operation failed: {str(e)}")
        return None
    
    # Validate mesh properties
    if not hollow_sphere.is_watertight:
        print("Warning: Mesh is not watertight")
    if not hollow_sphere.is_volume:
        print("Warning: Mesh doesn't form a proper volume")
    
    # Process and repair if needed
    hollow_sphere.process()
    
    # Check minimum feature size
    min_edge_length = hollow_sphere.edges_unique_length.min()
    if min_edge_length < 0.1:
        print(f"Warning: Small features ({min_edge_length:.2f}mm) may not print well")
    
    return hollow_sphere

# Create and export the model
model = create_printable_hollow_sphere()
if model is not None:
    model.export('output.stl')