import trimesh
import numpy as np

def create_pyramid_mesh():
    # Create outer pyramid with proper wall thickness
    outer_vertices = np.array([
        [0, 0, 0],
        [25, 0, 0],
        [25, 25, 0],
        [0, 25, 0],
        [12.5, 12.5, 30]
    ])
    
    outer_faces = np.array([
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [0, 3, 2],
        [0, 2, 1]
    ])
    
    # Create inner pyramid with minimum wall thickness of 2.5mm
    inner_scale = 0.8
    wall_thickness = 2.5
    inner_vertices = outer_vertices.copy()
    inner_vertices[:-1] = inner_vertices[:-1] * inner_scale
    inner_vertices[:-1] += np.array([wall_thickness, wall_thickness, 0])
    inner_vertices[-1][2] = 28
    
    inner_faces = np.array([
        [5, 6, 9],
        [6, 7, 9],
        [7, 8, 9],
        [8, 5, 9],
        [5, 8, 7],
        [5, 7, 6]
    ])
    
    all_vertices = np.vstack((outer_vertices, inner_vertices))
    all_faces = np.vstack((outer_faces, inner_faces))
    
    mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)
    
    if not mesh.is_watertight:
        mesh.fill_holes()
    if not mesh.is_winding_consistent:
        mesh.fix_normals()
    
    # Validate minimum feature size
    if mesh.extents.min() < 1.0:
        raise ValueError("Model contains features smaller than 1mm which may not print well")
    
    return mesh

def add_support_structure(base_mesh):
    support_height = 5
    support_vertices = np.array([
        [0, 0, -support_height],
        [25, 0, -support_height],
        [25, 25, -support_height],
        [0, 25, -support_height],
        [0, 0, 0],
        [25, 0, 0],
        [25, 25, 0],
        [0, 25, 0]
    ])
    
    support_faces = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [0, 4, 1],
        [1, 4, 5],
        [1, 5, 2],
        [2, 5, 6],
        [2, 6, 3],
        [3, 6, 7],
        [3, 7, 0],
        [0, 7, 4],
        [4, 5, 6],
        [4, 6, 7]
    ])
    
    support_mesh = trimesh.Trimesh(vertices=support_vertices, faces=support_faces)
    combined_mesh = base_mesh + support_mesh
    
    return combined_mesh

pyramid_mesh = create_pyramid_mesh()
supported_mesh = add_support_structure(pyramid_mesh)
supported_mesh.export('pyramid_with_support.stl')