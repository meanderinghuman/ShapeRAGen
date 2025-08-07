import trimesh
import numpy as np
from stl import mesh

def create_printable_hollow_sphere(output_file='output.stl', outer_radius=45, wall_thickness=1, subdivisions=4):
    try:
        # Validate parameters
        if wall_thickness < 1:
            raise ValueError("Wall thickness must be at least 1mm for FDM printing")
            
        if outer_radius <= wall_thickness:
            raise ValueError("Outer radius must be greater than wall thickness")

        # Create spheres
        outer_sphere = trimesh.creation.icosphere(radius=outer_radius, subdivisions=subdivisions)
        inner_sphere = trimesh.creation.icosphere(radius=outer_radius - wall_thickness, subdivisions=subdivisions)

        # Create hollow sphere
        hollow_sphere = outer_sphere.difference(inner_sphere)

        # Ensure mesh is printable
        hollow_sphere.fill_holes()
        hollow_sphere.process()
        
        if not hollow_sphere.is_watertight:
            raise ValueError("Mesh is not watertight and cannot be printed")

        # Convert to numpy-stl format efficiently
        vertices = hollow_sphere.vertices
        faces = hollow_sphere.faces
        
        # Create numpy-stl mesh
        numpy_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        numpy_mesh.vectors = vertices[faces]
        
        # Save binary STL (smaller file size)
        numpy_mesh.save(output_file)
        
        return hollow_sphere
        
    except Exception as e:
        print(f"Error creating printable model: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    create_printable_hollow_sphere()