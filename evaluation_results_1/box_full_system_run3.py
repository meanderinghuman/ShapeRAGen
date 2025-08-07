import trimesh
import numpy as np

def create_hollow_box(outer_length=30, outer_width=20, outer_height=40, wall_thickness=1.2):
    # Validate minimum wall thickness for FDM printing
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1.0mm for FDM printing")
    
    # Validate dimensions are positive
    if any(d <= 0 for d in [outer_length, outer_width, outer_height]):
        raise ValueError("All dimensions must be positive values")
        
    # Create outer box
    outer_box = trimesh.creation.box(extents=[outer_length, outer_width, outer_height])
    
    # Calculate inner dimensions (subtracting wall thickness from both sides)
    inner_length = max(0.1, outer_length - 2 * wall_thickness)
    inner_width = max(0.1, outer_width - 2 * wall_thickness)
    inner_height = max(0.1, outer_height - wall_thickness)  # Only subtract from bottom
    
    # Create inner box (offset to maintain wall thickness)
    inner_box = trimesh.creation.box(extents=[inner_length, inner_width, inner_height])
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])
    
    # Create hollow box by subtracting inner from outer
    try:
        hollow_box = outer_box.difference(inner_box)
    except:
        raise RuntimeError("Boolean operation failed - check your dimensions")
    
    # Ensure the mesh is watertight and valid for 3D printing
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
        hollow_box.process()
    
    # Verify minimum thickness
    if hollow_box.extents.min() < 1.0:
        print("Warning: Minimum thickness below recommended 1.0mm in some areas")
    
    return hollow_box

# Create and export the hollow box
hollow_box = create_hollow_box()
hollow_box.export('output.stl')