import trimesh
import numpy as np
from stl import mesh

def create_hollow_box(outer_dim, wall_thickness):
    outer_box = trimesh.creation.box(extents=outer_dim)
    inner_dim = [d - 2 * wall_thickness for d in outer_dim]
    inner_box = trimesh.creation.box(extents=inner_dim)
    
    hollow_box = outer_box.difference(inner_box)
    
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
        hollow_box.fix_normals()
    
    if not hollow_box.is_watertight:
        raise ValueError("Failed to create watertight mesh")
    
    return hollow_box

def trimesh_to_stl(trimesh_obj):
    vertices = trimesh_obj.vertices
    faces = trimesh_obj.faces
    data = np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype)
    data['vectors'] = vertices[faces]
    return mesh.Mesh(data)

outer_dimensions = [20, 30, 40]
wall_thickness = 2.0

try:
    hollow_box = create_hollow_box(outer_dimensions, wall_thickness)
    stl_mesh = trimesh_to_stl(hollow_box)
    stl_mesh.save('hollow_box.stl')
    print("Successfully created hollow box STL")
except Exception as e:
    print(f"Error creating hollow box: {str(e)}")