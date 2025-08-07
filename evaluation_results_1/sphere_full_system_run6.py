import trimesh
import numpy as np

def create_hollow_sphere(outer_radius=45.0, wall_thickness=2.0, output_file='output.stl'):
    try:
        # Validate parameters
        if wall_thickness < 1.0:
            raise ValueError("Wall thickness must be at least 1mm for FDM printing")
            
        # Create spheres
        outer_sphere = trimesh.creation.icosphere(radius=outer_radius)
        inner_sphere = trimesh.creation.icosphere(radius=outer_radius - wall_thickness)
        
        # Create hollow sphere
        hollow_sphere = outer_sphere.difference(inner_sphere)
        
        # Process mesh
        hollow_sphere.process()
        
        # Ensure watertight
        if not hollow_sphere.is_watertight:
            hollow_sphere.fill_holes()
            hollow_sphere.process()
            
        # Verify watertightness
        if not hollow_sphere.is_watertight:
            raise ValueError("Failed to create watertight mesh")
            
        # Verify wall thickness meets requirements
        if hollow_sphere.bounding_box.extents.min() < wall_thickness:
            raise ValueError("Minimum wall thickness requirement not met")
            
        # Export
        hollow_sphere.export(output_file)
        return hollow_sphere
        
    except Exception as e:
        print(f"Error creating hollow sphere: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    create_hollow_sphere(outer_radius=45.0, wall_thickness=2.0)