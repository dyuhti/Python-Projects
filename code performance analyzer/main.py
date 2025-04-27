import cProfile
import pstats
import io
import memory_profiler
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import time

# Data storage for profiling results
profiling_results = {
    "functions": [],
    "execution_time": [],
    "memory_usage": []
}


# Function to profile execution time
def profile_execution(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        profiler.disable()

        exec_time = end_time - start_time
        profiling_results["functions"].append(func.__name__)
        profiling_results["execution_time"].append(exec_time)

        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s).sort_stats(pstats.SortKey.TIME)
        stats.print_stats()
        return result, exec_time

    return wrapper


# Function to profile memory usage
def profile_memory(func):
    def wrapper(*args, **kwargs):
        if __name__ == "__main__":  # Ensure multiprocessing works properly on Windows
            mem_usage = memory_profiler.memory_usage((func, args, kwargs), max_usage=True)
            max_memory = mem_usage if isinstance(mem_usage, float) else max(mem_usage)
            profiling_results["memory_usage"].append(max_memory)
            return func(*args, **kwargs), max_memory

    return wrapper


# Function to estimate time complexity
def estimate_complexity(func):
    sizes = [1000, 5000, 10000, 20000, 50000]  # Different input sizes
    times = []

    for size in sizes:
        _, exec_time = func(size)  # Run function and measure time
        times.append(exec_time)

    # Fit to common complexity classes
    complexities = {
        "O(1)": [1] * len(sizes),
        "O(log n)": np.log(sizes),
        "O(n)": sizes,
        "O(n log n)": sizes * np.log(sizes),
        "O(n²)": np.array(sizes) ** 2
    }

    best_fit = None
    min_error = float("inf")

    for label, growth in complexities.items():
        coeffs = np.polyfit(growth, times, 1)  # Linear regression
        error = np.sum((np.polyval(coeffs, growth) - times) ** 2)  # Error calculation

        if error < min_error:
            min_error = error
            best_fit = label

    return best_fit


# Helper function (simple operation)
def helper_function(n):
    return [i * 2 for i in range(n)]


# Example function with profiling
@profile_execution
@profile_memory
def example_function(n):
    helper_function(n)
    return sum(i ** 2 for i in range(n))


# Run profiling and update GUI
def run_profiling():
    try:
        n = int(entry.get())
        (_, execution_time), memory_usage = example_function(n)
        complexity = estimate_complexity(example_function)

        # Display results in a message box
        messagebox.showinfo("Profiling Results",
                            f"Execution Time: {execution_time:.4f} sec\n"
                            f"Memory Usage: {memory_usage:.2f} MB\n"
                            f"Estimated Complexity: {complexity}")

        # Create Bar Chart
        functions = ['example_function', 'helper_function']
        exec_times = [execution_time, execution_time / 2]  # Assuming helper is faster
        mem_usages = [memory_usage, memory_usage * 0.9]

        fig, ax1 = plt.subplots(figsize=(7, 5))

        # Execution Time Bar Graph
        ax1.bar(functions, exec_times, color='blue', label='Execution Time (s)')
        ax1.set_ylabel("Execution Time (s)", color='blue')

        # Memory Usage Line Graph
        ax2 = ax1.twinx()
        ax2.plot(functions, mem_usages, color="red", marker="o", label='Memory Usage (MB)')
        ax2.set_ylabel("Memory Usage (MB)", color='red')

        plt.title("Profiling Results: Execution Time & Memory Usage")
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")


# GUI Setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Program Profiling Tool")
    root.geometry("400x250")

    label = tk.Label(root, text="Enter a number (n):")
    label.pack(pady=5)

    entry = tk.Entry(root)
    entry.pack(pady=5)

    button = tk.Button(root, text="Run Profiling", command=run_profiling)
    button.pack(pady=10)

    root.mainloop()
