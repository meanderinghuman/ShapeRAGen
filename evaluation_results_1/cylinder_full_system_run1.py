import trimesh
import numpy as np

def create_printable_hollow_cylinder(outer_radius=15, wall_thickness=2, height=40, base_thickness=1):
    # Validate wall thickness (typical FDM minimum is 0.4-0.8mm)
    if wall_thickness < 0.8:
        raise ValueError("Wall thickness should be at least 0.8mm for FDM printing")
    
    inner_radius = outer_radius - wall_thickness
    
    # Create outer cylinder
    outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)
    
    # Create inner cylinder (hollow part)
    inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)
    
    # Create base plate
    base = trimesh.creation.cylinder(radius=outer_radius, height=base_thickness)
    base.apply_translation([0, 0, -base_thickness])
    
    try:
        # Subtract inner cylinder from outer cylinder
        hollow_cylinder = outer_cylinder.difference(inner_cylinder)
        
        # Combine with base plate
        final_mesh = hollow_cylinder.union(base)
        
        # Ensure the mesh is watertight and manifold
        if not final_mesh.is_watertight:
            final_mesh.fill_holes()
            final_mesh.process()
            
        if not final_mesh.is_watertight:
            raise ValueError("Failed to create watertight mesh")
            
        return final_mesh
    except Exception as e:
        print(f"Boolean operation failed: {str(e)}")
        # Fallback to simple concatenation if boolean ops fail
        print("Using fallback method (non-manifold result may need repair)")
        return trimesh.util.concatenate([outer_cylinder, inner_cylinder, base])

# Create and export the model
model = create_printable_hollow_cylinder()
model.export('hollow_cylinder_with_base.stl')