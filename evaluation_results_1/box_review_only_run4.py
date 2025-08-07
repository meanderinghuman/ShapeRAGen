import trimesh
import numpy as np

def create_hollow_box():
    # Define dimensions in millimeters
    box_length = 30
    box_width = 20
    box_height = 40
    wall_thickness = 2  # Minimum recommended for FDM printing
    
    # Create outer box
    outer_mesh = trimesh.creation.box((box_length, box_width, box_height))
    
    # Create inner box (hollow space)
    inner_length = box_length - 2 * wall_thickness
    inner_width = box_width - 2 * wall_thickness
    inner_height = box_height - wall_thickness  # Keep bottom solid
    
    inner_mesh = trimesh.creation.box((inner_length, inner_width, inner_height))
    
    # Position inner box centered in XY and slightly above bottom in Z
    inner_mesh.apply_translation([0, 0, wall_thickness/2])
    
    try:
        # Create hollow box by subtracting inner from outer
        hollow_mesh = outer_mesh.difference(inner_mesh)
        
        # Process mesh to ensure watertightness and correct normals
        hollow_mesh = hollow_mesh.process()
        
        # Verify mesh is suitable for 3D printing
        if not hollow_mesh.is_watertight:
            raise ValueError("Resulting mesh is not watertight")
        if hollow_mesh.volume < 0.1:
            raise ValueError("Resulting mesh has negligible volume")
            
        # Export as STL
        hollow_mesh.export('hollow_box.stl')
        return hollow_mesh
        
    except Exception as e:
        print(f"Error creating hollow box: {str(e)}")
        return None

# Create and export the hollow box
hollow_box = create_hollow_box()