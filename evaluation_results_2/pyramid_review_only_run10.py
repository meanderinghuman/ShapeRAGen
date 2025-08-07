import trimesh
import numpy as np

def create_pyramid():
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

    inner_scale = 0.8
    min_wall_thickness = 2.0
    inner_vertices = outer_vertices * inner_scale
    inner_vertices[-1] = [12.5 * inner_scale, 12.5 * inner_scale, 30]

    inner_faces = np.array([
        [0, 4, 1],
        [1, 4, 2],
        [2, 4, 3],
        [3, 4, 0],
        [0, 2, 3],
        [0, 1, 2]
    ])

    vertices = np.vstack((outer_vertices, inner_vertices))
    faces = np.vstack((outer_faces, inner_faces + 5))

    pyramid_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    if not pyramid_mesh.is_watertight:
        pyramid_mesh.fill_holes()
    pyramid_mesh.fix_normals()
    
    if pyramid_mesh.volume < 0:
        pyramid_mesh.invert()
    
    min_thickness = trimesh.interfaces.gmsh.minimum_thickness(pyramid_mesh)
    if min_thickness < min_wall_thickness:
        raise ValueError(f"Wall thickness {min_thickness:.2f}mm is below minimum required {min_wall_thickness}mm")
    
    return pyramid_mesh

if __name__ == "__main__":
    try:
        model = create_pyramid()
        model.export('pyramid_model.stl', file_type='stl_ascii')
    except Exception as e:
        print(f"Error creating model: {str(e)}")