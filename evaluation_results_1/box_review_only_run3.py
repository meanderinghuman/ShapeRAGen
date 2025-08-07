import trimesh
import numpy as np

def create_printable_hollow_box():
    # Outer dimensions
    outer_length = 30
    outer_width = 20
    outer_height = 40

    # Wall thickness (minimum 1.2mm for FDM printing)
    wall_thickness = max(2, 1.2)

    # Create outer box
    outer_box = trimesh.creation.box(
        extents=(outer_length, outer_width, outer_height),
        bounds=None,
        transform=None,
        sections=None,
        plane_origin=None,
        plane_normal=None
    )

    # Create inner box (hollow space)
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - wall_thickness  # Keep bottom solid

    inner_box = trimesh.creation.box(
        extents=(inner_length, inner_width, inner_height),
        bounds=None,
        transform=None,
        sections=None,
        plane_origin=None,
        plane_normal=None
    )

    # Position inner box centered within outer box
    inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

    try:
        # Create hollow box by subtracting inner from outer
        hollow_box = outer_box.difference(inner_box, engine='blender')
        
        # Repair and validate mesh
        hollow_box.process(validate=True)
        hollow_box.fill_holes()
        hollow_box.fix_normals()
        
        if not hollow_box.is_watertight:
            raise ValueError("Mesh is not watertight after processing")
            
        if not hollow_box.is_volume:
            raise ValueError("Mesh doesn't represent a solid volume")

        # Export as STL
        hollow_box.export('output.stl')
        return True
        
    except Exception as e:
        print(f"Error creating hollow box: {str(e)}")
        return False

create_printable_hollow_box()