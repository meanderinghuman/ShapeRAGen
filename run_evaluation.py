# run_evaluation.py

import sys
import os
from datetime import datetime
from rag_evaluation_system import RAGEvaluationSystem
from statistical_analysis import SimpleStatisticalAnalysis, create_final_thesis_figures


def main():
    """Main function to run the simplified evaluation"""

    # Configuration
    DEEPSEEK_API_KEY = "sk-XXXXXXXXXXXXXXX"  # Replace with your actual API key
    DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

    # Ask user what to run
    print("\n=== RAG Evaluation System ===")
    print("1. Run primary evaluation (DeepSeek)")
    print("2. Analyze existing results")
    print("3. Run STL analyzer")

    choice = input("\nEnter your choice (1-3): ")

    if choice == '1':
        # Run primary evaluation
        print("\n=== Starting Primary Evaluation ===")
        evaluator = RAGEvaluationSystem(DEEPSEEK_API_KEY, DEEPSEEK_API_BASE)

        # Check if context files exist
        if not all([
            os.path.exists("tri_docs_embeddings.npy"),
            os.path.exists("tri_docs_chunks.pkl"),
            os.path.exists("numpy_stl_embeddings.npy"),
            os.path.exists("numpy_stl_chunks.pkl"),
            os.path.exists("tri_custom_embeddings.npy"),
            os.path.exists("tri_custom_chunks.pkl"),
            os.path.exists("best_embeddings.npy"),
            os.path.exists("best_chunks.pkl")
        ]):
            print("\nWARNING: Some context files are missing!")
            print("Required files:")
            print("- tri_docs_embeddings.npy and tri_docs_chunks.pkl")
            print("- numpy_stl_embeddings.npy and numpy_stl_chunks.pkl")
            print("- tri_custom_embeddings.npy and tri_custom_chunks.pkl")
            print("- best_embeddings.npy and best_chunks.pkl")
            print("\nPlease ensure all embeddings and chunks files are available.")
            proceed = input("Continue anyway? (y/n): ")
            if proceed.lower() != 'y':
                return

        # Run evaluation
        evaluator.run_primary_evaluation(runs_per_shape=10)
        evaluator.analyze_results()
        evaluator.create_dashboard()

        # Run statistical analysis
        analyzer = SimpleStatisticalAnalysis(evaluator.results_dir)
        analyzer.perform_simple_analysis()

        # Create thesis figures
        create_final_thesis_figures(evaluator.results_dir)

        print("\n=== Primary Evaluation Complete ===")
        print(f"Results saved to: {evaluator.results_dir}")

    elif choice == '2':
        # Analyze existing results
        results_dir = input("Enter the results directory path: ")
        if not os.path.exists(results_dir):
            print("Directory not found!")
            return

        # Run analysis
        analyzer = SimpleStatisticalAnalysis(results_dir)
        analyzer.perform_simple_analysis()

        # Create thesis figures
        create_final_thesis_figures(results_dir)

        print("\n=== Analysis Complete ===")

    elif choice == '3':
        # Run STL analyzer
        import subprocess
        import sys

        print("\n=== Starting STL Analyzer ===")

        try:
            # Run the STL analyzer script
            subprocess.run([sys.executable, "stl_analyzer.py"])
        except Exception as e:
            print(f"Error running STL analyzer: {e}")

    else:
        print("Invalid choice!")

    print("\nEvaluation System Exited")


if __name__ == "__main__":
    main()