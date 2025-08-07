import trimesh
import numpy as np

def create_hollow_pyramid():
    # Outer pyramid dimensions (25x25mm base, 30mm height)
    outer_base = 25
    outer_height = 30
    
    # Inner pyramid dimensions (23x23mm base, 29mm height, 1mm offset)
    wall_thickness = 1
    inner_base = outer_base - 2 * wall_thickness
    inner_height = outer_height - wall_thickness
    
    # Create outer pyramid
    outer_vertices = np.array([
        [0, 0, 0],
        [outer_base, 0, 0],
        [outer_base, outer_base, 0],
        [0, outer_base, 0],
        [outer_base/2, outer_base/2, outer_height]
    ])
    
    outer_faces = np.array([
        [0, 1, 4],  # Front face
        [1, 2, 4],  # Right face
        [2, 3, 4],  # Back face
        [3, 0, 4]   # Left face
    ])
    
    # Create inner pyramid (inverted normals)
    inner_vertices = np.array([
        [wall_thickness, wall_thickness, 0],
        [outer_base-wall_thickness, wall_thickness, 0],
        [outer_base-wall_thickness, outer_base-wall_thickness, 0],
        [wall_thickness, outer_base-wall_thickness, 0],
        [outer_base/2, outer_base/2, inner_height]
    ])
    
    inner_faces = np.array([
        [0, 4, 1],  # Front face (reversed winding)
        [1, 4, 2],  # Right face
        [2, 4, 3],  # Back face
        [3, 4, 0]   # Left face
    ])
    
    # Create base faces
    base_faces_outer = np.array([[0, 3, 2], [0, 2, 1]])
    base_faces_inner = np.array([[0, 1, 2], [0, 2, 3]])
    
    # Combine all vertices and faces
    all_vertices = np.vstack((outer_vertices, inner_vertices))
    all_faces = np.vstack((
        outer_faces,
        inner_faces + 5,  # Offset by number of outer vertices
        base_faces_outer,
        base_faces_inner + 5
    ))
    
    # Create trimesh object
    pyramid_mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)
    
    # Validate mesh for 3D printing
    if not pyramid_mesh.is_watertight:
        pyramid_mesh.fill_holes()
    
    if not pyramid_mesh.is_watertight:
        raise ValueError("Mesh is not watertight and cannot be printed")
    
    # Check wall thickness
    if wall_thickness < 0.8:
        print("Warning: Wall thickness is below recommended minimum of 0.8mm")
    
    # Add a base plate for better adhesion
    base = trimesh.creation.box((outer_base, outer_base, wall_thickness))
    pyramid_mesh = pyramid_mesh + base
    
    return pyramid_mesh

# Create and export the model
pyramid = create_hollow_pyramid()
pyramid.export('pyramid.stl')