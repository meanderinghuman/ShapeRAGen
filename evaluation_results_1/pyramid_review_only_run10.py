import trimesh
import numpy as np

def create_pyramid():
    # Define pyramid dimensions with 2mm wall thickness
    base_size = 25
    height = 30
    wall_thickness = 2
    
    # Create outer pyramid vertices
    outer_vertices = np.array([
        [0, 0, 0],                  # Base vertex 0
        [base_size, 0, 0],          # Base vertex 1
        [base_size, base_size, 0],  # Base vertex 2
        [0, base_size, 0],          # Base vertex 3
        [base_size/2, base_size/2, height]  # Apex vertex
    ])
    
    # Create inner pyramid vertices with wall thickness
    inner_vertices = np.array([
        [wall_thickness, wall_thickness, 0],
        [base_size-wall_thickness, wall_thickness, 0],
        [base_size-wall_thickness, base_size-wall_thickness, 0],
        [wall_thickness, base_size-wall_thickness, 0],
        [base_size/2, base_size/2, height-wall_thickness]
    ])
    
    # Combine all vertices
    vertices = np.vstack((outer_vertices, inner_vertices))
    
    # Define faces (triangles)
    faces = [
        # Outer pyramid faces
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        # Base face (outer)
        [0, 3, 1],
        [1, 3, 2],
        # Inner pyramid faces
        [5, 6, 9],
        [6, 7, 9],
        [7, 8, 9],
        [8, 5, 9],
        # Base face (inner)
        [5, 8, 6],
        [6, 8, 7],
        # Connecting walls
        [0, 5, 1],
        [1, 5, 6],
        [1, 6, 2],
        [2, 6, 7],
        [2, 7, 3],
        [3, 7, 8],
        [3, 8, 0],
        [0, 8, 5]
    ]
    
    # Create and validate mesh
    pyramid_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    # Ensure mesh is printable
    if not pyramid_mesh.is_watertight:
        pyramid_mesh.fill_holes()
    pyramid_mesh.fix_normals()
    
    # Check minimum feature size
    if pyramid_mesh.extents.min() < wall_thickness:
        raise ValueError("Mesh features smaller than minimum wall thickness")
    
    return pyramid_mesh

# Generate and export pyramid
pyramid = create_pyramid()
pyramid.export('pyramid_3dprintable.stl')