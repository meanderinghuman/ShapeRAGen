import trimesh
import numpy as np

def create_printable_hollow_cylinder(outer_radius=15.0, height=40.0, wall_thickness=2.0, 
                                   min_wall_thickness=0.4, segments=64):
    # Validate parameters
    if wall_thickness < min_wall_thickness:
        raise ValueError(f"Wall thickness must be at least {min_wall_thickness}mm for FDM printing")
    if outer_radius <= wall_thickness:
        raise ValueError("Outer radius must be greater than wall thickness")
    
    # Create outer cylinder with higher resolution
    outer_cylinder = trimesh.creation.cylinder(
        radius=outer_radius, 
        height=height,
        segments=segments
    )
    
    # Create inner cylinder (hollow part)
    inner_radius = outer_radius - wall_thickness
    inner_cylinder = trimesh.creation.cylinder(
        radius=inner_radius, 
        height=height,
        segments=segments
    )
    
    try:
        # Subtract inner cylinder from outer cylinder to create hollow cylinder
        hollow_cylinder = outer_cylinder.difference(inner_cylinder)
        
        # Ensure mesh is watertight and manifold
        hollow_cylinder.fill_holes()
        hollow_cylinder.process()
        
        if not hollow_cylinder.is_watertight:
            raise ValueError("Resulting mesh is not watertight - not suitable for 3D printing")
            
        return hollow_cylinder
    except Exception as e:
        raise RuntimeError(f"Boolean operation failed: {str(e)}")

# Example usage:
hollow_cylinder = create_printable_hollow_cylinder(
    outer_radius=15.0,
    height=40.0,
    wall_thickness=2.0
)

# Export as binary STL (smaller file size)
hollow_cylinder.export('hollow_cylinder.stl')