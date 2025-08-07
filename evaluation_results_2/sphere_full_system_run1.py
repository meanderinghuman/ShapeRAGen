import trimesh
import numpy as np
from stl import mesh

def create_hollow_sphere(outer_radius=45, wall_thickness=1):
    # Create spheres
    outer_sphere = trimesh.creation.icosphere(radius=outer_radius)
    inner_sphere = trimesh.creation.icosphere(radius=outer_radius - wall_thickness)
    
    # Create hollow sphere
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    # Process mesh
    hollow_sphere.process()
    
    # Validate mesh
    if not hollow_sphere.is_watertight:
        raise ValueError("Mesh is not watertight - cannot be 3D printed")
    
    # Check wall thickness (approximate)
    if wall_thickness < 1:
        print("Warning: Wall thickness is below recommended minimum of 1mm for FDM printing")
    
    # Convert to numpy-stl mesh
    hollow_mesh = mesh.Mesh(np.zeros(hollow_sphere.faces.shape[0], dtype=mesh.Mesh.dtype))
    hollow_mesh.vectors = hollow_sphere.vertices[hollow_sphere.faces]
    
    return hollow_mesh

# Create and save hollow sphere
try:
    hollow_mesh = create_hollow_sphere(outer_radius=45, wall_thickness=1)
    hollow_mesh.save('output.stl')
    print("STL file saved successfully")
except Exception as e:
    print(f"Error creating mesh: {str(e)}")