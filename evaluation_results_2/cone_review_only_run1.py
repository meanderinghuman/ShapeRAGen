import trimesh
import numpy as np

def create_printable_cone(base_radius=20.0, height=35.0, wall_thickness=1.0):
    MIN_WALL_THICKNESS = 0.8
    
    if wall_thickness < MIN_WALL_THICKNESS:
        raise ValueError(f"Wall thickness must be at least {MIN_WALL_THICKNESS}mm for FDM printing")
    
    outer_cone = trimesh.creation.cone(radius=base_radius, height=height)
    inner_radius = base_radius - wall_thickness
    inner_height = height - wall_thickness
    
    inner_cone = trimesh.creation.cone(radius=inner_radius, height=inner_height)
    inner_cone.apply_translation([0, 0, wall_thickness])
    
    hollow_cone = outer_cone.difference(inner_cone)
    
    if not hollow_cone.is_watertight:
        hollow_cone.fill_holes()
        hollow_cone.process()
    
    if hollow_cone.is_empty:
        raise ValueError("Boolean operation resulted in empty mesh")
    
    if hollow_cone.volume < 0.1:
        raise ValueError("Resulting mesh has negligible volume")
    
    return hollow_cone

hollow_cone = create_printable_cone()
hollow_cone.export('output.stl')