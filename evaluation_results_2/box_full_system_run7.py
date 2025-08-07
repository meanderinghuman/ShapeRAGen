import trimesh
import numpy as np
from stl import mesh

def create_hollow_box(outer_length, outer_width, outer_height, wall_thickness):
    # Validate minimum wall thickness for FDM printing
    if wall_thickness < 1.0:
        raise ValueError("Wall thickness must be at least 1.0mm for FDM printing")
    
    # Create outer box
    outer_box = trimesh.creation.box(extents=[outer_length, outer_width, outer_height])
    
    # Create inner box dimensions
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - 2 * wall_thickness
    
    # Validate inner dimensions
    if any(dim <= 0 for dim in [inner_length, inner_width, inner_height]):
        raise ValueError("Wall thickness results in negative or zero inner dimensions")
    
    # Create inner box (hollow space)
    inner_box = trimesh.creation.box(extents=[inner_length, inner_width, inner_height])
    
    # Position the inner box at the center
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])
    
    # Create hollow box by subtracting inner from outer
    hollow_box = outer_box.difference(inner_box)
    
    # Validate and repair mesh
    if not hollow_box.is_watertight:
        hollow_box.fill_holes()
    hollow_box.fix_normals()
    
    if not hollow_box.is_watertight:
        raise ValueError("Failed to create watertight mesh")
    
    return hollow_box

def export_stl(hollow_box, filename='output.stl'):
    # Export as STL using trimesh
    hollow_box.export(filename)
    
    # Alternative export using numpy-stl (for compatibility)
    vertices = hollow_box.vertices
    faces = hollow_box.faces
    
    box_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            box_mesh.vectors[i][j] = vertices[f[j], :]
    
    box_mesh.save(filename.replace('.stl', '_numpy.stl'))

# Parameters
outer_length = 30  # x dimension
outer_width = 20   # y dimension
outer_height = 40   # z dimension
wall_thickness = 1  # wall thickness for FDM printing

# Create and export hollow box
try:
    hollow_box = create_hollow_box(outer_length, outer_width, outer_height, wall_thickness)
    export_stl(hollow_box)
except ValueError as e:
    print(f"Error creating model: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")