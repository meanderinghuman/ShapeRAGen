import trimesh
import numpy as np

def create_printable_cone():
    # Parameters with explicit minimum wall thickness (2mm)
    outer_radius = 20
    inner_radius = 18
    height = 35
    base_thickness = 2
    
    # Create outer cone
    outer_cone = trimesh.creation.cone(radius=outer_radius, height=height)
    
    # Create inner cone (hollow part) with smaller dimensions
    inner_cone = trimesh.creation.cone(radius=inner_radius, height=height-base_thickness)
    
    # Create base cylinder
    base = trimesh.creation.cylinder(radius=outer_radius, height=base_thickness)
    base.apply_translation([0, 0, -base_thickness])
    
    # Combine base with outer cone
    solid_cone = trimesh.boolean.union([outer_cone, base])
    
    # Subtract inner cone to create hollow cone with base
    hollow_cone = solid_cone.difference(inner_cone)
    
    # Validate mesh for 3D printing
    if not hollow_cone.is_watertight:
        hollow_cone.fill_holes()
    hollow_cone.fix_normals()
    
    if not hollow_cone.is_watertight or not hollow_cone.is_volume:
        raise ValueError("Mesh is not printable - not watertight or no volume")
    
    # Check minimum wall thickness (2mm in this case)
    if (outer_radius - inner_radius) < 2:
        raise ValueError("Wall thickness below minimum (2mm)")
    
    return hollow_cone

# Create and export the model
model = create_printable_cone()
model.export('output.stl')