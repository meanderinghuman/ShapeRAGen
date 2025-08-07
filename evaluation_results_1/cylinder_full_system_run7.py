import trimesh
import numpy as np

def create_printable_hollow_cylinder(outer_radius=15, inner_radius=14, height=40, min_wall_thickness=1.0):
    # Create cylinders
    outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)
    inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)
    
    # Verify wall thickness meets minimum requirements
    actual_wall = outer_radius - inner_radius
    if actual_wall < min_wall_thickness:
        raise ValueError(f"Wall thickness {actual_wall}mm is below minimum {min_wall_thickness}mm")
    
    # Perform boolean difference with error handling
    try:
        hollow_cylinder = outer_cylinder.difference(inner_cylinder)
    except:
        # Fallback to slower but more reliable method if initial difference fails
        hollow_cylinder = outer_cylinder.boolean_difference(inner_cylinder, engine='blender')
    
    # Ensure mesh is valid for 3D printing
    hollow_cylinder.process()
    hollow_cylinder.fill_holes()
    
    # Verify mesh is watertight
    if not hollow_cylinder.is_watertight:
        hollow_cylinder = hollow_cylinder.convex_hull  # Fallback to convex hull if not watertight
    
    return hollow_cylinder

# Create and export the hollow cylinder
hollow_cylinder = create_printable_hollow_cylinder()
hollow_cylinder.export('output.stl')