import trimesh
import numpy as np

def create_hollow_box(outer_dimensions, wall_thickness=2.0):
    """
    Create a hollow box with specified wall thickness.
    
    Args:
        outer_dimensions: [x, y, z] dimensions of outer box
        wall_thickness: thickness of walls in mm
        
    Returns:
        trimesh.Trimesh: hollow box mesh
    """
    # Validate wall thickness
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1mm for FDM printing")
        
    # Calculate inner dimensions ensuring minimum wall thickness
    inner_dimensions = np.array(outer_dimensions) - (2 * wall_thickness)
    if any(d <= 0 for d in inner_dimensions):
        raise ValueError("Wall thickness too large for given outer dimensions")
    
    # Create meshes
    outer_box = trimesh.primitives.Box(extents=outer_dimensions)
    inner_box = trimesh.primitives.Box(extents=inner_dimensions)
    
    # Create hollow box
    hollow_box = outer_box.difference(inner_box)
    
    # Process mesh to ensure it's printable
    hollow_box.process(validate=True)
    
    # Repair mesh if needed
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
        hollow_box.fix_normals()
    
    return hollow_box

# Example usage
if __name__ == "__main__":
    try:
        # Create hollow box with 20x30x40mm outer dimensions and 2mm walls
        hollow_box = create_hollow_box([20, 30, 40], wall_thickness=2.0)
        
        # Validate minimum thickness (optional - could use trimesh.proximity)
        if hollow_box.bounding_box.primitive.extents.min() < 1.0:
            print("Warning: Some dimensions below minimum printable thickness")
            
        # Export for printing
        hollow_box.export('hollow_box.stl')
        
    except Exception as e:
        print(f"Error creating printable model: {str(e)}")