import trimesh
import numpy as np

def create_hollow_pyramid():
    # Dimensions in millimeters
    base_size = 25
    height = 30
    wall_thickness = 2
    
    # Create outer pyramid
    outer_vertices = np.array([
        [0, 0, 0],
        [base_size, 0, 0],
        [base_size, base_size, 0],
        [0, base_size, 0],
        [base_size/2, base_size/2, height]
    ])

    outer_faces = np.array([
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [0, 3, 2],
        [0, 2, 1]
    ])

    # Create inner pyramid with wall thickness offset
    inner_vertices = np.array([
        [wall_thickness, wall_thickness, 0],
        [base_size-wall_thickness, wall_thickness, 0],
        [base_size-wall_thickness, base_size-wall_thickness, 0],
        [wall_thickness, base_size-wall_thickness, 0],
        [base_size/2, base_size/2, height-wall_thickness]
    ])

    inner_faces = np.array([
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [0, 3, 2],
        [0, 2, 1]
    ])

    # Create meshes
    outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
    inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

    # Combine meshes to create hollow pyramid
    hollow_pyramid = trimesh.util.concatenate([outer_mesh, inner_mesh.invert()])

    # Process mesh for 3D printing
    hollow_pyramid.fill_holes()
    hollow_pyramid.process()
    
    # Validate mesh
    if not hollow_pyramid.is_watertight:
        raise ValueError("Mesh is not watertight")
    if not hollow_pyramid.is_winding_consistent:
        raise ValueError("Mesh has inconsistent winding")
    
    # Check minimum feature size
    if hollow_pyramid.extents.min() < wall_thickness:
        raise ValueError("Features smaller than minimum wall thickness")
    
    return hollow_pyramid

# Create and export the pyramid
pyramid = create_hollow_pyramid()
pyramid.export('hollow_pyramid.stl')