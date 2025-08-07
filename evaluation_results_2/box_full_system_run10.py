import numpy as np
import trimesh
from stl import mesh

def create_printable_hollow_box(length=30, width=20, height=40, wall_thickness=2, output_file='output.stl'):
    # Validate minimum wall thickness for FDM printing
    if wall_thickness < 1.2:
        raise ValueError("Wall thickness must be at least 1.2mm for FDM printing")
    
    # Validate dimensions
    if any(d <= 0 for d in [length, width, height]):
        raise ValueError("All dimensions must be positive values")
    
    # Create outer box
    outer_box = trimesh.creation.box(extents=[length, width, height])
    
    # Create inner box (hollow space)
    inner_length = max(0.1, length - 2 * wall_thickness)
    inner_width = max(0.1, width - 2 * wall_thickness)
    inner_height = max(0.1, height - 2 * wall_thickness)
    inner_box = trimesh.creation.box(extents=[inner_length, inner_width, inner_height])
    
    # Position inner box at the center of outer box
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])
    
    try:
        # Subtract inner box from outer box to create hollow box
        hollow_box = outer_box.difference(inner_box, engine='blender')
    except:
        # Fallback to simple boolean if Blender isn't available
        hollow_box = outer_box.difference(inner_box)
    
    # Ensure the mesh is printable
    hollow_box = hollow_box.process(validate=True)
    hollow_box.fill_holes()
    hollow_box.fix_normals()
    
    # Verify mesh is watertight
    if not hollow_box.is_watertight:
        raise ValueError("Generated mesh is not watertight and cannot be printed")
    
    # Convert trimesh object to numpy-stl mesh more efficiently
    box_mesh = mesh.Mesh(np.zeros(hollow_box.faces.shape[0], dtype=mesh.Mesh.dtype))
    box_mesh.vectors = hollow_box.vertices[hollow_box.faces]
    
    # Save the mesh
    box_mesh.save(output_file)
    return hollow_box

# Example usage
if __name__ == "__main__":
    try:
        mesh = create_printable_hollow_box(
            length=30,
            width=20,
            height=40,
            wall_thickness=2,
            output_file='output.stl'
        )
        print("Successfully created printable hollow box")
    except Exception as e:
        print(f"Error creating model: {str(e)}")