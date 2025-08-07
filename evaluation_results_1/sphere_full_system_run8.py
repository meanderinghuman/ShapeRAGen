import trimesh
import numpy as np

def create_hollow_sphere(outer_radius=45, wall_thickness=1, output_file='output.stl'):
    try:
        # Create spheres
        outer_sphere = trimesh.creation.icosphere(radius=outer_radius)
        inner_sphere = trimesh.creation.icosphere(radius=outer_radius - wall_thickness)
        
        # Create hollow sphere
        hollow_sphere = outer_sphere.difference(inner_sphere)
        
        # Process and validate mesh
        hollow_sphere.process()
        
        if not hollow_sphere.is_watertight:
            hollow_sphere.fill_holes()
            hollow_sphere.process()
            
        if not hollow_sphere.is_watertight:
            raise ValueError("Mesh is not watertight after repair attempts")
            
        if hollow_sphere.volume < 0.1:
            raise ValueError("Mesh volume is too small, check wall thickness")
            
        # Export the mesh
        hollow_sphere.export(output_file)
        print(f"Successfully exported to {output_file}")
        return hollow_sphere
        
    except Exception as e:
        print(f"Error creating hollow sphere: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    create_hollow_sphere()