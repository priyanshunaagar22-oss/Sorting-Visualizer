# Sorting-Visualizer
Dynamic Sorting Algorithm Visualizer built with Python and Matplotlib. Explore Bubble, Insertion, Merge, and Quick Sort step-by-step with interactive controls for size and speed.

# 🔄 Dynamic Sorting Algorithm Visualizer

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Matplotlib](https://img.shields.io/badge/Library-Matplotlib-orange.svg)](https://matplotlib.org/)
[![License](https://img.shields.io/github/license/YOUR_USERNAME/YOUR_REPO_NAME)](LICENSE)

---

## 💡 Project Overview

This is an interactive, educational tool that visually demonstrates the execution flow of core sorting algorithms. Built entirely in Python using the Matplotlib library for its graphical interface, the application breaks down complex logic (like comparison and swapping) into clear, frame-by-frame animations using **Python Generators**.

The visualizer includes dynamic information panels that display the **Time Complexity**, **Space Complexity**, and **Stability** of the selected algorithm, making it an excellent resource for learning Data Structures and Algorithms (DSA).

## ✨ Features

* **Algorithms Covered:** Bubble Sort, Insertion Sort, Merge Sort, and Quick Sort.
* **Interactive Controls:** Sliders to adjust the input array **Size** (up to 50 elements) and animation **Speed** (interval in ms).
* **Visual State Tracking:** Clear color-coding to highlight the status of elements:
    * <span style="color:#f59e0b">**Amber:** Comparing</span>
    * <span style="color:#ef4444">**Red:** Swapping / Placement</span>
    * <span style="color:#10b981">**Green:** Sorted / Finalized</span>
* **Dynamic Info Panel:** Displays algorithmic complexity and a step-by-step description of the chosen method.

## 🚀 Installation and Setup

### Prerequisites

You must have Python (3.x) installed on your system.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```

2.  **Install Dependencies:**
    The project requires **Matplotlib** and **NumPy** (which is a Matplotlib dependency).
    ```bash
    pip install matplotlib numpy
    ```

## ▶️ Usage

To run the visualizer, execute the Python file from your terminal:

```bash
python sorting-visualizer-python.py
