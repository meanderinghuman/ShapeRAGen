"""
STL Dimension Analyzer for PyCharm

This script analyzes STL files to extract dimensions and statistics.
Simply run it in PyCharm and it will prompt you for a file or directory to analyze.

Required packages:
  - numpy
  - trimesh
  - matplotlib

If you get import errors, install the requirements in your PyCharm venv:
  1. In PyCharm, go to: File > Settings > Project > Python Interpreter
  2. Click the + button
  3. Search for and install: numpy, trimesh, matplotlib
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import traceback

# Try importing required packages and provide helpful messages if they're missing
try:
    import numpy as np
except ImportError:
    print("Error: numpy package is missing.")
    print("Install it in PyCharm via: File > Settings > Project > Python Interpreter > + > search 'numpy'")
    input("Press Enter to exit...")
    sys.exit(1)

try:
    import trimesh
except ImportError:
    print("Error: trimesh package is missing.")
    print("Install it in PyCharm via: File > Settings > Project > Python Interpreter > + > search 'trimesh'")
    input("Press Enter to exit...")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.colors import LightSource
except ImportError:
    print("Error: matplotlib package is missing.")
    print("Install it in PyCharm via: File > Settings > Project > Python Interpreter > + > search 'matplotlib'")
    input("Press Enter to exit...")
    sys.exit(1)


def analyze_stl(file_path, expected_dimensions=None, visualize=False):
    """
    Analyze an STL file to extract dimensions and other metrics.

    Args:
        file_path (str): Path to the STL file
        expected_dimensions (tuple, optional): Expected dimensions as (width, length, depth)
        visualize (bool): Whether to visualize the mesh

    Returns:
        dict: Dictionary containing the analysis results
    """
    try:
        # Load the mesh
        mesh = trimesh.load(file_path)

        # Calculate dimensions
        bounds = mesh.bounds
        min_bounds = bounds[0]
        max_bounds = bounds[1]

        dimensions = max_bounds - min_bounds
        width, length, depth = dimensions

        # Calculate volume and center of mass
        volume = mesh.volume
        center_of_mass = mesh.center_mass

        # Count faces and vertices
        num_faces = len(mesh.faces)
        num_vertices = len(mesh.vertices)

        # Check if the mesh is watertight (manifold)
        is_watertight = mesh.is_watertight

        # Create result dictionary
        result = {
            'file_name': os.path.basename(file_path),
            'dimensions': {
                'width': width,
                'length': length,
                'depth': depth
            },
            'volume': volume,
            'center_of_mass': center_of_mass,
            'num_faces': num_faces,
            'num_vertices': num_vertices,
            'is_watertight': is_watertight
        }

        # Compare with expected dimensions if provided
        if expected_dimensions is not None:
            exp_width, exp_length, exp_depth = expected_dimensions
            width_diff = abs(width - exp_width)
            length_diff = abs(length - exp_length)
            depth_diff = abs(depth - exp_depth)

            # Calculate percentage differences
            width_pct_diff = (width_diff / exp_width) * 100 if exp_width > 0 else float('inf')
            length_pct_diff = (length_diff / exp_length) * 100 if exp_length > 0 else float('inf')
            depth_pct_diff = (depth_diff / exp_depth) * 100 if exp_depth > 0 else float('inf')

            # Add dimension comparison to result
            result['dimension_comparison'] = {
                'expected': {
                    'width': exp_width,
                    'length': exp_length,
                    'depth': exp_depth
                },
                'absolute_diff': {
                    'width': width_diff,
                    'length': length_diff,
                    'depth': depth_diff
                },
                'percentage_diff': {
                    'width': width_pct_diff,
                    'length': length_pct_diff,
                    'depth': depth_pct_diff
                }
            }

        # Visualize the mesh if requested
        if visualize:
            visualize_mesh(mesh, result)

        return result

    except Exception as e:
        print(f"Error analyzing STL file: {e}")
        traceback.print_exc()
        return None


def visualize_mesh(mesh, analysis_result=None):
    """
    Visualize the mesh and optionally display analysis information.

    Args:
        mesh (trimesh.Trimesh): The mesh to visualize
        analysis_result (dict, optional): Analysis results to display
    """
    # Create a figure with 2 subplots
    fig = plt.figure(figsize=(12, 6))

    # 3D visualization
    ax1 = fig.add_subplot(121, projection='3d')

    # Get mesh data
    vertices = mesh.vertices
    faces = mesh.faces

    # Plot the triangles
    tri = ax1.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2],
                          triangles=faces, cmap='viridis', alpha=0.8)

    # Set equal aspect ratio
    ax1.set_box_aspect([1,1,1])

    # Add title and labels
    ax1.set_title('3D Model Visualization')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    # Information panel
    if analysis_result:
        ax2 = fig.add_subplot(122)
        ax2.axis('off')

        # Create text for the information panel
        info_text = f"File: {analysis_result['file_name']}\n\n"
        info_text += "Dimensions:\n"
        info_text += f"  Width:  {analysis_result['dimensions']['width']:.2f} mm\n"
        info_text += f"  Length: {analysis_result['dimensions']['length']:.2f} mm\n"
        info_text += f"  Depth:  {analysis_result['dimensions']['depth']:.2f} mm\n\n"

        info_text += f"Volume: {analysis_result['volume']:.2f} mm³\n"
        info_text += f"Faces: {analysis_result['num_faces']}\n"
        info_text += f"Vertices: {analysis_result['num_vertices']}\n"
        info_text += f"Watertight: {'Yes' if analysis_result['is_watertight'] else 'No'}\n"

        # Add expected dimension comparison if available
        if 'dimension_comparison' in analysis_result:
            exp = analysis_result['dimension_comparison']['expected']
            pct_diff = analysis_result['dimension_comparison']['percentage_diff']

            info_text += "\nExpected Dimensions:\n"
            info_text += f"  Width:  {exp['width']:.2f} mm ({pct_diff['width']:.1f}% diff)\n"
            info_text += f"  Length: {exp['length']:.2f} mm ({pct_diff['length']:.1f}% diff)\n"
            info_text += f"  Depth:  {exp['depth']:.2f} mm ({pct_diff['depth']:.1f}% diff)\n"

        ax2.text(0.05, 0.95, info_text, va='top', ha='left', fontfamily='monospace')

    plt.tight_layout()
    plt.show()


def print_analysis_result(result):
    """
    Print the analysis result in a formatted way.

    Args:
        result (dict): The analysis result dictionary
    """
    if not result:
        return

    print(f"Analysis for: {result['file_name']}")
    print("-" * 50)

    # Print dimensions
    print(f"Dimensions:")
    print(f"  Width:  {result['dimensions']['width']:.2f} mm")
    print(f"  Length: {result['dimensions']['length']:.2f} mm")
    print(f"  Depth:  {result['dimensions']['depth']:.2f} mm")

    # Print other metrics
    print(f"\nVolume: {result['volume']:.2f} mm³")
    print(f"Faces: {result['num_faces']}")
    print(f"Vertices: {result['num_vertices']}")
    print(f"Watertight: {'Yes' if result['is_watertight'] else 'No'}")

    # Print expected dimension comparison if available
    if 'dimension_comparison' in result:
        exp = result['dimension_comparison']['expected']
        abs_diff = result['dimension_comparison']['absolute_diff']
        pct_diff = result['dimension_comparison']['percentage_diff']

        print("\nExpected Dimensions:")
        print(f"  Width:  {exp['width']:.2f} mm (diff: {abs_diff['width']:.2f} mm, {pct_diff['width']:.1f}%)")
        print(f"  Length: {exp['length']:.2f} mm (diff: {abs_diff['length']:.2f} mm, {pct_diff['length']:.1f}%)")
        print(f"  Depth:  {exp['depth']:.2f} mm (diff: {abs_diff['depth']:.2f} mm, {pct_diff['depth']:.1f}%)")

        # Add a summary of how well it matches
        avg_pct_diff = (pct_diff['width'] + pct_diff['length'] + pct_diff['depth']) / 3
        if avg_pct_diff < 5:
            print("\nDimension Match: Excellent (< 5% difference)")
        elif avg_pct_diff < 10:
            print("\nDimension Match: Good (< 10% difference)")
        elif avg_pct_diff < 20:
            print("\nDimension Match: Fair (< 20% difference)")
        else:
            print("\nDimension Match: Poor (> 20% difference)")


def parse_expected_dimensions(dims_str):
    """
    Parse a comma-separated string of dimensions into a tuple of floats.

    Args:
        dims_str (str): Comma-separated string of dimensions (width,length,depth)

    Returns:
        tuple: Tuple of (width, length, depth) as floats
    """
    try:
        return tuple(float(x) for x in dims_str.split(','))
    except Exception as e:
        print(f"Error parsing dimensions: {e}")
        print("Expected format: width,length,depth (e.g., 20,30,40)")
        return None


def add_shape_dimensions_from_name(filename):
    """
    Try to extract shape and dimensions based on the shape name.

    Args:
        filename (str): The filename to parse

    Returns:
        tuple: (shape_name, dimensions) or (None, None) if parsing fails
    """
    try:
        # Remove extension and split parts
        base_name = os.path.basename(filename).replace('.stl', '')
        parts = base_name.split('_')

        # Get shape name (first part)
        shape_name = parts[0].lower()

        # Hard-coded expected dimensions based on shape name
        if shape_name == 'box':
            return shape_name, (30, 20, 40)  # width, length, depth
        elif shape_name == 'cylinder':
            return shape_name, (30, 30, 40)  # diameter, length, diameter
        elif shape_name == 'cone':
            return shape_name, (40, 40, 35)  # base diameter, length, base diameter
        elif shape_name == 'pyramid':
            return shape_name, (25, 25, 30)  # base width, length, base depth
        elif shape_name == 'sphere':
            return shape_name, (90, 90, 90)  # diameter in each dimension

        return shape_name, None
    except Exception:
        return None, None


def batch_analyze_directory(directory_path):
    """
    Analyze all STL files in a directory.

    Args:
        directory_path (str): Path to the directory containing STL files

    Returns:
        list: List of analysis results for each STL file
    """
    results = []

    stl_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.stl')]

    if not stl_files:
        print(f"No STL files found in {directory_path}")
        return results

    print(f"Found {len(stl_files)} STL files to analyze")

    for filename in stl_files:
        file_path = os.path.join(directory_path, filename)
        print(f"\nAnalyzing {filename}...")

        # Try to get expected dimensions from filename
        shape_name, expected_dims = add_shape_dimensions_from_name(filename)

        if expected_dims:
            print(f"Detected shape '{shape_name}' with expected dimensions: {expected_dims}")

        # Analyze the file
        result = analyze_stl(file_path, expected_dims)
        if result:
            results.append(result)
            print_analysis_result(result)
            print("-" * 80)

    return results


def generate_report(results, output_file=None):
    """
    Generate a report summarizing the analysis results.

    Args:
        results (list): List of analysis results
        output_file (str, optional): Path to save the report
    """
    if not results:
        print("No results to generate report from.")
        return

    # Basic statistics
    num_files = len(results)
    num_watertight = sum(1 for r in results if r['is_watertight'])

    # Calculate dimension match statistics
    dimension_match_counts = {'Excellent': 0, 'Good': 0, 'Fair': 0, 'Poor': 0}
    dimension_match_percentages = []

    for result in results:
        if 'dimension_comparison' in result:
            pct_diff = result['dimension_comparison']['percentage_diff']
            avg_pct_diff = (pct_diff['width'] + pct_diff['length'] + pct_diff['depth']) / 3
            dimension_match_percentages.append(avg_pct_diff)

            if avg_pct_diff < 5:
                dimension_match_counts['Excellent'] += 1
            elif avg_pct_diff < 10:
                dimension_match_counts['Good'] += 1
            elif avg_pct_diff < 20:
                dimension_match_counts['Fair'] += 1
            else:
                dimension_match_counts['Poor'] += 1

    # Build report text
    report_text = "STL Analysis Report\n"
    report_text += "=" * 50 + "\n\n"

    report_text += f"Number of files analyzed: {num_files}\n"
    report_text += f"Number of watertight models: {num_watertight} ({num_watertight/num_files*100:.1f}%)\n\n"

    if dimension_match_percentages:
        report_text += "Dimension Match Statistics:\n"
        for category in ['Excellent', 'Good', 'Fair', 'Poor']:
            count = dimension_match_counts[category]
            percentage = count/len(dimension_match_percentages)*100 if dimension_match_percentages else 0
            report_text += f"  {category}: {count} ({percentage:.1f}%)\n"

        report_text += f"\nAverage dimension difference: {sum(dimension_match_percentages)/len(dimension_match_percentages):.2f}%\n\n"

    # Summary of each file
    report_text += "Individual File Summaries:\n"
    report_text += "-" * 50 + "\n\n"

    for result in results:
        report_text += f"File: {result['file_name']}\n"
        report_text += f"  Dimensions (mm): {result['dimensions']['width']:.1f} x {result['dimensions']['length']:.1f} x {result['dimensions']['depth']:.1f}\n"

        if 'dimension_comparison' in result:
            exp = result['dimension_comparison']['expected']
            pct_diff = result['dimension_comparison']['percentage_diff']
            avg_pct_diff = (pct_diff['width'] + pct_diff['length'] + pct_diff['depth']) / 3

            report_text += f"  Expected (mm): {exp['width']:.1f} x {exp['length']:.1f} x {exp['depth']:.1f}\n"
            report_text += f"  Avg Difference: {avg_pct_diff:.1f}%\n"

            # Add match rating
            if avg_pct_diff < 5:
                match_rating = "Excellent"
            elif avg_pct_diff < 10:
                match_rating = "Good"
            elif avg_pct_diff < 20:
                match_rating = "Fair"
            else:
                match_rating = "Poor"
            report_text += f"  Match Rating: {match_rating}\n"

        report_text += f"  Watertight: {'Yes' if result['is_watertight'] else 'No'}\n"
        report_text += "\n"

    # Print report
    print(report_text)

    # Save to file if requested
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report_text)
        print(f"Report saved to {output_file}")

    return report_text


class STLAnalyzerGUI:
    """Simple GUI for STL file analysis"""

    def __init__(self, root):
        self.root = root
        self.root.title("STL Dimension Analyzer")
        self.root.geometry("500x600")
        self.root.resizable(True, True)

        self.setup_ui()

    def setup_ui(self):
        # Create frames
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)

        middle_frame = tk.Frame(self.root, padx=10, pady=10)
        middle_frame.pack(fill=tk.X)

        self.result_frame = tk.Frame(self.root, padx=10, pady=10)
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        # File selection
        tk.Label(top_frame, text="Select an STL file or directory:").pack(anchor=tk.W)

        file_frame = tk.Frame(top_frame)
        file_frame.pack(fill=tk.X, pady=5)

        self.path_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.path_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(file_frame, text="Browse File", command=self.browse_file).pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="Browse Dir", command=self.browse_directory).pack(side=tk.LEFT)

        # Expected dimensions
        tk.Label(top_frame, text="Expected Dimensions (width,length,depth in mm):").pack(anchor=tk.W)

        self.expected_dims_var = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.expected_dims_var, width=20).pack(anchor=tk.W)

        # Options
        options_frame = tk.Frame(middle_frame)
        options_frame.pack(fill=tk.X)

        self.visualize_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Visualize Model", variable=self.visualize_var).pack(side=tk.LEFT)

        self.batch_var = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Batch Mode (Directory)", variable=self.batch_var).pack(side=tk.LEFT, padx=10)

        # Action buttons
        button_frame = tk.Frame(middle_frame)
        button_frame.pack(fill=tk.X, pady=10)

        tk.Button(button_frame, text="Analyze", command=self.run_analysis, bg="#4CAF50", fg="white", padx=20).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Save Report", command=self.save_report).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Clear", command=self.clear_results).pack(side=tk.LEFT)

        # Results display
        tk.Label(self.result_frame, text="Results:").pack(anchor=tk.W)

        # Create scrollable text widget for results
        scrollbar = tk.Scrollbar(self.result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text = tk.Text(self.result_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.result_text.yview)

        # Initialize variables
        self.results = []
        self.report_text = ""

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an STL file",
            filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
        )
        if file_path:
            self.path_var.set(file_path)
            self.batch_var.set(False)

    def browse_directory(self):
        dir_path = filedialog.askdirectory(title="Select a directory containing STL files")
        if dir_path:
            self.path_var.set(dir_path)
            self.batch_var.set(True)

    def run_analysis(self):
        # Clear previous results
        self.clear_results()

        # Get path
        path = self.path_var.get()
        if not path:
            messagebox.showerror("Error", "Please select an STL file or directory")
            return

        # Check if path exists
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Path does not exist: {path}")
            return

        # Get expected dimensions
        expected_dims = None
        if self.expected_dims_var.get():
            expected_dims = parse_expected_dimensions(self.expected_dims_var.get())
            if not expected_dims:
                messagebox.showerror("Error", "Invalid expected dimensions format. Use width,length,depth (e.g., 20,30,40)")
                return

        # Run analysis
        try:
            if self.batch_var.get() or os.path.isdir(path):
                self.result_text.insert(tk.END, f"Batch analyzing STL files in '{path}'...\n\n")
                self.results = batch_analyze_directory(path)
                if self.results:
                    self.report_text = generate_report(self.results)
                    self.result_text.insert(tk.END, self.report_text)
                else:
                    self.result_text.insert(tk.END, "No valid STL files found or analysis failed.")
            else:
                self.result_text.insert(tk.END, f"Analyzing '{path}'...\n\n")

                # If expected dimensions not provided, try to infer from filename
                if not expected_dims:
                    shape_name, inferred_dims = add_shape_dimensions_from_name(path)
                    if inferred_dims:
                        self.result_text.insert(tk.END, f"Detected shape '{shape_name}' with expected dimensions: {inferred_dims}\n\n")
                        expected_dims = inferred_dims

                result = analyze_stl(path, expected_dims, self.visualize_var.get())
                if result:
                    self.results = [result]
                    # Convert result to text
                    import io
                    with io.StringIO() as buffer:
                        print_analysis_result(result)
                        buffer.write("\n")
                        self.report_text = buffer.getvalue()

                    self.result_text.insert(tk.END, self.report_text)
                else:
                    self.result_text.insert(tk.END, "Analysis failed. Check if the file is a valid STL.")

        except Exception as e:
            self.result_text.insert(tk.END, f"Error during analysis: {str(e)}\n\n")
            traceback.print_exc()
            self.result_text.insert(tk.END, traceback.format_exc())

    def save_report(self):
        if not self.report_text:
            messagebox.showinfo("Info", "No analysis results to save")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Report",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.report_text)
                messagebox.showinfo("Success", f"Report saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.results = []
        self.report_text = ""


def run_gui():
    """Run the GUI application"""
    root = tk.Tk()
    app = STLAnalyzerGUI(root)
    root.mainloop()


def simple_cli():
    """Simple command-line interface for direct script execution"""
    print("STL Dimension Analyzer")
    print("=" * 50)

    # Check if a file was provided as an argument
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        path = sys.argv[1]
        print(f"Using file from command line: {path}")
    else:
        # Ask for a file or directory
        print("Enter path to an STL file or directory (or press Enter to browse):")
        path = input("> ").strip()

        if not path:
            # Create a root window just for the file dialog
            root = tk.Tk()
            root.withdraw()  # Hide the main window

            path = filedialog.askopenfilename(
                title="Select an STL file",
                filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
            )

            if not path:
                print("No file selected. Exiting.")
                return

    # Check if path exists
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        return

    # Ask for expected dimensions
    print("Enter expected dimensions as width,length,depth (in mm) or leave blank:")
    dims_str = input("> ").strip()

    expected_dims = None
    if dims_str:
        expected_dims = parse_expected_dimensions(dims_str)
        if not expected_dims:
            return

    # Batch analysis of directory
    if os.path.isdir(path):
        print(f"Batch analyzing STL files in '{path}'...")
        results = batch_analyze_directory(path)

        if results:
            print("\nGenerate a report? (y/n)")
            if input("> ").strip().lower() in ['y', 'yes']:
                print("\nEnter report file name (or leave blank for console only):")
                report_file = input("> ").strip()
                generate_report(results, report_file if report_file else None)

    # Single file analysis
    elif os.path.isfile(path):
        if not path.lower().endswith('.stl'):
            print(f"Error: '{path}' is not an STL file.")
            return

        print(f"Analyzing '{path}'...")

        # If expected dimensions not provided, try to infer from filename
        if not expected_dims:
            shape_name, inferred_dims = add_shape_dimensions_from_name(path)
            if inferred_dims:
                print(f"Detected shape '{shape_name}' with expected dimensions: {inferred_dims}")
                print("Use these dimensions? (y/n)")
                if input("> ").strip().lower() in ['y', 'yes']:
                    expected_dims = inferred_dims

        print("Visualize the model? (y/n)")
        visualize = input("> ").strip().lower() in ['y', 'yes']

        result = analyze_stl(path, expected_dims, visualize)
        if result:
            print_analysis_result(result)

    else:
        print(f"Error: '{path}' is neither a file nor a directory.")

    print("\nAnalysis complete!")
    input("Press Enter to exit...")


if __name__ == "__main__":
    # Check if we're running in PyCharm
    is_pycharm = 'PYCHARM_HOSTED' in os.environ or 'JETBRAINS_REMOTE_RUN' in os.environ

    if is_pycharm:
        # If running in PyCharm, use the GUI interface
        run_gui()
    else:
        # Otherwise, use the command-line interface
        try:
            simple_cli()
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            input("Press Enter to exit...")