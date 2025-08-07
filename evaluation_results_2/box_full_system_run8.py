import trimesh
import numpy as np
from stl import mesh

def create_hollow_box(outer_length=30, outer_width=20, outer_height=40, wall_thickness=2):
    # Validate minimum wall thickness for FDM printing
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1mm for FDM printing")
    
    # Create inner box dimensions (hollow space)
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - wall_thickness  # open top

    # Validate inner dimensions
    if inner_length <= 0 or inner_width <= 0 or inner_height <= 0:
        raise ValueError("Wall thickness too large for given outer dimensions")

    # Create outer box
    outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))

    # Create inner box (offset by wall thickness)
    inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

    # Subtract inner box from outer box to create hollow box
    hollow_box = outer_box.difference(inner_box)

    # Ensure mesh is watertight (critical for 3D printing)
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
        hollow_box.fix_normals()

    return hollow_box

def export_stl(mesh_obj, filename='output.stl'):
    vertices = mesh_obj.vertices
    faces = mesh_obj.faces

    # Create the numpy-stl mesh object
    data = np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype)
    for i, f in enumerate(faces):
        for j in range(3):
            data['vectors'][i][j] = vertices[f[j], :]

    # Create the mesh and save to file
    hollow_mesh = mesh.Mesh(data)
    hollow_mesh.save(filename)

# Example usage
if __name__ == "__main__":
    try:
        hollow_box = create_hollow_box()
        export_stl(hollow_box)
        
        # Print some diagnostics
        print(f"Mesh is watertight: {hollow_box.is_watertight}")
        print(f"Mesh volume: {hollow_box.volume:.2f} mm³")
    except Exception as e:
        print(f"Error creating hollow box: {str(e)}")