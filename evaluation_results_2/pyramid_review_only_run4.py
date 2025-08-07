import trimesh
import numpy as np

def create_hollow_pyramid(base_size=25.0, height=30.0, wall_thickness=1.2, base_thickness=1.0):
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness should be at least 1.0mm for FDM printing")
    if base_size <= 2 * wall_thickness:
        raise ValueError("Base size too small for specified wall thickness")
    
    inner_size = base_size - 2 * wall_thickness
    inner_height = height - wall_thickness
    
    outer_vertices = np.array([
        [0, 0, 0],
        [base_size, 0, 0],
        [base_size, base_size, 0],
        [0, base_size, 0],
        [0, 0, base_thickness],
        [base_size, 0, base_thickness],
        [base_size, base_size, base_thickness],
        [0, base_size, base_thickness],
        [base_size/2, base_size/2, height]
    ])
    
    inner_vertices = np.array([
        [wall_thickness, wall_thickness, base_thickness],
        [base_size-wall_thickness, wall_thickness, base_thickness],
        [base_size-wall_thickness, base_size-wall_thickness, base_thickness],
        [wall_thickness, base_size-wall_thickness, base_thickness],
        [base_size/2, base_size/2, inner_height]
    ])
    
    outer_faces = np.array([
        [0, 1, 4], [1, 5, 4],  # Front wall
        [1, 2, 5], [2, 6, 5],  # Right wall
        [2, 3, 6], [3, 7, 6],  # Back wall
        [3, 0, 7], [0, 4, 7],  # Left wall
        [4, 5, 8], [5, 6, 8],  # Upper front/right
        [6, 7, 8], [7, 4, 8],  # Upper back/left
        [3, 2, 0], [0, 2, 1]   # Bottom
    ])
    
    inner_faces = np.array([
        [0, 4, 1], [1, 4, 2],  # Inner walls
        [2, 4, 3], [3, 4, 0],
        [0, 1, 3], [1, 2, 3]    # Inner bottom
    ])
    
    all_vertices = np.vstack((outer_vertices, inner_vertices))
    all_faces = np.vstack((
        outer_faces,
        inner_faces + len(outer_vertices)
    ))
    
    pyramid_mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)
    
    if not pyramid_mesh.is_watertight:
        pyramid_mesh.fill_holes()
    pyramid_mesh.fix_normals()
    
    if not pyramid_mesh.is_watertight or pyramid_mesh.is_empty:
        raise ValueError("Failed to create valid printable mesh")
    
    return pyramid_mesh

pyramid = create_hollow_pyramid()
pyramid.export('hollow_pyramid.stl')