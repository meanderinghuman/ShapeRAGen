import trimesh
import numpy as np
from stl import mesh

def create_hollow_cone(outer_radius=20, wall_thickness=2, height=35, filename='output.stl'):
    # Calculate inner dimensions with consistent wall thickness
    inner_radius = outer_radius - wall_thickness
    inner_height = height - wall_thickness
    
    # Create cones
    outer_cone = trimesh.creation.cone(radius=outer_radius, height=height)
    inner_cone = trimesh.creation.cone(radius=inner_radius, height=inner_height)
    
    # Create hollow cone
    hollow_cone = outer_cone.difference(inner_cone)
    
    # Process and validate mesh
    hollow_cone.process()
    if not hollow_cone.is_watertight:
        raise ValueError("Mesh is not watertight - not suitable for 3D printing")
    
    # Export with validation
    export_result = hollow_cone.export(filename)
    if not export_result:
        raise IOError(f"Failed to export to {filename}")
    
    return hollow_cone

# Example usage
hollow_cone = create_hollow_cone()