import trimesh
import numpy as np

def create_hollow_pyramid(base_size=25.0, height=30.0, wall_thickness=2.0):
    # Validate minimum wall thickness for FDM printing
    if wall_thickness < 1.5:
        raise ValueError("Wall thickness should be at least 1.5mm for FDM printing")
    
    # Create outer pyramid vertices
    outer_vertices = np.array([
        [base_size/2, base_size/2, 0],
        [-base_size/2, base_size/2, 0],
        [-base_size/2, -base_size/2, 0],
        [base_size/2, -base_size/2, 0],
        [0, 0, height]
    ])
    
    # Create inner pyramid vertices with proper wall thickness
    inner_size = base_size - 2 * wall_thickness
    inner_height = height - wall_thickness
    inner_vertices = np.array([
        [inner_size/2, inner_size/2, 0],
        [-inner_size/2, inner_size/2, 0],
        [-inner_size/2, -inner_size/2, 0],
        [inner_size/2, -inner_size/2, 0],
        [0, 0, inner_height]
    ])
    
    # Combine vertices
    vertices = np.vstack((outer_vertices, inner_vertices))
    
    # Define faces with consistent winding
    faces = [
        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],
        [5, 6, 9], [6, 7, 9], [7, 8, 9], [8, 5, 9],
        [0, 1, 5], [1, 5, 6], [1, 2, 6], [2, 6, 7],
        [2, 3, 7], [3, 7, 8], [3, 0, 8], [0, 8, 5]
    ]
    
    # Create and validate mesh
    pyramid_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    if not pyramid_mesh.is_watertight:
        pyramid_mesh.fill_holes()
    pyramid_mesh.fix_normals()
    
    # Check minimum feature size
    if pyramid_mesh.edges_unique_length.min() < 1.5:
        print("Warning: Some features may be too small for reliable printing")
    
    return pyramid_mesh

# Generate and export the pyramid
pyramid = create_hollow_pyramid()
pyramid.export('pyramid.stl')