import trimesh
import numpy as np

def create_printable_pyramid():
    # Define pyramid dimensions with validation
    base_size = 25.0
    height = 30.0
    wall_thickness = max(2.0, 1.0)  # Enforce minimum printable thickness
    
    # Create base plate for better bed adhesion
    base_plate_thickness = 1.0
    base_plate_vertices = np.array([
        [0, 0, -base_plate_thickness],
        [base_size, 0, -base_plate_thickness],
        [base_size, base_size, -base_plate_thickness],
        [0, base_size, -base_plate_thickness]
    ])
    
    # Create outer pyramid vertices
    outer_vertices = np.array([
        [0, 0, 0],
        [base_size, 0, 0],
        [base_size, base_size, 0],
        [0, base_size, 0],
        [base_size/2, base_size/2, height]
    ])
    
    # Create inner pyramid vertices (offset by wall thickness)
    inner_size = base_size - 2 * wall_thickness
    inner_vertices = np.array([
        [wall_thickness, wall_thickness, 0],
        [base_size - wall_thickness, wall_thickness, 0],
        [base_size - wall_thickness, base_size - wall_thickness, 0],
        [wall_thickness, base_size - wall_thickness, 0],
        [base_size/2, base_size/2, height - wall_thickness]
    ])
    
    # Combine all vertices
    vertices = np.vstack((base_plate_vertices, outer_vertices, inner_vertices))
    
    # Define faces (triangles)
    faces = np.array([
        # Base plate faces
        [0, 3, 1],
        [1, 3, 2],
        
        # Outer pyramid faces
        [4, 5, 8],
        [5, 6, 8],
        [6, 7, 8],
        [7, 4, 8],
        
        # Inner pyramid faces (inverted normals)
        [9, 13, 10],
        [10, 13, 11],
        [11, 13, 12],
        [12, 13, 9],
        
        # Bottom faces (connecting base plate to outer pyramid)
        [0, 4, 1],
        [1, 4, 5],
        [1, 5, 2],
        [2, 5, 6],
        [2, 6, 3],
        [3, 6, 7],
        [3, 7, 0],
        [0, 7, 4],
        
        # Outer base triangles
        [4, 7, 5],
        [5, 7, 6],
        
        # Inner base triangles
        [9, 10, 12],
        [10, 11, 12],
        
        # Side walls (connecting outer and inner pyramids)
        [4, 9, 5],
        [5, 9, 10],
        [5, 10, 6],
        [6, 10, 11],
        [6, 11, 7],
        [7, 11, 12],
        [7, 12, 4],
        [4, 12, 9]
    ])
    
    # Create the mesh
    pyramid_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    # Validate mesh for 3D printing
    if not pyramid_mesh.is_watertight:
        pyramid_mesh.fill_holes()
    pyramid_mesh.fix_normals()
    
    # Check for overhangs that might need supports
    overhang = np.degrees(np.arccos(pyramid_mesh.face_normals[:, 2]))
    if np.any(overhang > 45):
        print("Note: Model contains overhangs that may require supports")
    
    return pyramid_mesh

# Create and export the pyramid
pyramid = create_printable_pyramid()
pyramid.export('pyramid_with_base.stl')