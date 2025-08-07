# check_context_files.py

import os


def check_required_files():
    """Check if all required context files are present"""

    required_files = {
        'Trimesh Documentation': ['tri_docs_embeddings.npy', 'tri_docs_chunks.pkl'],
        'NumPy-STL Documentation': ['numpy_stl_embeddings.npy', 'numpy_stl_chunks.pkl'],
        'Custom Trimesh Functions': ['tri_custom_embeddings.npy', 'tri_custom_chunks.pkl'],
        'Best Practices': ['best_embeddings.npy', 'best_chunks.pkl']
    }

    print("Checking required context files...\n")

    all_present = True
    missing_files = []

    for context_name, files in required_files.items():
        print(f"{context_name}:")
        for file in files:
            if os.path.exists(file):
                print(f"  ✓ {file} - Found")
            else:
                print(f"  ✗ {file} - MISSING")
                missing_files.append(file)
                all_present = False
        print()

    if all_present:
        print("✓ All required context files are present!")
        print("You can proceed with the evaluation.")
    else:
        print(f"✗ {len(missing_files)} file(s) are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease ensure all required files are in the current directory.")

        # Check if original script exists
        if os.path.exists('3D_Gen.py'):
            print("\nTip: You can run your original script to generate these files:")
            print("  python 3D_Gen.py")

    return all_present


if __name__ == "__main__":
    check_required_files()