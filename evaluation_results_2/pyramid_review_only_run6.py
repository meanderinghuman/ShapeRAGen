import trimesh
import numpy as np

def create_hollow_pyramid():
    base_size = 25.0
    height = 30.0
    wall_thickness = 1.0
    min_wall_thickness = 1.0
    
    if wall_thickness < min_wall_thickness:
        wall_thickness = min_wall_thickness

    outer_vertices = np.array([
        [0, 0, 0],
        [base_size, 0, 0],
        [base_size, base_size, 0],
        [0, base_size, 0],
        [base_size/2, base_size/2, height]
    ])

    inner_size = base_size - 2 * wall_thickness
    inner_height = height - wall_thickness
    inner_vertices = np.array([
        [wall_thickness, wall_thickness, 0],
        [inner_size + wall_thickness, wall_thickness, 0],
        [inner_size + wall_thickness, inner_size + wall_thickness, 0],
        [wall_thickness, inner_size + wall_thickness, 0],
        [base_size/2, base_size/2, inner_height]
    ])

    vertices = np.vstack((outer_vertices, inner_vertices))

    faces = [
        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],
        [5, 6, 9], [6, 7, 9], [7, 8, 9], [8, 5, 9],
        [0, 1, 5], [1, 5, 6], [1, 2, 6], [2, 6, 7],
        [2, 3, 7], [3, 7, 8], [3, 0, 8], [0, 8, 5]
    ]

    pyramid_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    pyramid_mesh.fix_normals()
    pyramid_mesh.fill_holes()

    if not pyramid_mesh.is_watertight:
        pyramid_mesh = pyramid_mesh.convex_hull

    base_plate = trimesh.creation.box((base_size, base_size, wall_thickness))
    base_plate.apply_translation((base_size/2, base_size/2, -wall_thickness/2))
    
    combined = trimesh.util.concatenate([pyramid_mesh, base_plate])
    
    if combined.is_watertight:
        combined.export('hollow_pyramid_with_base.stl')
    else:
        pyramid_mesh.export('hollow_pyramid.stl')

create_hollow_pyramid()