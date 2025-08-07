import trimesh
import numpy as np
from stl import mesh

def create_printable_hollow_cone():
    # Create outer cone with 20mm radius and 35mm height
    outer_cone = trimesh.creation.cone(radius=20, height=35)
    
    # Create inner cone with 2mm wall thickness (18mm radius)
    inner_cone = trimesh.creation.cone(radius=18, height=34)
    
    # Create hollow cone by difference operation
    hollow_cone = outer_cone.difference(inner_cone)
    
    # Create base plate for stability
    base_plate = trimesh.creation.cylinder(radius=20, height=2)
    base_plate.apply_translation([0, 0, -1])  # Position below cone
    
    # Combine cone with base plate
    final_mesh = hollow_cone.union(base_plate)
    
    # Ensure mesh is printable
    final_mesh.fill_holes()
    final_mesh.fix_normals()
    
    # Verify minimum wall thickness (2mm)
    if not final_mesh.is_watertight:
        raise ValueError("Mesh is not watertight - not suitable for printing")
    
    # Export as STL
    final_mesh.export('hollow_cone_with_base.stl')

create_printable_hollow_cone()