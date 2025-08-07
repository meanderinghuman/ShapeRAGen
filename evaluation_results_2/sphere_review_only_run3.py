import trimesh
import numpy as np

def create_printable_hollow_sphere():
    try:
        # Create outer and inner spheres with sufficient resolution
        sphere = trimesh.creation.icosphere(subdivisions=4, radius=45)
        inner_sphere = trimesh.creation.icosphere(subdivisions=4, radius=43)
        
        # Boolean difference operation with safety checks
        if sphere.is_watertight and inner_sphere.is_watertight:
            hollow_sphere = sphere.difference(inner_sphere)
        else:
            raise ValueError("Input meshes are not watertight")
        
        # Validate and repair mesh
        hollow_sphere.process()
        if not hollow_sphere.is_watertight:
            hollow_sphere.fill_holes()
        
        # Additional checks for printing viability
        if hollow_sphere.is_empty:
            raise ValueError("Resulting mesh is empty")
        if hollow_sphere.volume < 100:
            raise ValueError("Mesh volume too small for reliable printing")
        
        # Export with options for better 3D printing
        hollow_sphere.export(
            'hollow_sphere.stl',
            file_type='stl',
            resolution=500  # Higher resolution for smooth curves
        )
        
        return hollow_sphere
    
    except Exception as e:
        print(f"Error creating printable mesh: {str(e)}")
        return None

# Execute the function
printable_sphere = create_printable_hollow_sphere()