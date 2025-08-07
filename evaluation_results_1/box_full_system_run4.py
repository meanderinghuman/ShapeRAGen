import trimesh
import numpy as np

def create_hollow_box(outer_dimensions, wall_thickness, output_file='output.stl'):
    # Validate wall thickness (minimum 1mm for FDM printing)
    if wall_thickness < 0.001:
        raise ValueError("Wall thickness must be at least 1mm (0.001m) for FDM printing")
    
    # Validate dimensions are positive
    if any(d <= 0 for d in outer_dimensions):
        raise ValueError("All dimensions must be positive")
    
    # Calculate inner dimensions with wall thickness
    inner_dimensions = [
        max(0, outer_dimensions[0] - 2 * wall_thickness),
        max(0, outer_dimensions[1] - 2 * wall_thickness),
        max(0, outer_dimensions[2] - 2 * wall_thickness)
    ]
    
    # Check if inner box would have valid dimensions
    if any(d <= 0 for d in inner_dimensions):
        raise ValueError("Wall thickness too large for given outer dimensions")
    
    # Create boxes
    outer_box = trimesh.primitives.Box(extents=outer_dimensions)
    inner_box = trimesh.primitives.Box(extents=inner_dimensions)
    
    # Create hollow box
    hollow_box = outer_box.difference(inner_box)
    
    # Process mesh to ensure it's printable
    hollow_box.process(validate=True)
    
    # Additional checks for printability
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
        hollow_box.process(validate=True)
    
    # Verify minimum feature size
    if hollow_box.extents.min() < wall_thickness:
        print("Warning: Some features may be smaller than specified wall thickness")
    
    # Export STL
    hollow_box.export(output_file)
    return hollow_box

# Example usage
if __name__ == "__main__":
    outer_dim = [0.020, 0.030, 0.040]  # 20mm × 30mm × 40mm
    wall_thickness = 0.001  # 1mm
    create_hollow_box(outer_dim, wall_thickness)