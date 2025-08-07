import trimesh
import numpy as np
from stl import mesh

# Create outer cylinder with sufficient segments for smoothness
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40, segments=64)

# Create inner cylinder with slight offset for clean boolean
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40.2, segments=64)

# Perform boolean difference with error handling
try:
    hollow_cylinder = outer_cylinder.difference(inner_cylinder)
    if not hollow_cylinder.is_watertight:
        raise ValueError("Resulting mesh is not watertight")
        
    # Verify minimum wall thickness (1mm in this case)
    if not (15 - 14) >= 1.0:
        raise ValueError("Wall thickness below minimum required (1mm)")
        
    # Process and repair mesh
    hollow_cylinder.fill_holes()
    hollow_cylinder.process()
    
    # Export as STL
    hollow_cylinder.export('output.stl')
    
except Exception as e:
    print(f"Error creating printable mesh: {str(e)}")