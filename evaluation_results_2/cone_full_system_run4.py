import trimesh
import numpy as np

def create_printable_cone():
    # Create outer cone with validated dimensions
    outer_radius = 20
    inner_radius = 18
    height = 35
    wall_thickness = outer_radius - inner_radius
    
    # Validate minimum wall thickness for FDM printing
    if wall_thickness < 2:
        raise ValueError("Wall thickness must be at least 2mm for FDM printing")
    
    # Create cones with slight overlap to ensure manifold
    outer_cone = trimesh.creation.cone(radius=outer_radius, height=height)
    inner_cone = trimesh.creation.cone(radius=inner_radius, height=height-0.5)
    
    # Position inner cone slightly inside outer cone
    inner_cone.apply_translation([0, 0, 0.25])
    
    # Create hollow cone
    hollow_cone = outer_cone.difference(inner_cone)
    
    # Create base with extra margin for better adhesion
    base_radius = outer_radius + 2
    base = trimesh.creation.cylinder(radius=base_radius, height=1)
    base.apply_translation([0, 0, -0.5])  # Position below cone
    
    # Combine cone and base
    model = hollow_cone.union(base)
    
    # Thorough mesh repair
    model.process(validate=True)
    model.fill_holes()
    model.remove_unreferenced_vertices()
    model.merge_vertices()
    model.fix_normals()
    
    # Verify mesh is solid and printable
    if not model.is_watertight:
        raise ValueError("Mesh is not watertight - cannot be 3D printed")
    if model.volume < 0.1:
        raise ValueError("Mesh volume too small - check geometry")
    
    return model

# Create and export model
printable_cone = create_printable_cone()
printable_cone.export('hollow_cone.stl')