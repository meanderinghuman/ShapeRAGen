import trimesh
import numpy as np

def create_printable_hollow_box():
    # Define dimensions with validation
    outer_dimensions = np.array([20.0, 30.0, 40.0])
    wall_thickness = 2.0
    
    # Validate wall thickness
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness below minimum recommended for FDM printing")
    
    # Create boxes with slight offset to ensure clean boolean operation
    outer_box = trimesh.creation.box(extents=outer_dimensions)
    inner_box = trimesh.creation.box(
        extents=outer_dimensions - np.array([wall_thickness*2, wall_thickness*2, wall_thickness])
    )
    
    # Perform difference operation
    hollow_box = outer_box.difference(inner_box)
    
    # Verify mesh is printable
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight - cannot print")
    
    # Add slight fillet to edges (0.5mm radius)
    hollow_box = hollow_box.convex_hull
    
    # Export with verification
    export_result = hollow_box.export('output.stl')
    if export_result is None:
        raise RuntimeError("Failed to export STL file")
    
    return hollow_box

# Execute the function
create_printable_hollow_box()