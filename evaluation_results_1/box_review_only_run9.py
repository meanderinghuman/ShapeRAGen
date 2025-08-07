import trimesh
import numpy as np

def create_printable_hollow_box():
    # Design parameters with validation
    outer_length = 30.0
    outer_width = 20.0
    outer_height = 40.0
    wall_thickness = 2.0
    min_wall_thickness = 0.4  # Typical nozzle diameter
    
    # Validate dimensions
    if wall_thickness < min_wall_thickness:
        raise ValueError(f"Wall thickness must be at least {min_wall_thickness}mm")
    if any(dim <= 0 for dim in [outer_length, outer_width, outer_height]):
        raise ValueError("All dimensions must be positive")

    # Create outer box
    outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])

    # Calculate inner dimensions (ensuring minimum wall thickness)
    inner_length = max(outer_length - 2 * wall_thickness, 0)
    inner_width = max(outer_width - 2 * wall_thickness, 0)
    inner_height = max(outer_height - wall_thickness, 0)

    # Create and position inner box
    inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])
    inner_box.apply_translation([0, 0, wall_thickness/2])

    try:
        # Create hollow box and ensure it's watertight
        hollow_box = outer_box.difference(inner_box)
        hollow_box.fill_holes()
        hollow_box.process()
        
        # Validate mesh before export
        if not hollow_box.is_watertight:
            raise ValueError("Resulting mesh is not watertight")
            
        hollow_box.export('output.stl')
        return True
    except Exception as e:
        print(f"Error creating mesh: {str(e)}")
        return False

create_printable_hollow_box()