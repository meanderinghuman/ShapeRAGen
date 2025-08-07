import trimesh
import numpy as np
from stl import mesh

def create_printable_cone():
    # Create outer cone with base
    outer_cone = trimesh.creation.cone(radius=20, height=35)
    
    # Create inner cone with slightly smaller dimensions
    inner_cone = trimesh.creation.cone(radius=18, height=34)
    
    # Create base for stability
    base = trimesh.creation.cylinder(radius=20, height=1)
    base.apply_translation([0, 0, -0.5])  # Center the base
    
    try:
        # Combine outer cone with base
        solid_cone = outer_cone.union(base)
        
        # Subtract inner cone to create hollow structure
        hollow_cone = solid_cone.difference(inner_cone)
        
        # Process and validate mesh
        hollow_cone = hollow_cone.process()
        if not hollow_cone.is_watertight:
            raise ValueError("Mesh is not watertight")
        if hollow_cone.volume < 0.1:
            raise ValueError("Mesh volume too small")
        
        # Export the model
        hollow_cone.export('output.stl')
        return True
    except Exception as e:
        print(f"Error creating model: {str(e)}")
        return False

create_printable_cone()