import trimesh
import numpy as np

def create_hollow_box(outer_length, outer_width, outer_height, wall_thickness):
    # Validate wall thickness
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1.0mm for FDM printing")
    
    # Create outer box
    outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])
    
    # Calculate inner dimensions with safety margin
    inner_length = max(outer_length - 2 * wall_thickness, 0.1)
    inner_width = max(outer_width - 2 * wall_thickness, 0.1)
    inner_height = max(outer_height - 2 * wall_thickness, 0.1)
    
    # Create inner box (hollow space)
    inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])
    
    # Subtract inner box from outer box to create hollow box
    hollow_box = outer_box.difference(inner_box)
    
    # Process and validate mesh
    hollow_box = hollow_box.process()
    
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight - cannot be 3D printed")
    
    return hollow_box

def export_mesh(mesh, filename, file_format='stl'):
    supported_formats = ['stl', 'obj', 'ply']
    if file_format.lower() not in supported_formats:
        raise ValueError(f"Unsupported format. Choose from: {supported_formats}")
    
    mesh.export(filename)

# Example usage
if __name__ == "__main__":
    # Define dimensions (mm)
    outer_length = 30
    outer_width = 20
    outer_height = 40
    wall_thickness = 1.2  # Suitable for FDM printing
    
    try:
        hollow_box = create_hollow_box(outer_length, outer_width, outer_height, wall_thickness)
        export_mesh(hollow_box, 'output.stl')
    except Exception as e:
        print(f"Error creating 3D model: {str(e)}")