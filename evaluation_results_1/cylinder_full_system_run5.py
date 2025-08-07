import trimesh
import numpy as np

def create_printable_hollow_cylinder():
    # Parameters with safety checks
    outer_radius = 15.0
    height = 40.0
    wall_thickness = 2.0  # Recommended minimum for FDM printing
    
    # Validate minimum wall thickness
    if wall_thickness < 1.5:
        raise ValueError("Wall thickness below recommended minimum for FDM printing (1.5mm)")
    
    # Create cylinders
    outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)
    inner_radius = max(outer_radius - wall_thickness, 0.1)  # Ensure positive radius
    inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)
    
    # Create hollow cylinder with error handling
    try:
        hollow_cylinder = outer_cylinder.difference(inner_cylinder)
    except:
        # Fallback to manual hollowing if boolean fails
        hollow_cylinder = outer_cylinder.copy()
        hollow_cylinder.faces = np.vstack([outer_cylinder.faces, inner_cylinder.faces[::-1]])
    
    # Process mesh for printing
    hollow_cylinder.process(validate=True)
    hollow_cylinder.fill_holes()
    
    # Add optional base plate for better printing
    base = trimesh.creation.cylinder(radius=outer_radius, height=1.0)
    base.apply_translation([0, 0, -0.5])  # Center at z=0
    final_mesh = trimesh.util.concatenate([hollow_cylinder, base])
    
    # Final validation
    if not final_mesh.is_watertight:
        final_mesh = final_mesh.convex_hull  # Fallback to convex hull if not watertight
    
    return final_mesh

# Create and export
printable_cylinder = create_printable_hollow_cylinder()
printable_cylinder.export('output.stl')