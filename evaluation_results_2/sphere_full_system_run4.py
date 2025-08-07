import trimesh
import numpy as np

def create_printable_hollow_sphere():
    # Create outer sphere with 45mm radius
    outer_sphere = trimesh.creation.icosphere(radius=45)
    
    # Create inner sphere with slightly smaller radius (44mm) to make it hollow
    inner_sphere = trimesh.creation.icosphere(radius=44)
    
    # Create the hollow sphere by subtracting inner from outer
    hollow_sphere = outer_sphere.difference(inner_sphere)
    
    # Validate wall thickness (should be 1mm)
    thickness = hollow_sphere.bounding_box.extents.min()
    if thickness < 1.0:
        raise ValueError(f"Wall thickness {thickness:.2f}mm is below minimum printable thickness of 1mm")
    
    # Ensure the mesh is watertight and manifold (important for 3D printing)
    if not hollow_sphere.is_watertight:
        hollow_sphere.fill_holes()
    
    # Process the mesh to remove degenerate faces and fix normals
    hollow_sphere.process(validate=True)
    
    # Check if the mesh is printable (has volume)
    if hollow_sphere.volume < 0.1:
        raise ValueError("Mesh has no significant volume and is unprintable")
    
    # Add a small base plate for better printability
    base = trimesh.creation.box(extents=[100, 100, 1])
    base.apply_translation([0, 0, -45 - 0.5])  # Position below the sphere
    
    # Combine sphere with base
    printable_model = hollow_sphere.union(base)
    
    # Export as binary STL file (smaller file size)
    printable_model.export('printable_hollow_sphere.stl')

if __name__ == '__main__':
    create_printable_hollow_sphere()