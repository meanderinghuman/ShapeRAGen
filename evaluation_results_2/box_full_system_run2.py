import trimesh
import numpy as np

def create_printable_hollow_box():
    # Define outer dimensions (mm)
    outer_length = 30
    outer_width = 20
    outer_height = 40

    # Set minimum printable wall thickness (mm)
    min_wall_thickness = 1.0
    wall_thickness = min_wall_thickness  # Using minimum printable thickness

    # Create outer box
    outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])

    # Create inner box dimensions (subtracting wall thickness from all sides)
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - 2 * wall_thickness

    # Validate dimensions
    if inner_length <= 0 or inner_width <= 0 or inner_height <= 0:
        raise ValueError("Wall thickness results in non-positive inner dimensions")

    inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])
    
    # Create hollow box
    hollow_box = outer_box.difference(inner_box)

    # Process and validate mesh
    hollow_box = hollow_box.process()
    if not hollow_box.is_watertight:
        raise ValueError("Resulting mesh is not watertight - not suitable for 3D printing")

    # Check volume to ensure proper hollowing
    if hollow_box.volume <= 0:
        raise ValueError("Resulting mesh has zero or negative volume")

    # Export as binary STL (smaller file size)
    hollow_box.export('output.stl', file_type='stl')

    return hollow_box

if __name__ == "__main__":
    try:
        model = create_printable_hollow_box()
        print(f"Successfully created printable model with volume: {model.volume:.2f} mm³")
    except Exception as e:
        print(f"Error creating model: {str(e)}")