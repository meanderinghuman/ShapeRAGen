import trimesh
import numpy as np
from stl import mesh

def create_printable_cone(base_radius=20.0, height=35.0, wall_thickness=1.0, resolution=100):
    # Validate minimum printable thickness
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1.0mm for FDM printing")
    
    # Create outer cone with specified resolution
    outer_cone = trimesh.creation.cone(
        radius=base_radius,
        height=height,
        sections=resolution
    )
    
    # Create inner cone (hollow part)
    inner_radius = base_radius - wall_thickness
    inner_height = height - wall_thickness
    inner_cone = trimesh.creation.cone(
        radius=inner_radius,
        height=inner_height,
        sections=resolution
    )
    
    # Position inner cone to create solid bottom
    inner_cone.apply_translation([0, 0, wall_thickness/2])
    
    # Create hollow cone by subtracting inner from outer
    hollow_cone = outer_cone.difference(inner_cone)
    
    # Process and validate mesh
    hollow_cone.process()
    if not hollow_cone.is_watertight:
        raise ValueError("Generated mesh is not watertight - cannot print")
    
    # Check minimum feature size
    if hollow_cone.extents.min() < 1.0:
        print("Warning: Some features may be too small for reliable printing")
    
    return hollow_cone

# Generate and export the cone
hollow_cone = create_printable_cone()
hollow_cone.export('output.stl')