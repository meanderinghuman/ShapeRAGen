import openai
import subprocess
import tempfile
import os
import time
import shutil
import re
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
from typing import Dict, List, Tuple
import traceback


class RAGEvaluationSystem:
    def __init__(self, api_key: str, api_base: str):
        """Initialize the evaluation system with API credentials"""
        self.api_key = api_key
        self.api_base = api_base
        openai.api_key = api_key
        openai.api_base = api_base

        # Initialize embedder
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Load or create contexts
        self.tri_docs_chunks, self.tri_docs_embeddings = self.load_context("tri_docs")
        self.numpy_stl_chunks, self.numpy_stl_embeddings = self.load_context("numpy_stl")
        self.tri_custom_chunks, self.tri_custom_embeddings = self.load_context("tri_custom")
        self.best_practices_chunks, self.best_practices_embeddings = self.load_context("best_practices")

        # Define test shapes
        self.test_shapes = {
            'box': "Create a hollow box with base sides 20mm and 30mm, height 40mm",
            'cylinder': "Create a hollow cylinder with radius 15mm, height 40mm",
            'cone': "Create a hollow cone with base radius 20mm, height 35mm",
            'pyramid': "Create a hollow pyramid with base 25mm x 25mm, height 30mm",
            'sphere': "Create a sphere with radius 45mm"
        }

        # Evaluation conditions
        self.conditions = {
            'baseline': {'use_rag': False, 'use_review': False},
            'rag_only': {'use_rag': True, 'use_review': False},
            'review_only': {'use_rag': False, 'use_review': True},
            'full_system': {'use_rag': True, 'use_review': True}
        }

        # Results storage
        self.results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = f"evaluation_results_{self.timestamp}"
        os.makedirs(self.results_dir, exist_ok=True)

    def load_context(self, context_type: str) -> Tuple[List[str], np.ndarray]:
        """Load existing context or return empty if not found"""
        emb_file = f"{context_type}_embeddings.npy"
        chunks_file = f"{context_type}_chunks.pkl"

        if os.path.exists(emb_file) and os.path.exists(chunks_file):
            embeddings = np.load(emb_file)
            with open(chunks_file, "rb") as f:
                chunks = pickle.load(f)
            return chunks, embeddings
        else:
            print(f"Warning: Context files for {context_type} not found")
            return [], np.array([])

    def retrieve_context(self, query: str, k: int = 3) -> str:
        """Retrieve relevant context using the existing RAG system"""
        if len(self.tri_docs_chunks) == 0:
            return ""

        # Retrieve from each source
        tri_docs_context = self._retrieve_from_source(
            query, self.tri_docs_chunks, self.tri_docs_embeddings, k
        )
        numpy_stl_context = self._retrieve_from_source(
            query, self.numpy_stl_chunks, self.numpy_stl_embeddings, k
        )
        tri_custom_context = self._retrieve_from_source(
            query, self.tri_custom_chunks, self.tri_custom_embeddings, k
        )
        best_practices_context = self._retrieve_from_source(
            query, self.best_practices_chunks, self.best_practices_embeddings, k
        )

        # Combine contexts
        combined_context = (
                "Trimesh Documentation context:\n" + tri_docs_context +
                "\n\nNumPy-STL Documentation context:\n" + numpy_stl_context +
                "\n\nCustom Trimesh Functions context:\n" + tri_custom_context +
                "\n\n3D Printing Best Practices context:\n" + best_practices_context
        )

        return combined_context

    def _retrieve_from_source(self, query: str, chunks: List[str], embeddings: np.ndarray, k: int) -> str:
        """Retrieve from a specific source"""
        if len(chunks) == 0:
            return ""

        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        query_emb = self.embedder.encode([query])
        query_emb = np.array(query_emb, dtype=np.float32)

        distances, indices = index.search(query_emb, k)
        retrieved = [chunks[idx] for idx in indices[0]]

        return "\n\n".join(retrieved)

    def generate_code(self, prompt: str, extra_context: str = "") -> str:
        """Generate code using the existing function"""
        messages = [
            {"role": "system", "content": (
                "You are a helpful assistant that writes correct Python code. "
                "Your task is to generate code that uses the 'trimesh' and 'numpy-stl' libraries to create hollow 3D shapes "
                "and export it as an STL file named 'output.stl'. Ensure the mesh is suitable for FDM printing. "
                "All explanations and commentary should be placed before or after the code block, not within it. "
                "Always wrap your code in markdown code blocks with ```python at the start and ``` at the end. "
                "The code block should only contain valid, executable Python code with no comments that are not meant to be executed. "
                "Always include necessary imports like 'import trimesh', 'import numpy as np', and 'from stl import mesh' within the code block. "
                "Do not generate harmful code."
            )},
            {"role": "user", "content": prompt + "\n" + extra_context}
        ]

        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )

        return response.choices[0].message.content.strip()

    def extract_code_from_markdown(self, text: str) -> str:
        """Extract Python code from markdown blocks"""
        pattern = r'```(?:python)?\s*([\s\S]*?)```'
        matches = re.findall(pattern, text)

        if not matches:
            return ""

        return "\n\n".join(match.strip() for match in matches)

    def test_code(self, code: str) -> Tuple[bool, str, str]:
        """Test code execution and return success status, stdout, and stderr"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py", encoding="utf-8") as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"

            result = subprocess.run(
                ["python", temp_file_path],
                capture_output=True,
                text=True,
                timeout=20,
                env=env
            )

            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            # Check if output.stl was created
            success = not stderr and os.path.exists("output.stl")

            return success, stdout, stderr

        except subprocess.TimeoutExpired:
            return False, "", "Execution timed out"
        except Exception as e:
            return False, "", str(e)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def review_code(self, code: str, context: str) -> str:
        """Review and refine code using the existing review function"""
        review_prompt = (
                "Please review the following Python code based on the provided documentation and best practices for 3D printing. "
                "If improvements are needed, return an updated version of the code; otherwise, return the code as is.\n\n"
                "Wrap your final code inside ```python and ``` markdown code blocks. "
                "The code block should only contain valid, executable Python code. "
                "All explanations should be outside the code block.\n\n"
                "Code:\n" + code + "\n\nContext:\n" + context
        )

        messages = [
            {"role": "system", "content": (
                "You are a helpful assistant that reviews and refines Python code for creating 3D printing models using 'trimesh' and/or 'numpy-stl'. "
                "Ensure the mesh is suitable for FDM printing with emphasis on minimum wall thickness and supports where needed. "
                "Take note of contact points between the shape and its support(s). "
                "Your review should consider best practices and documentation guidelines, and if the code can be improved, return an updated version. "
                "Always wrap your code in markdown code blocks with ```python at the start and ``` at the end. "
                "The code block should only contain valid, executable Python code with no comments that are not meant to be executed. "
                "Always include necessary imports like 'import trimesh', 'import numpy as np', or 'from stl import mesh' within the code block. "
                "Do not generate harmful code."
            )},
            {"role": "user", "content": review_prompt}
        ]

        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )

        return response.choices[0].message.content.strip()

    def run_single_test(self, shape: str, condition: str, run_number: int) -> Dict:
        """Run a single test with specified parameters"""
        start_time = time.time()
        iterations = 0
        success = False
        errors = []
        context_used = ""

        # Get shape prompt
        prompt = self.test_shapes[shape]

        # Get condition settings
        settings = self.conditions[condition]
        use_rag = settings['use_rag']
        use_review = settings['use_review']

        # Retrieve context if needed
        if use_rag:
            context_used = self.retrieve_context(prompt)

        # Iterative generation process
        extra_context = context_used
        final_code = None

        while iterations < 5 and not success:
            iterations += 1

            # Generate code
            generated_response = self.generate_code(prompt, extra_context)
            code = self.extract_code_from_markdown(generated_response)

            if not code:
                errors.append(f"Iteration {iterations}: No valid code block found")
                continue

            # Test code
            success, stdout, stderr = self.test_code(code)

            if success:
                final_code = code

                # Review if needed
                if use_review:
                    reviewed_response = self.review_code(code, context_used)
                    reviewed_code = self.extract_code_from_markdown(reviewed_response)

                    if reviewed_code:
                        review_success, review_stdout, review_stderr = self.test_code(reviewed_code)

                        if review_success:
                            final_code = reviewed_code
                        else:
                            errors.append(f"Review failed: {review_stderr}")

                break
            else:
                errors.append(f"Iteration {iterations}: {stderr}")
                extra_context = context_used + f"\n\nError in iteration {iterations}: {stderr}"

        # Clean up and save results
        end_time = time.time()
        execution_time = end_time - start_time

        # Save generated STL if successful
        stl_filename = None
        if success and os.path.exists("output.stl"):
            stl_filename = f"{shape}_{condition}_run{run_number}.stl"
            stl_path = os.path.join(self.results_dir, stl_filename)
            shutil.move("output.stl", stl_path)

        # Save final code
        code_filename = f"{shape}_{condition}_run{run_number}.py"
        code_path = os.path.join(self.results_dir, code_filename)
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(final_code if final_code else "# No successful code generated")

        return {
            'shape': shape,
            'condition': condition,
            'run_number': run_number,
            'success': success,
            'iterations': iterations,
            'execution_time': execution_time,
            'errors': errors,
            'stl_file': stl_filename,
            'code_file': code_filename,
            'timestamp': datetime.now().isoformat()
        }

    def run_primary_evaluation(self, runs_per_shape: int = 10):
        """Run primary evaluation focusing on DeepSeek with all conditions"""
        print("Starting primary evaluation...")
        total_tests = len(self.test_shapes) * len(self.conditions) * runs_per_shape
        current_test = 0

        for shape in self.test_shapes:
            for condition in self.conditions:
                for run in range(runs_per_shape):
                    current_test += 1
                    print(f"\nTest {current_test}/{total_tests}")
                    print(f"Shape: {shape}, Condition: {condition}, Run: {run + 1}")

                    try:
                        result = self.run_single_test(shape, condition, run + 1)
                        self.results.append(result)

                        # Save after each test
                        self.save_results()

                    except Exception as e:
                        print(f"Error in test: {str(e)}")
                        traceback.print_exc()

                    # Clean up any leftover files
                    if os.path.exists("output.stl"):
                        os.remove("output.stl")

    def save_results(self):
        """Save current results to files"""
        # Save raw results as JSON
        json_path = os.path.join(self.results_dir, "raw_results.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)

        # Save as CSV for analysis
        df = pd.DataFrame(self.results)
        csv_path = os.path.join(self.results_dir, "results.csv")
        df.to_csv(csv_path, index=False)

    def analyze_results(self):
        """Analyze results and create visualizations"""
        df = pd.DataFrame(self.results)

        # 1. Success rate by condition
        success_by_condition = df.groupby('condition')['success'].mean() * 100

        plt.figure(figsize=(10, 6))
        success_by_condition.plot(kind='bar')
        plt.title('Success Rate by Condition')
        plt.ylabel('Success Rate (%)')
        plt.xlabel('Condition')
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'success_by_condition.png'))
        plt.close()

        # 2. Average iterations by condition
        avg_iterations = df[df['success'] == True].groupby('condition')['iterations'].mean()

        plt.figure(figsize=(10, 6))
        avg_iterations.plot(kind='bar')
        plt.title('Average Iterations to Success')
        plt.ylabel('Iterations')
        plt.xlabel('Condition')
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'iterations_by_condition.png'))
        plt.close()

        # 3. Success rate by shape
        success_by_shape = df.groupby(['shape', 'condition'])['success'].mean() * 100

        plt.figure(figsize=(12, 8))
        success_by_shape.unstack().plot(kind='bar')
        plt.title('Success Rate by Shape and Condition')
        plt.ylabel('Success Rate (%)')
        plt.xlabel('Shape')
        plt.legend(title='Condition')
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'success_by_shape.png'))
        plt.close()

        # 4. NEW: Execution time by condition
        execution_time_by_condition = df.groupby('condition')['execution_time'].mean()

        plt.figure(figsize=(10, 6))
        execution_time_by_condition.plot(kind='bar')
        plt.title('Average Execution Time by Condition')
        plt.ylabel('Time (seconds)')
        plt.xlabel('Condition')
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'execution_time_by_condition.png'))
        plt.close()

        # 5. NEW: Execution time boxplot
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='condition', y='execution_time', data=df)
        plt.title('Execution Time Distribution by Condition')
        plt.ylabel('Time (seconds)')
        plt.xlabel('Condition')
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'execution_time_boxplot.png'))
        plt.close()

        # 6. NEW: Combined metrics comparison
        # Normalize metrics for comparison
        success_norm = df.groupby('condition')['success'].mean() / df.groupby('condition')['success'].mean().max()
        time_norm = df.groupby('condition')['execution_time'].mean() / df.groupby('condition')[
            'execution_time'].mean().max()
        iterations_norm = df[df['success'] == True].groupby('condition')['iterations'].mean() / \
                          df[df['success'] == True].groupby('condition')['iterations'].mean().max()

        # Create combined metrics dataframe
        combined_metrics = pd.DataFrame({
            'Success Rate': success_norm,
            'Execution Time (lower is better)': 1 - time_norm,  # Invert so lower is better
            'Iterations (lower is better)': 1 - iterations_norm  # Invert so lower is better
        })

        plt.figure(figsize=(10, 6))
        combined_metrics.plot(kind='bar')
        plt.title('Normalized Performance Metrics by Condition')
        plt.ylabel('Performance (higher is better)')
        plt.xlabel('Condition')
        plt.ylim(0, 1.1)
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'combined_metrics.png'))
        plt.close()

        # 4. RAG impact analysis
        rag_conditions = df[df['condition'].isin(['rag_only', 'full_system'])]
        no_rag_conditions = df[df['condition'].isin(['baseline', 'review_only'])]

        rag_success = rag_conditions['success'].mean() * 100
        no_rag_success = no_rag_conditions['success'].mean() * 100
        rag_improvement = rag_success - no_rag_success

        # Time comparison
        rag_time = rag_conditions['execution_time'].mean()
        no_rag_time = no_rag_conditions['execution_time'].mean()
        time_difference = rag_time - no_rag_time

        # 5. Summary statistics
        summary_stats = {
            'Overall Success Rate': f"{df['success'].mean() * 100:.1f}%",
            'RAG Improvement': f"{rag_improvement:.1f}%",
            'Best Condition': success_by_condition.idxmax(),
            'Best Condition Success Rate': f"{success_by_condition.max():.1f}%",
            'Average Iterations (Success)': f"{df[df['success'] == True]['iterations'].mean():.2f}",
            'Hardest Shape': df.groupby('shape')['success'].mean().idxmin(),
            'Easiest Shape': df.groupby('shape')['success'].mean().idxmax(),
            'Average Execution Time': f"{df['execution_time'].mean():.2f} seconds",
            'Time Difference (RAG vs No RAG)': f"{time_difference:.2f} seconds ({(time_difference / no_rag_time) * 100:.1f}%)"
        }

        # Save summary
        with open(os.path.join(self.results_dir, 'summary.txt'), 'w') as f:
            f.write("EVALUATION SUMMARY\n")
            f.write("==================\n\n")
            for key, value in summary_stats.items():
                f.write(f"{key}: {value}\n")

        return summary_stats

    def create_dashboard(self):
        """Create an HTML dashboard for results"""
        df = pd.DataFrame(self.results)

        html = f"""
        <html>
        <head>
            <title>RAG Evaluation Results - {self.timestamp}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
                .success {{ background-color: #d4edda; }}
                .failure {{ background-color: #f8d7da; }}
                img {{ max-width: 100%; height: auto; margin: 20px 0; }}
                .summary {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
                .chart-container {{ display: flex; flex-wrap: wrap; justify-content: space-between; }}
                .chart {{ width: 48%; margin-bottom: 20px; }}
                @media (max-width: 768px) {{ .chart {{ width: 100%; }} }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>RAG Evaluation Results</h1>
                <p>Evaluation completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

                <div class="summary">
                    <h2>Summary Statistics</h2>
                    <ul>
        """

        # Add summary statistics
        summary_stats = self.analyze_results()
        for key, value in summary_stats.items():
            html += f"<li><strong>{key}:</strong> {value}</li>"

        html += """
                    </ul>
                </div>

                <h2>Success Rate and Performance Charts</h2>
                <div class="chart-container">
                    <div class="chart">
                        <h3>Success Rate by Condition</h3>
                        <img src="success_by_condition.png" alt="Success Rate by Condition">
                    </div>
                    <div class="chart">
                        <h3>Average Iterations to Success</h3>
                        <img src="iterations_by_condition.png" alt="Average Iterations">
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart">
                        <h3>Success Rate by Shape</h3>
                        <img src="success_by_shape.png" alt="Success by Shape">
                    </div>
                    <div class="chart">
                        <h3>Combined Performance Metrics</h3>
                        <img src="combined_metrics.png" alt="Combined Metrics">
                    </div>
                </div>

                <h2>Execution Time Analysis</h2>
                <div class="chart-container">
                    <div class="chart">
                        <h3>Average Execution Time by Condition</h3>
                        <img src="execution_time_by_condition.png" alt="Execution Time">
                    </div>
                    <div class="chart">
                        <h3>Execution Time Distribution</h3>
                        <img src="execution_time_boxplot.png" alt="Time Distribution">
                    </div>
                </div>

                <h2>Detailed Results</h2>
                <table>
                    <tr>
                        <th>Shape</th>
                        <th>Condition</th>
                        <th>Success Rate</th>
                        <th>Avg Iterations</th>
                        <th>Avg Time (s)</th>
                    </tr>
        """

        # Add detailed results table
        grouped_results = df.groupby(['shape', 'condition']).agg({
            'success': 'mean',
            'iterations': 'mean',
            'execution_time': 'mean'
        }).reset_index()

        for _, row in grouped_results.iterrows():
            success_class = 'success' if row['success'] > 0.7 else 'failure' if row['success'] < 0.3 else ''
            html += f"""
                <tr>
                    <td>{row['shape']}</td>
                    <td>{row['condition']}</td>
                    <td class="{success_class}">{row['success'] * 100:.1f}%</td>
                    <td>{row['iterations']:.1f}</td>
                    <td>{row['execution_time']:.1f}</td>
                </tr>
            """

        html += """
                </table>
            </div>
        </body>
        </html>
        """

        # Save dashboard
        dashboard_path = os.path.join(self.results_dir, 'dashboard.html')
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"Dashboard created at: {dashboard_path}")


def main():
    """Main execution function"""
    # Initialize the evaluation system
    api_key = "sk-XXXXXXXXXXXXXXX"  # Replace with your actual API key
    api_base = "https://api.deepseek.com/v1"

    evaluator = RAGEvaluationSystem(api_key, api_base)

    # Run primary evaluation
    print("Starting RAG evaluation...")
    evaluator.run_primary_evaluation(runs_per_shape=10)

    # Analyze results
    print("\nAnalyzing results...")
    summary = evaluator.analyze_results()

    # Create dashboard
    print("\nCreating dashboard...")
    evaluator.create_dashboard()

    # Print summary
    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)
    for key, value in summary.items():
        print(f"{key}: {value}")

    print(f"\nResults saved to: {evaluator.results_dir}")
    print(f"Dashboard available at: {os.path.join(evaluator.results_dir, 'dashboard.html')}")


if __name__ == "__main__":
    main()
