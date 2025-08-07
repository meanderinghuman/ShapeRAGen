import trimesh
import numpy as np

def create_hollow_box(outer_length, outer_width, outer_height, wall_thickness):
    # Validate wall thickness meets minimum requirements
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1.0mm for FDM printing")
    
    # Validate inner dimensions will be positive
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - 2 * wall_thickness
    
    if any(dim <= 0 for dim in [inner_length, inner_width, inner_height]):
        raise ValueError("Wall thickness too large for given outer dimensions")
    
    # Create outer box
    outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))
    
    # Create inner box (hollow space)
    inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))
    
    # Position inner box at center of outer box
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])
    
    # Create hollow box by subtracting inner from outer
    try:
        hollow_box = outer_box.difference(inner_box)
    except Exception as e:
        raise RuntimeError(f"Failed to create hollow box: {str(e)}")
    
    # Ensure the mesh is watertight (important for 3D printing)
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
        hollow_box.fix_normals()
        
        if not hollow_box.is_watertight:
            raise RuntimeError("Failed to create watertight mesh")
    
    return hollow_box

# Example usage
if __name__ == "__main__":
    # Define outer dimensions (mm)
    outer_length = 30
    outer_width = 20
    outer_height = 40
    
    # Set wall thickness (mm) - 1mm is minimum recommended for FDM printing
    wall_thickness = 1.0
    
    try:
        hollow_box = create_hollow_box(outer_length, outer_width, outer_height, wall_thickness)
        hollow_box.export('output.stl')
    except Exception as e:
        print(f"Error creating 3D model: {str(e)}")