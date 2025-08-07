import trimesh
import numpy as np

def create_hollow_pyramid():
    # Define pyramid dimensions
    base_size = 25
    height = 30
    wall_thickness = 2
    
    # Create outer pyramid vertices
    outer_vertices = np.array([
        [0, 0, 0], [base_size, 0, 0], [base_size, base_size, 0], [0, base_size, 0],
        [base_size/2, base_size/2, height]
    ])
    
    # Create inner pyramid vertices (offset by wall thickness)
    inner_vertices = np.array([
        [wall_thickness, wall_thickness, 0],
        [base_size-wall_thickness, wall_thickness, 0],
        [base_size-wall_thickness, base_size-wall_thickness, 0],
        [wall_thickness, base_size-wall_thickness, 0],
        [base_size/2, base_size/2, height-wall_thickness]
    ])
    
    # Faces for both pyramids (same topology)
    faces = np.array([
        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  # sides
        [0, 3, 2], [0, 2, 1]  # base
    ])
    
    # Create both meshes
    outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=faces)
    inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=faces)
    
    # Combine and ensure watertight
    hollow = outer_mesh.difference(inner_mesh)
    
    # Verify wall thickness
    if not hollow.is_watertight:
        raise ValueError("Resulting mesh is not watertight")
    
    return hollow

# Create and export
try:
    pyramid = create_hollow_pyramid()
    pyramid.export('hollow_pyramid.stl')
except Exception as e:
    print(f"Error creating pyramid: {str(e)}")