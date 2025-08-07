import trimesh
import numpy as np

def create_hollow_box(outer_dimensions, wall_thickness=2.0):
    # Validate wall thickness
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1mm for FDM printing")
    
    # Calculate inner dimensions
    inner_dimensions = np.array(outer_dimensions) - (2 * wall_thickness)
    if any(d <= 0 for d in inner_dimensions):
        raise ValueError("Wall thickness too large for given outer dimensions")
    
    # Create boxes
    outer_box = trimesh.creation.box(extents=outer_dimensions)
    inner_box = trimesh.creation.box(extents=inner_dimensions)
    
    # Create hollow box
    hollow_box = outer_box.difference(inner_box)
    
    # Process mesh
    hollow_box.fill_holes()
    hollow_box.process()
    
    # Validate mesh
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight")
    
    return hollow_box

# Example usage
try:
    hollow_box = create_hollow_box(outer_dimensions=[20, 30, 40], wall_thickness=2.0)
    
    # Export as STL
    hollow_box.export('output.stl')
    
    print("Successfully created hollow box with 2mm walls")
except Exception as e:
    print(f"Error creating hollow box: {str(e)}")