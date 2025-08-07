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


##############################################
# Part A: Context Retrieval & Embedding Setup #
##############################################

def is_valid_link(link, domain):
    return link.startswith(domain) and '#' not in link


def crawl_page(url, domain, visited, recursive=True):
    if url in visited:
        return ""
    print("Crawling:", url)
    visited.add(url)
    page_text = ""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print("Failed to fetch:", url, e)
        return ""
    soup = BeautifulSoup(response.text, "html.parser")
    page_text += soup.get_text(separator="\n", strip=True) + "\n\n"

    if recursive:
        # Follow internal links only if recursion is enabled.
        for a_tag in soup.find_all('a', href=True):
            link = urllib.parse.urljoin(url, a_tag['href'])
            if is_valid_link(link, domain) and link not in visited:
                time.sleep(0.5)
                page_text += crawl_page(link, domain, visited, recursive=recursive)
    return page_text


def crawl_site(start_url, domain, recursive=True):
    visited = set()
    full_text = crawl_page(start_url, domain, visited, recursive=recursive)
    chunks = [chunk.strip() for chunk in full_text.split("\n\n") if chunk.strip()]
    return chunks


def load_or_create_context(context_name, source_type, source, emb_file, chunks_file, recursive=True):
    """
    Depending on source_type:
      - "crawl": 'source' is either a URL (if single) or a list of URLs to crawl.
      - "file": 'source' is a local text file.
    The parameter 'recursive' determines if the crawler follows internal links.
    """
    if os.path.exists(emb_file) and os.path.exists(chunks_file):
        print(f"Loading precomputed embeddings for {context_name}...")
        embeddings = np.load(emb_file)
        with open(chunks_file, "rb") as f:
            chunks = pickle.load(f)
        return chunks, embeddings

    print(f"Creating context for {context_name}...")
    if source_type == "crawl":
        if isinstance(source, list):
            all_chunks = []
            for url in source:
                domain = urllib.parse.urlparse(url).scheme + "://" + urllib.parse.urlparse(url).netloc
                # For custom links, you might disable recursion.
                chunks_from_url = crawl_site(url, domain, recursive=recursive)
                all_chunks.extend(chunks_from_url)
            chunks = all_chunks
        else:
            domain = source  # assume source is a URL
            chunks = crawl_site(source, domain, recursive=recursive)
    elif source_type == "file":
        with open(source, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    else:
        chunks = []

    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = embedder.encode(chunks)
    np.save(emb_file, embeddings)
    with open(chunks_file, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Saved embeddings for {context_name} to {emb_file} and {chunks_file}.")
    return chunks, embeddings


def build_faiss_index(embeddings):
    embeddings = np.array(embeddings, dtype=np.float32)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


def retrieve_context(query, chunks, embeddings, embedder, k=3):
    index = build_faiss_index(embeddings)
    query_emb = embedder.encode([query])
    query_emb = np.array(query_emb, dtype=np.float32)
    distances, indices = index.search(query_emb, k)
    retrieved = [chunks[idx] for idx in indices[0]]
    return "\n\n".join(retrieved)


def trimesh_crawler_and_embeddings():
    start_url = "https://trimesh.org/"
    domain = "https://trimesh.org"
    emb_file = "tri_docs_embeddings.npy"
    chunks_file = "tri_docs_chunks.pkl"

    return load_or_create_context("Trimesh Docs", "crawl", start_url, emb_file, chunks_file)


def numpy_stl_crawler_and_embeddings():
    start_url = "https://numpy-stl.readthedocs.io/en/latest/usage.html"
    domain = "https://numpy-stl.readthedocs.io"
    emb_file = "numpy_stl_embeddings.npy"
    chunks_file = "numpy_stl_chunks.pkl"

    return load_or_create_context("NumPy-STL Docs", "crawl", start_url, emb_file, chunks_file)


##############################################
# Part B: Iterative Code Generation Pipeline  #
##############################################

def generate_code(prompt, extra_context=""):
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
    code = response.choices[0].message.content.strip()
    return code


def extract_code_from_markdown(text):
    """
    Extracts Python code from Markdown code blocks.

    Parameters:
        text (str): Text containing Markdown code blocks

    Returns:
        str: Extracted Python code or empty string if no code found
    """
    # Pattern to match Python code blocks with ```python or ``` python
    pattern = r'```(?:python)?\s*([\s\S]*?)```'
    matches = re.findall(pattern, text)

    if not matches:
        print("No code blocks found in the response.")
        return ""

    # If multiple code blocks, combine them
    combined_code = "\n\n".join(match.strip() for match in matches)
    return combined_code


def test_code(code):
    # Write the code to a temporary file with UTF-8 encoding.
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py", encoding="utf-8") as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    try:
        # Set environment variable to force Python to use UTF-8 mode.
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        result = subprocess.run(
            ["python", temp_file_path],
            capture_output=True,
            text=True,
            timeout=20,
            env=env  # Pass the modified environment to the subprocess.
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
    except subprocess.TimeoutExpired:
        stdout = ""
        stderr = "Execution timed out."
    finally:
        os.remove(temp_file_path)
    return stdout, stderr


def review_code(existing_code, context):
    """
    Sends the existing code along with the available context to the model for review.
    It asks the model to refine the code if necessary.
    """
    review_prompt = (
            "Please review the following Python code based on the provided documentation and best practices for 3D printing. "
            "If improvements are needed, return an updated version of the code; otherwise, return the code as is.\n\n"
            "Wrap your final code inside ```python and ``` markdown code blocks. "
            "The code block should only contain valid, executable Python code. "
            "All explanations should be outside the code block.\n\n"
            "Code:\n" + existing_code + "\n\nContext:\n" + context
    )
    messages = [
        {"role": "system", "content": (
            "You are a helpful assistant that reviews and refines Python code for creating 3D printing models using 'trimesh' and/or 'numpy-stl'. "
            "Your review should consider best practices and documentation guidelines, and if the code can be improved, return an updated version. "
            "If no improvements are needed, return the code as is. "
            "Ensure the mesh is suitable for FDM printing with emphasis on minimum wall thickness and supports where needed. "
            "Take note of contact points between the shape and its support(s). "
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
    reviewed_code = response.choices[0].message.content.strip()
    return reviewed_code


##############################################
# Part C: Main Pipeline Integration         #
##############################################

def run_single_iteration(prompt, combined_context, iteration_number, max_iterations=5):
    """
    Runs a single iteration of the code generation pipeline.

    Returns:
        tuple: (final_code, success) where success is a boolean indicating if code executed successfully
    """
    print(f"\n========== Running iteration #{iteration_number} ==========")

    extra_context = combined_context
    final_code = None
    last_generated_code = None  # Track the last generated code even if it had errors

    for i in range(max_iterations):
        print(f"\n--- Iteration {iteration_number}-{i + 1} ---")

        # Generate code and extract only the Python code from markdown blocks
        generated_response = generate_code(prompt, extra_context)
        print("Full Model Response:")
        print(generated_response)

        # Extract only the code from markdown blocks
        code = extract_code_from_markdown(generated_response)
        if not code:
            print("No valid code block found. Retrying with more explicit instructions...")
            extra_context += "\n\nIMPORTANT: Please provide the code wrapped in ```python and ``` markdown tags."
            continue

        # Store the last generated code even if it has errors
        last_generated_code = code

        print("\nExtracted Code:")
        print(code)

        stdout, stderr = test_code(code)
        print("\nExecution Output:")
        print(stdout)
        if stderr:
            print("\nExecution Error:")
            print(stderr)

        if stderr:
            print("\nCode execution produced an error.")
            extra_context = combined_context + "\n\nError Details:\n" + stderr + "\nPlease revise the code accordingly. Make sure to wrap your code in ```python and ``` markdown blocks."
            if os.path.exists("output.stl"):
                os.remove("output.stl")
            time.sleep(1)
        else:
            print("\nCode executed successfully. Proceeding to code review step...")
            # Even if the code ran without error, ask the model to review and refine the code.
            reviewed_response = review_code(code, combined_context)
            print("\nFull Review Response:")
            print(reviewed_response)

            # Extract only the code from markdown blocks in the review response
            reviewed_code = extract_code_from_markdown(reviewed_response)
            if not reviewed_code:
                print("No valid code block found in the review. Using previously generated code.")
                final_code = code
                break

            print("\nExtracted Reviewed Code:")
            print(reviewed_code)

            # Optionally, test the reviewed code once more.
            stdout_review, stderr_review = test_code(reviewed_code)
            if stderr_review:
                print("\nReviewed code execution produced an error:")
                print(stderr_review)
                extra_context = combined_context + "\n\nError Details from reviewed code:\n" + stderr_review + "\nPlease revise the code accordingly. Make sure to wrap your code in ```python and ``` markdown blocks."
                if os.path.exists("output.stl"):
                    os.remove("output.stl")
                time.sleep(1)
            else:
                final_code = reviewed_code
                break

    # After all iterations, check if we have a successful code
    if final_code is None:
        print(f"Maximum iterations ({max_iterations}) reached without successful code execution.")

        # Make a one-time attempt to fix the last generated code
        if last_generated_code:
            print("Making one final attempt to fix the last generated code...")
            fix_prompt = (
                f"The following code has errors. Please fix it:\n\n{last_generated_code}\n\n"
                "Make sure to wrap your code in ```python and ``` markdown blocks."
            )
            try:
                fix_response = generate_code(fix_prompt, combined_context)
                fixed_code = extract_code_from_markdown(fix_response)
                if fixed_code:
                    stdout_fixed, stderr_fixed = test_code(fixed_code)
                    if not stderr_fixed:
                        final_code = fixed_code
                        print("Final attempt succeeded!")
                    else:
                        print("Final attempt failed with errors.")
            except Exception as e:
                print(f"Error during final fix attempt: {e}")

        # If we still don't have working code
        if final_code is None:
            print("All attempts to generate working code have failed.")
            return last_generated_code, False

    return final_code, True


def main(prompt="Create a box with base sides 14mm and 20mm with height 30mm", n_runs=1):
    """
    Main function to run the pipeline multiple times.

    Args:
        prompt (str): The prompt to use for generating 3D models
        n_runs (int): Number of times to run the pipeline
    """
    # Load all contexts once at the beginning
    print("Loading contexts...")

    # Load trimesh documentation context.
    tri_docs_chunks, tri_docs_embeddings = trimesh_crawler_and_embeddings()

    # Load numpy-stl documentation context
    numpy_stl_chunks, numpy_stl_embeddings = numpy_stl_crawler_and_embeddings()

    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # Get custom trimesh functions contexts:
    # 1. Custom Trimesh Functions Context
    CUSTOM_URLS = [
        "https://github.com/mikedh/trimesh/issues/2285",
        "https://github.com/mikedh/trimesh/issues/1899"
    ]
    tri_custom_chunks, tri_custom_embeddings = load_or_create_context(
        "Custom Trimesh Functions",
        "crawl",
        CUSTOM_URLS,
        "tri_custom_embeddings.npy",
        "tri_custom_chunks.pkl",
        recursive=False  # Disable recursion so that only these specific pages are fetched.
    )

    # 2. 3D Printing Best Practices Context from a local file.
    best_practices_file = "best_practices.txt"  # Ensure this file exists.
    best_chunks, best_embeddings = load_or_create_context(
        "3D Printing Best Practices",
        "file",
        best_practices_file,
        "best_embeddings.npy",
        "best_chunks.pkl"
    )

    # Retrieve context from each source.
    tri_docs_context = retrieve_context(prompt, tri_docs_chunks, tri_docs_embeddings, embedder, k=3)
    numpy_stl_context = retrieve_context(prompt, numpy_stl_chunks, numpy_stl_embeddings, embedder, k=3)
    tri_custom_context = retrieve_context(prompt, tri_custom_chunks, tri_custom_embeddings, embedder, k=3)
    best_context = retrieve_context(prompt, best_chunks, best_embeddings, embedder, k=3)

    combined_context = (
            "Trimesh Documentation context:\n" + tri_docs_context +
            "\n\nNumPy-STL Documentation context:\n" + numpy_stl_context +
            "\n\nCustom Trimesh Functions context:\n" + tri_custom_context +
            "\n\n3D Printing Best Practices context:\n" + best_context
    )

    # Run the pipeline n times
    for i in range(1, n_runs + 1):
        print(f"\n\n############################################################")
        print(f"#                    RUN {i} OF {n_runs}                      #")
        print(f"############################################################\n")

        final_code, success = run_single_iteration(prompt, combined_context, i)

        # Save the final code if we have it
        if final_code:
            code_filename = f"final_code_{i}.py"
            with open(code_filename, "w", encoding="utf-8") as f:
                f.write(final_code)
            print(f"\nFinal code saved to '{code_filename}'.")

            if os.path.exists("output.stl"):
                stl_filename = f"final_output_{i}.stl"
                shutil.move("output.stl", stl_filename)
                print(f"Final STL file saved as '{stl_filename}'.")
            else:
                print(f"No STL file found for run {i}.")
        else:
            print(f"No code was saved for run {i}.")

        # Clean up any temporary files between iterations
        if os.path.exists("output.stl"):
            os.remove("output.stl")

        # Add a small delay between runs to avoid hitting API rate limits
        if i < n_runs:
            time.sleep(2)

    print(f"\n\nCompleted all {n_runs} runs.")


if __name__ == "__main__":
    openai.api_key = "sk-XXXXXXXXXXXXXXX"  # Replace with your actual API key
    openai.api_base = "https://api.deepseek.com/v1"  # Deepseek model

    # Usage - run the pipeline n-times with a specific prompt
    prompt1 = "Create cylinder with diameter 25mm, height 40mm"
    prompt2 = "Create a box with base sides 20mm and 30mm, height 40mm"
    prompt3 = "Create a cone with base radius 20mm, height 35mm"
    prompt4 = "Create a pyramid with base 25mm x 25mm, height 30mm"
    prompt5 = "Create a sphere with radius 45mm"
    n_runs = 10

    main(prompt=prompt5, n_runs=n_runs)
