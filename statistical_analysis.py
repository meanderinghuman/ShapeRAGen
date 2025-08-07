# statistical_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os


class SimpleStatisticalAnalysis:
    def __init__(self, results_dir: str):
        """Initialize with results directory"""
        self.results_dir = results_dir
        self.df = pd.read_csv(os.path.join(results_dir, 'results.csv'))

    def perform_simple_analysis(self):
        """Perform simple statistical analysis that's easy to understand"""

        # 1. Basic success rates
        print("\n=== BASIC SUCCESS RATES ===")
        success_rates = self.df.groupby('condition')['success'].mean() * 100
        print(f"Success rates by condition:")
        for condition, rate in success_rates.items():
            print(f"  {condition}: {rate:.1f}%")

        # 2. Simple comparison: Does RAG help?
        print("\n=== DOES RAG HELP? ===")
        with_rag = self.df[self.df['condition'].isin(['rag_only', 'full_system'])]['success']
        without_rag = self.df[self.df['condition'].isin(['baseline', 'review_only'])]['success']

        rag_success_rate = with_rag.mean() * 100
        no_rag_success_rate = without_rag.mean() * 100
        improvement = rag_success_rate - no_rag_success_rate

        print(f"With RAG: {rag_success_rate:.1f}% success")
        print(f"Without RAG: {no_rag_success_rate:.1f}% success")
        print(f"Improvement: {improvement:.1f} percentage points")

        # 3. Simple t-test (is the difference significant?)
        t_stat, p_value = stats.ttest_ind(with_rag, without_rag)
        print(f"\nIs this difference significant? {'YES' if p_value < 0.05 else 'NO'}")
        print(f"(p-value: {p_value:.4f} - if less than 0.05, it's significant)")

        # 4. Which shape is hardest?
        print("\n=== WHICH SHAPE IS HARDEST? ===")
        shape_difficulty = self.df.groupby('shape')['success'].mean() * 100
        sorted_shapes = shape_difficulty.sort_values()

        print("Success rates by shape (from hardest to easiest):")
        for shape, rate in sorted_shapes.items():
            print(f"  {shape}: {rate:.1f}%")

        # 5. Success by shape
        print("\n=== SUCCESS RATE BY SHAPE ===")
        shape_success = self.df.groupby('shape')['success'].mean() * 100
        for shape, rate in shape_success.items():
            print(f"  {shape}: {rate:.1f}% success")

        # 6. NEW: Execution Time Analysis
        print("\n=== EXECUTION TIME ANALYSIS ===")
        time_by_condition = self.df.groupby('condition')['execution_time'].agg(['mean', 'median', 'std'])

        print("Average execution time by condition (seconds):")
        for condition, row in time_by_condition.iterrows():
            print(f"  {condition}: {row['mean']:.1f}s (median: {row['median']:.1f}s, std: {row['std']:.1f}s)")

        # 7. NEW: Time comparison for RAG vs No RAG
        print("\n=== RAG TIME IMPACT ===")
        rag_time = self.df[self.df['condition'].isin(['rag_only', 'full_system'])]['execution_time']
        no_rag_time = self.df[self.df['condition'].isin(['baseline', 'review_only'])]['execution_time']

        t_stat_time, p_value_time = stats.ttest_ind(rag_time, no_rag_time)

        print(f"Average time with RAG: {rag_time.mean():.1f} seconds")
        print(f"Average time without RAG: {no_rag_time.mean():.1f} seconds")
        print(f"Difference: {rag_time.mean() - no_rag_time.mean():.1f} seconds")
        print(f"Is time difference significant? {'YES' if p_value_time < 0.05 else 'NO'} (p-value: {p_value_time:.4f})")

        # 8. NEW: Iterations Analysis
        print("\n=== ITERATIONS ANALYSIS ===")
        # Only consider successful runs for iteration analysis
        successful_runs = self.df[self.df['success'] == True]
        iterations_by_condition = successful_runs.groupby('condition')['iterations'].agg(['mean', 'median', 'std'])

        print("Average iterations to success by condition:")
        for condition, row in iterations_by_condition.iterrows():
            print(f"  {condition}: {row['mean']:.1f} iterations (median: {row['median']:.1f}, std: {row['std']:.1f})")

        # 9. NEW: Effect Size Analysis (Cohen's d)
        print("\n=== EFFECT SIZE ANALYSIS ===")
        # Calculate Cohen's d for success rates (practical significance)
        cohens_d_success = self._calculate_cohens_d(with_rag, without_rag)

        print(f"Effect size for RAG on success rate: {cohens_d_success:.2f}")
        if abs(cohens_d_success) < 0.2:
            print("  Interpretation: Small effect")
        elif abs(cohens_d_success) < 0.5:
            print("  Interpretation: Medium effect")
        elif abs(cohens_d_success) < 0.8:
            print("  Interpretation: Large effect")
        else:
            print("  Interpretation: Very large effect")

        # Create simple visualizations including time charts
        self.create_simple_visualizations()

        # Create a simple report
        self.create_simple_report()

    def _calculate_cohens_d(self, group1, group2):
        """Calculate Cohen's d effect size"""
        mean1, mean2 = group1.mean(), group2.mean()
        n1, n2 = len(group1), len(group2)
        var1, var2 = group1.var(), group2.var()

        # Pooled standard deviation
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))

        # Cohen's d
        d = (mean1 - mean2) / pooled_std

        return d

    def create_simple_visualizations(self):
        """Create easy-to-understand visualizations"""

        # 1. Bar chart of success rates
        plt.figure(figsize=(10, 6))
        success_rates = self.df.groupby('condition')['success'].mean() * 100

        bars = plt.bar(success_rates.index, success_rates.values)
        plt.title('Success Rate by Condition', fontsize=16)
        plt.ylabel('Success Rate (%)', fontsize=14)
        plt.xlabel('Condition', fontsize=14)

        # Add percentage labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.1f}%',
                     ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'simple_success_rates.png'), dpi=300)
        plt.close()

        # 2. RAG vs No RAG comparison
        plt.figure(figsize=(8, 6))
        categories = ['Without RAG', 'With RAG']
        values = [
            self.df[self.df['condition'].isin(['baseline', 'review_only'])]['success'].mean() * 100,
            self.df[self.df['condition'].isin(['rag_only', 'full_system'])]['success'].mean() * 100
        ]

        bars = plt.bar(categories, values, color=['#ff7f0e', '#2ca02c'])
        plt.title('RAG Impact on Success Rate', fontsize=16)
        plt.ylabel('Success Rate (%)', fontsize=14)

        # Add percentage labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.1f}%',
                     ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'rag_comparison.png'), dpi=300)
        plt.close()

        # 3. Shape difficulty chart
        plt.figure(figsize=(10, 6))
        shape_success = self.df.groupby('shape')['success'].mean() * 100
        shape_success = shape_success.sort_values()

        bars = plt.barh(shape_success.index, shape_success.values, color='skyblue')
        plt.title('Success Rate by Shape', fontsize=16)
        plt.xlabel('Success Rate (%)', fontsize=14)

        # Add percentage labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height() / 2.,
                     f'{width:.1f}%',
                     ha='left', va='center')

        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'shape_difficulty.png'), dpi=300)
        plt.close()

        # 4. NEW: Execution Time by Condition
        plt.figure(figsize=(10, 6))
        time_by_condition = self.df.groupby('condition')['execution_time'].mean()

        bars = plt.bar(time_by_condition.index, time_by_condition.values, color='lightgreen')
        plt.title('Average Execution Time by Condition', fontsize=16)
        plt.ylabel('Time (seconds)', fontsize=14)
        plt.xlabel('Condition', fontsize=14)

        # Add time labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.1f}s',
                     ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'execution_time.png'), dpi=300)
        plt.close()

        # 5. NEW: Boxplot of Execution Times
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='condition', y='execution_time', data=self.df)
        plt.title('Execution Time Distribution by Condition', fontsize=16)
        plt.ylabel('Time (seconds)', fontsize=14)
        plt.xlabel('Condition', fontsize=14)
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'execution_time_boxplot.png'), dpi=300)
        plt.close()

        # 6. NEW: Iterations to Success by Condition
        plt.figure(figsize=(10, 6))
        iterations_by_condition = self.df[self.df['success'] == True].groupby('condition')['iterations'].mean()

        bars = plt.bar(iterations_by_condition.index, iterations_by_condition.values, color='lightcoral')
        plt.title('Average Iterations to Success by Condition', fontsize=16)
        plt.ylabel('Iterations', fontsize=14)
        plt.xlabel('Condition', fontsize=14)

        # Add iteration labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.1f}',
                     ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'iterations_to_success.png'), dpi=300)
        plt.close()

    def create_simple_report(self):
        """Create a simple, easy-to-understand report"""

        # Calculate key metrics
        overall_success = self.df['success'].mean() * 100
        best_condition = self.df.groupby('condition')['success'].mean().idxmax()
        best_condition_rate = self.df.groupby('condition')['success'].mean().max() * 100

        with_rag = self.df[self.df['condition'].isin(['rag_only', 'full_system'])]['success'].mean() * 100
        without_rag = self.df[self.df['condition'].isin(['baseline', 'review_only'])]['success'].mean() * 100
        rag_improvement = with_rag - without_rag

        # Time metrics
        rag_time = self.df[self.df['condition'].isin(['rag_only', 'full_system'])]['execution_time'].mean()
        no_rag_time = self.df[self.df['condition'].isin(['baseline', 'review_only'])]['execution_time'].mean()
        time_difference = rag_time - no_rag_time

        hardest_shape = self.df.groupby('shape')['success'].mean().idxmin()
        easiest_shape = self.df.groupby('shape')['success'].mean().idxmax()

        # Iteration metrics for successful runs
        successful_runs = self.df[self.df['success'] == True]
        avg_iterations = successful_runs['iterations'].mean()
        rag_iterations = successful_runs[successful_runs['condition'].isin(['rag_only', 'full_system'])][
            'iterations'].mean()
        no_rag_iterations = successful_runs[successful_runs['condition'].isin(['baseline', 'review_only'])][
            'iterations'].mean()

        # Calculate effect size
        cohens_d = self._calculate_cohens_d(
            self.df[self.df['condition'].isin(['rag_only', 'full_system'])]['success'],
            self.df[self.df['condition'].isin(['baseline', 'review_only'])]['success']
        )

        # Generate report
        report = f"""
SIMPLE EVALUATION REPORT
========================

OVERALL RESULTS
--------------
Total tests conducted: {len(self.df)}
Overall success rate: {overall_success:.1f}%

BEST PERFORMING CONDITION
------------------------
{best_condition} with {best_condition_rate:.1f}% success rate

RAG EFFECTIVENESS
----------------
Success rate WITH RAG: {with_rag:.1f}%
Success rate WITHOUT RAG: {without_rag:.1f}%
Improvement: {rag_improvement:.1f} percentage points

This means RAG increases success by {rag_improvement:.1f}%!

EXECUTION TIME
-------------
Average time WITH RAG: {rag_time:.1f} seconds
Average time WITHOUT RAG: {no_rag_time:.1f} seconds
Difference: {time_difference:.1f} seconds ({(time_difference / no_rag_time) * 100:.1f}% {'increase' if time_difference > 0 else 'decrease'})

ITERATIONS TO SUCCESS
-------------------
Average iterations overall: {avg_iterations:.1f}
Average iterations WITH RAG: {rag_iterations:.1f}
Average iterations WITHOUT RAG: {no_rag_iterations:.1f}
Difference: {rag_iterations - no_rag_iterations:.1f} iterations

SHAPE ANALYSIS
-------------
Hardest shape to generate: {hardest_shape}
Easiest shape to generate: {easiest_shape}

STATISTICAL SIGNIFICANCE
-----------------------
Is the RAG improvement statistically significant?
{'YES' if self._is_significant() else 'NO'} (p-value: {self._get_p_value():.4f})

Effect size (Cohen's d): {cohens_d:.2f} ({'small' if abs(cohens_d) < 0.2 else 'medium' if abs(cohens_d) < 0.5 else 'large' if abs(cohens_d) < 0.8 else 'very large'})
This is a measure of how meaningful the difference is in practical terms.

CONCLUSION
----------
{self._generate_conclusion()}
"""

        # Save report
        with open(os.path.join(self.results_dir, 'simple_report.txt'), 'w') as f:
            f.write(report)

        print(report)

    def _is_significant(self):
        """Check if RAG improvement is statistically significant"""
        with_rag = self.df[self.df['condition'].isin(['rag_only', 'full_system'])]['success']
        without_rag = self.df[self.df['condition'].isin(['baseline', 'review_only'])]['success']
        t_stat, p_value = stats.ttest_ind(with_rag, without_rag)
        return p_value < 0.05

    def _get_p_value(self):
        """Get p-value for RAG comparison"""
        with_rag = self.df[self.df['condition'].isin(['rag_only', 'full_system'])]['success']
        without_rag = self.df[self.df['condition'].isin(['baseline', 'review_only'])]['success']
        t_stat, p_value = stats.ttest_ind(with_rag, without_rag)
        return p_value

    def _generate_conclusion(self):
        """Generate simple conclusion"""
        with_rag = self.df[self.df['condition'].isin(['rag_only', 'full_system'])]['success'].mean() * 100
        without_rag = self.df[self.df['condition'].isin(['baseline', 'review_only'])]['success'].mean() * 100
        improvement = with_rag - without_rag

        if improvement > 20:
            return "RAG provides a substantial improvement in code generation success!"
        elif improvement > 10:
            return "RAG provides a significant improvement in code generation success."
        elif improvement > 0:
            return "RAG provides some improvement in code generation success."
        else:
            return "RAG does not appear to improve code generation success in this test."


def create_final_thesis_figures(results_dir: str):
    """Create publication-quality figures for thesis"""

    df = pd.read_csv(os.path.join(results_dir, 'results.csv'))

    # Set publication style
    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.titlesize'] = 16

    # Figure 1: Main results comparison
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    conditions_order = ['baseline', 'review_only', 'rag_only', 'full_system']
    success_rates = df.groupby('condition')['success'].mean() * 100
    success_rates = success_rates.reindex(conditions_order)

    bars = ax.bar(range(len(success_rates)), success_rates.values,
                  color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])

    ax.set_xticks(range(len(success_rates)))
    ax.set_xticklabels(['Baseline', 'Review Only', 'RAG Only', 'Full System'], rotation=0)
    ax.set_ylabel('Success Rate (%)')
    ax.set_title('Code Generation Success Rate by Condition')
    ax.set_ylim(0, 100)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 1,
                f'{height:.1f}%',
                ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'thesis_figure_1.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Figure 2: RAG impact by shape
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    shape_data = df.groupby(['shape', 'condition'])['success'].mean() * 100
    shape_data = shape_data.unstack()

    x = np.arange(len(shape_data.index))
    width = 0.2

    for i, condition in enumerate(conditions_order):
        if condition in shape_data.columns:
            ax.bar(x + i * width, shape_data[condition], width,
                   label=condition.replace('_', ' ').title())

    ax.set_xlabel('Shape Type')
    ax.set_ylabel('Success Rate (%)')
    ax.set_title('Success Rate by Shape and Condition')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(shape_data.index)
    ax.legend()
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'thesis_figure_2.png'), dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Thesis figures saved to {results_dir}")


if __name__ == "__main__":
    # Example usage
    results_dir = "evaluation_results_20240124_120000"  # Replace with actual results directory

    # Run simple analysis
    analyzer = SimpleStatisticalAnalysis(results_dir)
    analyzer.perform_simple_analysis()

    # Create thesis figures
    create_final_thesis_figures(results_dir)