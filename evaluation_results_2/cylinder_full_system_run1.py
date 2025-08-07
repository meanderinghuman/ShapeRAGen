import trimesh
import numpy as np

def create_printable_hollow_cylinder(outer_radius=15.0, inner_radius=14.0, height=40.0):
    # Validate minimum wall thickness (typically 0.8mm for FDM)
    min_wall_thickness = 0.8
    if (outer_radius - inner_radius) < min_wall_thickness:
        raise ValueError(f"Wall thickness must be at least {min_wall_thickness}mm")
    
    try:
        # Create the outer and inner cylinders
        outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)
        inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)
        
        # Perform boolean difference operation
        hollow_cylinder = outer_cylinder.difference(inner_cylinder)
        
        # Process the mesh for 3D printing
        hollow_cylinder.fill_holes()
        hollow_cylinder.process()
        
        # Validate the mesh is watertight
        if not hollow_cylinder.is_watertight:
            raise ValueError("Resulting mesh is not watertight")
            
        return hollow_cylinder
    except Exception as e:
        raise RuntimeError(f"Error creating hollow cylinder: {str(e)}")

# Create and export the hollow cylinder
hollow_cylinder = create_printable_hollow_cylinder()
hollow_cylinder.export('output_ascii.stl', file_type='stl_ascii')  # For human-readable
hollow_cylinder.export('output_binary.stl')  # For smaller file size