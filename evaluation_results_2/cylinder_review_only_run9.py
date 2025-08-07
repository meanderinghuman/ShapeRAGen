import trimesh
import numpy as np

def create_printable_hollow_cylinder():
    # Parameters with printability considerations
    outer_radius = 15.0
    inner_radius = 12.0  # 3mm wall thickness (good for FDM)
    height = 40.0
    base_thickness = 2.0  # Add base for better bed adhesion
    segment_count = 64  # Smooth cylinder
    
    # Create components
    outer_cylinder = trimesh.creation.cylinder(
        radius=outer_radius,
        height=height,
        sections=segment_count)
    
    inner_cylinder = trimesh.creation.cylinder(
        radius=inner_radius,
        height=height,
        sections=segment_count)
    
    # Create base plate
    base = trimesh.creation.cylinder(
        radius=outer_radius,
        height=base_thickness)
    
    # Perform boolean operations with error handling
    try:
        hollow = outer_cylinder.difference(inner_cylinder)
        final = hollow.union(base)
        
        # Ensure mesh is printable
        if not final.is_watertight:
            final.fill_holes()
            final.fix_normals()
        
        # Validate wall thickness
        if (outer_radius - inner_radius) < 1.0:
            raise ValueError("Wall thickness below minimum recommended 1mm")
            
        return final
    except Exception as e:
        print(f"Boolean operation failed: {str(e)}")
        raise

# Create and export model
model = create_printable_hollow_cylinder()
model.export('output.stl')