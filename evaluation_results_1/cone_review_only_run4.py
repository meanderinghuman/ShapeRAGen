import trimesh
import numpy as np
from trimesh.boolean import difference

def create_printable_hollow_cone():
    # Create outer cone with sufficient wall thickness
    outer_cone = trimesh.creation.cone(radius=20, height=35)
    
    # Create inner cone with 2mm wall thickness
    inner_cone = trimesh.creation.cone(radius=18, height=34)
    
    # Position inner cone with 0.5mm offset for top thickness
    inner_cone.apply_translation([0, 0, 0.5])
    
    # Perform boolean difference with error handling
    try:
        hollow_cone = difference([outer_cone, inner_cone], engine='blender')
    except:
        hollow_cone = outer_cone.difference(inner_cone)
    
    # Create a base plate for better printing
    base = trimesh.creation.cylinder(radius=20, height=1)
    base.apply_translation([0, 0, -0.5])
    
    # Combine with base plate
    final_model = hollow_cone + base
    
    # Verify mesh is watertight and printable
    if not final_model.is_watertight:
        final_model.fill_holes()
        final_model.fix_normals()
    
    # Export with proper units
    final_model.export('hollow_cone_with_base.stl')
    
    return final_model

create_printable_hollow_cone()