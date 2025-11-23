import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button, Slider, RadioButtons
import numpy as np
import random

# Algorithm definitions
algorithms = {
    'Bubble Sort': {
        'time': 'O(n²)',
        'space': 'O(1)',
        'best': 'O(n)',
        'stable': 'Yes',
        'description': '''Bubble Sort is the simplest sorting algorithm. It works by repeatedly 
stepping through the list, comparing adjacent elements and swapping them 
if they are in the wrong order. The pass through the list is repeated 
until no swaps are needed, which indicates that the list is sorted.''',
        'how_it_works': [
            '1. Compare adjacent elements from left to right',
            '2. If the left element is greater, swap them',
            '3. Move to the next pair and repeat',
            '4. After each pass, largest element "bubbles up"',
            '5. Repeat until no swaps are needed'
        ]
    },
    'Insertion Sort': {
        'time': 'O(n²)',
        'space': 'O(1)',
        'best': 'O(n)',
        'stable': 'Yes',
        'description': '''Insertion Sort builds the final sorted array one item at a time. 
It is much like sorting playing cards in your hands - you pick up one 
card at a time and insert it into its correct position among the 
already-sorted cards.''',
        'how_it_works': [
            '1. Start from second element (first is sorted)',
            '2. Compare current with sorted portion',
            '3. Shift larger elements one position right',
            '4. Insert current element in correct position',
            '5. Move to next element and repeat'
        ]
    },
    'Merge Sort': {
        'time': 'O(n log n)',
        'space': 'O(n)',
        'best': 'O(n log n)',
        'stable': 'Yes',
        'description': '''Merge Sort is a divide-and-conquer algorithm. It divides the input 
array into two halves, recursively sorts them, and then merges the two 
sorted halves. It guarantees O(n log n) time complexity in all cases, 
making it efficient for large datasets.''',
        'how_it_works': [
            '1. Divide the array into two halves',
            '2. Recursively sort each half',
            '3. Merge two sorted halves by comparing',
            '4. Place the smaller element first',
            '5. Continue until all elements are merged'
        ]
    },
    'Quick Sort': {
        'time': 'O(n log n)',
        'space': 'O(log n)',
        'best': 'O(n log n)',
        'stable': 'No',
        'description': '''Quick Sort is a highly efficient divide-and-conquer algorithm. 
It works by selecting a "pivot" element and partitioning the array so 
that elements smaller than the pivot go to the left and larger elements 
go to the right. This process is recursively applied to the sub-arrays.''',
        'how_it_works': [
            '1. Choose a pivot element (usually last)',
            '2. Partition: smaller left, larger right',
            '3. Pivot is now in final sorted position',
            '4. Recursively apply to sub-arrays',
            '5. Base case: size 0 or 1 already sorted'
        ]
    }
}

class SortingVisualizer:
    def __init__(self):
        self.size = 25
        self.speed = 100  # milliseconds delay
        self.array = []
        self.colors = []
        self.sorting = False
        self.current_algorithm = 'Bubble Sort'
        self.current_step = ''
        self.generator = None
        
        # Colors
        self.COLOR_UNSORTED = '#6366f1'   # Indigo
        self.COLOR_COMPARING = '#f59e0b'  # Amber
        self.COLOR_SWAPPING = '#ef4444'   # Red
        self.COLOR_SORTED = '#10b981'     # Green
        self.COLOR_BG = '#1f2937'         # Dark gray
        self.COLOR_PANEL = '#374151'      # Lighter gray
        
        self.setup_gui()
        self.generate_array()
        
    def setup_gui(self):
        # Create figure with dark background
        self.fig = plt.figure(figsize=(14, 9), facecolor=self.COLOR_BG)
        self.fig.canvas.manager.set_window_title('🔄 Sorting Visualizer')
        
        # Main bar chart area
        self.ax_bars = self.fig.add_axes([0.05, 0.35, 0.6, 0.55], facecolor=self.COLOR_PANEL)
        self.ax_bars.set_xticks([])
        self.ax_bars.set_yticks([])
        for spine in self.ax_bars.spines.values():
            spine.set_color(self.COLOR_PANEL)
        
        # Current step display
        self.ax_step = self.fig.add_axes([0.05, 0.28, 0.6, 0.05], facecolor=self.COLOR_PANEL)
        self.ax_step.set_xticks([])
        self.ax_step.set_yticks([])
        for spine in self.ax_step.spines.values():
            spine.set_visible(False)
        self.step_text = self.ax_step.text(0.5, 0.5, '', ha='center', va='center',
                                            fontsize=10, color='#fde047', 
                                            transform=self.ax_step.transAxes)
        
        # Title
        self.fig.text(0.35, 0.94, '🔄 Sorting Visualizer', ha='center', va='center',
                      fontsize=20, fontweight='bold', color='#818cf8')
        
        # Legend
        legend_y = 0.22
        legend_items = [
            (self.COLOR_UNSORTED, 'Unsorted'),
            (self.COLOR_COMPARING, 'Comparing'),
            (self.COLOR_SWAPPING, 'Swapping'),
            (self.COLOR_SORTED, 'Sorted')
        ]
        for i, (color, label) in enumerate(legend_items):
            x_pos = 0.12 + i * 0.15
            self.fig.patches.append(plt.Rectangle((x_pos, legend_y), 0.02, 0.02,
                                    facecolor=color, transform=self.fig.transFigure))
            self.fig.text(x_pos + 0.03, legend_y + 0.01, label, fontsize=9, 
                         color='white', va='center')
        
        # Algorithm info panel (right side)
        self.ax_info = self.fig.add_axes([0.68, 0.28, 0.3, 0.62], facecolor=self.COLOR_PANEL)
        self.ax_info.set_xticks([])
        self.ax_info.set_yticks([])
        for spine in self.ax_info.spines.values():
            spine.set_color('#4b5563')
        self.update_info_panel()
        
        # Controls area
        # Algorithm selector
        self.ax_radio = self.fig.add_axes([0.05, 0.02, 0.15, 0.15], facecolor=self.COLOR_PANEL)
        self.radio = RadioButtons(self.ax_radio, list(algorithms.keys()), 
                                   active=0, activecolor='#818cf8')
        for label in self.radio.labels:
            label.set_color('white')
            label.set_fontsize(8)
        self.radio.on_clicked(self.on_algorithm_change)
        
        # Size slider
        self.ax_size = self.fig.add_axes([0.28, 0.12, 0.15, 0.03], facecolor=self.COLOR_PANEL)
        self.slider_size = Slider(self.ax_size, 'Size', 8, 50, valinit=self.size, 
                                   valstep=1, color='#818cf8')
        self.slider_size.label.set_color('white')
        self.slider_size.valtext.set_color('white')
        self.slider_size.on_changed(self.on_size_change)
        
        # Speed slider
        self.ax_speed = self.fig.add_axes([0.28, 0.05, 0.15, 0.03], facecolor=self.COLOR_PANEL)
        self.slider_speed = Slider(self.ax_speed, 'Speed', 10, 500, valinit=self.speed,
                                    valstep=10, color='#818cf8')
        self.slider_speed.label.set_color('white')
        self.slider_speed.valtext.set_color('white')
        self.slider_speed.on_changed(self.on_speed_change)
        
        # Buttons
        self.ax_new = self.fig.add_axes([0.5, 0.08, 0.1, 0.05])
        self.btn_new = Button(self.ax_new, 'New Array', color=self.COLOR_PANEL, hovercolor='#4b5563')
        self.btn_new.label.set_color('white')
        self.btn_new.on_clicked(self.on_new_array)
        
        self.ax_start = self.fig.add_axes([0.62, 0.08, 0.1, 0.05])
        self.btn_start = Button(self.ax_start, 'Start', color='#4f46e5', hovercolor='#6366f1')
        self.btn_start.label.set_color('white')
        self.btn_start.on_clicked(self.on_start)
        
        self.ax_stop = self.fig.add_axes([0.74, 0.08, 0.1, 0.05])
        self.btn_stop = Button(self.ax_stop, 'Stop', color='#dc2626', hovercolor='#ef4444')
        self.btn_stop.label.set_color('white')
        self.btn_stop.on_clicked(self.on_stop)
        
    def update_info_panel(self):
        self.ax_info.clear()
        self.ax_info.set_xticks([])
        self.ax_info.set_yticks([])
        self.ax_info.set_facecolor(self.COLOR_PANEL)
        
        info = algorithms[self.current_algorithm]
        
        # Algorithm name
        self.ax_info.text(0.5, 0.95, self.current_algorithm, ha='center', va='top',
                          fontsize=14, fontweight='bold', color='#818cf8',
                          transform=self.ax_info.transAxes)
        
        # Description
        self.ax_info.text(0.05, 0.85, info['description'], ha='left', va='top',
                          fontsize=7, color='#d1d5db', wrap=True,
                          transform=self.ax_info.transAxes)
        
        # How it works
        self.ax_info.text(0.05, 0.58, 'How it works:', ha='left', va='top',
                          fontsize=9, fontweight='bold', color='#fbbf24',
                          transform=self.ax_info.transAxes)
        
        steps_text = '\n'.join(info['how_it_works'])
        self.ax_info.text(0.05, 0.52, steps_text, ha='left', va='top',
                          fontsize=7, color='#9ca3af',
                          transform=self.ax_info.transAxes)
        
        # Complexity boxes
        complexities = [
            ('Best', info['best'], '#10b981'),
            ('Avg/Worst', info['time'], '#f59e0b'),
            ('Space', info['space'], '#818cf8'),
            ('Stable', info['stable'], '#10b981' if info['stable'] == 'Yes' else '#ef4444')
        ]
        
        box_width = 0.22
        start_x = 0.05
        for i, (label, value, color) in enumerate(complexities):
            x = start_x + i * (box_width + 0.02)
            # Box background
            rect = plt.Rectangle((x, 0.02), box_width, 0.12,
                                   facecolor='#1f2937', transform=self.ax_info.transAxes,
                                   clip_on=False)
            self.ax_info.add_patch(rect)
            # Label
            self.ax_info.text(x + box_width/2, 0.11, label, ha='center', va='center',
                              fontsize=6, color='#9ca3af', transform=self.ax_info.transAxes)
            # Value
            self.ax_info.text(x + box_width/2, 0.05, value, ha='center', va='center',
                              fontsize=10, fontweight='bold', color=color,
                              family='monospace', transform=self.ax_info.transAxes)
        
        self.fig.canvas.draw_idle()
        
    def generate_array(self):
        self.array = [random.randint(10, 100) for _ in range(self.size)]
        self.colors = [self.COLOR_UNSORTED] * self.size
        self.update_bars()
        self.step_text.set_text('')
        
    def update_bars(self):
        self.ax_bars.clear()
        self.ax_bars.set_xticks([])
        self.ax_bars.set_yticks([])
        self.ax_bars.set_facecolor(self.COLOR_PANEL)
        self.ax_bars.set_ylim(0, 110)
        
        x = np.arange(len(self.array))
        self.ax_bars.bar(x, self.array, color=self.colors, width=0.8)
        self.fig.canvas.draw_idle()
        
    def set_step(self, text):
        self.step_text.set_text(text)
        
    # Sorting Algorithms as Generators
    def bubble_sort(self):
        arr = self.array
        n = len(arr)
        for i in range(n - 1):
            for j in range(n - i - 1):
                self.colors = [self.COLOR_UNSORTED] * n
                for k in range(n - i, n):
                    self.colors[k] = self.COLOR_SORTED
                self.colors[j] = self.COLOR_COMPARING
                self.colors[j + 1] = self.COLOR_COMPARING
                self.set_step(f'Comparing elements at index {j} and {j + 1}')
                yield
                
                if arr[j] > arr[j + 1]:
                    self.colors[j] = self.COLOR_SWAPPING
                    self.colors[j + 1] = self.COLOR_SWAPPING
                    self.set_step(f'Swapping {arr[j]} and {arr[j + 1]}')
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    yield
                    
            self.colors[n - 1 - i] = self.COLOR_SORTED
            
        self.colors = [self.COLOR_SORTED] * n
        self.set_step('Sorting complete!')
        yield
        
    def insertion_sort(self):
        arr = self.array
        n = len(arr)
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            
            self.colors = [self.COLOR_SORTED if x < i else self.COLOR_UNSORTED for x in range(n)]
            self.colors[i] = self.COLOR_COMPARING
            self.set_step(f'Picking element {key} to insert into sorted portion')
            yield
            
            while j >= 0 and arr[j] > key:
                self.colors[j] = self.COLOR_SWAPPING
                self.colors[j + 1] = self.COLOR_SWAPPING
                self.set_step(f'Shifting {arr[j]} to the right')
                arr[j + 1] = arr[j]
                yield
                j -= 1
                
            arr[j + 1] = key
            self.colors = [self.COLOR_SORTED if x <= i else self.COLOR_UNSORTED for x in range(n)]
            self.set_step(f'Inserting {key} at position {j + 1}')
            yield
            
        self.colors = [self.COLOR_SORTED] * n
        self.set_step('Sorting complete!')
        yield
        
    def merge_sort(self):
        arr = self.array
        n = len(arr)
        
        def merge(l, m, r):
            left = arr[l:m + 1]
            right = arr[m + 1:r + 1]
            i = j = 0
            k = l
            
            self.set_step(f'Merging subarrays [{l}..{m}] and [{m + 1}..{r}]')
            
            while i < len(left) and j < len(right):
                self.colors = [self.COLOR_UNSORTED] * n
                self.colors[l + i] = self.COLOR_COMPARING
                self.colors[m + 1 + j] = self.COLOR_COMPARING
                self.set_step(f'Comparing {left[i]} and {right[j]}')
                yield True
                
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                    
                self.colors[k] = self.COLOR_SWAPPING
                yield True
                k += 1
                
            while i < len(left):
                arr[k] = left[i]
                self.colors[k] = self.COLOR_SWAPPING
                yield True
                i += 1
                k += 1
                
            while j < len(right):
                arr[k] = right[j]
                self.colors[k] = self.COLOR_SWAPPING
                yield True
                j += 1
                k += 1
                
        def sort(l, r):
            if l < r:
                m = (l + r) // 2
                self.set_step(f'Dividing array at index {m}')
                yield True
                yield from sort(l, m)
                yield from sort(m + 1, r)
                yield from merge(l, m, r)
                
        yield from sort(0, n - 1)
        self.colors = [self.COLOR_SORTED] * n
        self.set_step('Sorting complete!')
        yield True
        
    def quick_sort(self):
        arr = self.array
        n = len(arr)
        sorted_indices = set()
        
        def partition(low, high):
            pivot = arr[high]
            self.set_step(f'Choosing pivot: {pivot} at index {high}')
            yield True
            
            i = low - 1
            for j in range(low, high):
                self.colors = [self.COLOR_UNSORTED] * n
                for idx in sorted_indices:
                    self.colors[idx] = self.COLOR_SORTED
                self.colors[j] = self.COLOR_COMPARING
                self.colors[high] = self.COLOR_COMPARING
                self.set_step(f'Comparing {arr[j]} with pivot {pivot}')
                yield True
                
                if arr[j] < pivot:
                    i += 1
                    if i != j:
                        self.colors[i] = self.COLOR_SWAPPING
                        self.colors[j] = self.COLOR_SWAPPING
                        self.set_step(f'Swapping {arr[i]} and {arr[j]}')
                        arr[i], arr[j] = arr[j], arr[i]
                        yield True
                        
            self.colors[i + 1] = self.COLOR_SWAPPING
            self.colors[high] = self.COLOR_SWAPPING
            self.set_step(f'Placing pivot {pivot} in correct position')
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            yield True
            return i + 1
            
        def sort(low, high):
            if low < high:
                pi_gen = partition(low, high)
                pi = None
                for val in pi_gen:
                    if isinstance(val, int):
                        pi = val
                    else:
                        yield val
                pi = low
                for val in partition(low, high):
                    if isinstance(val, int):
                        pi = val
                        break
                    yield val
                # Re-run partition to get pi correctly
                i = low - 1
                for j in range(low, high):
                    if arr[j] < arr[high]:
                        i += 1
                # Actually, let's simplify
                
        # Simplified iterative approach for generator
        stack = [(0, n - 1)]
        while stack:
            low, high = stack.pop()
            if low < high:
                pivot = arr[high]
                self.set_step(f'Choosing pivot: {pivot} at index {high}')
                self.colors = [self.COLOR_UNSORTED] * n
                for idx in sorted_indices:
                    self.colors[idx] = self.COLOR_SORTED
                yield True
                
                i = low - 1
                for j in range(low, high):
                    self.colors = [self.COLOR_UNSORTED] * n
                    for idx in sorted_indices:
                        self.colors[idx] = self.COLOR_SORTED
                    self.colors[j] = self.COLOR_COMPARING
                    self.colors[high] = self.COLOR_COMPARING
                    self.set_step(f'Comparing {arr[j]} with pivot {pivot}')
                    yield True
                    
                    if arr[j] < pivot:
                        i += 1
                        if i != j:
                            self.colors[i] = self.COLOR_SWAPPING
                            self.colors[j] = self.COLOR_SWAPPING
                            self.set_step(f'Swapping {arr[i]} and {arr[j]}')
                            arr[i], arr[j] = arr[j], arr[i]
                            yield True
                            
                pi = i + 1
                self.colors[pi] = self.COLOR_SWAPPING
                self.colors[high] = self.COLOR_SWAPPING
                self.set_step(f'Placing pivot in correct position')
                arr[pi], arr[high] = arr[high], arr[pi]
                yield True
                
                sorted_indices.add(pi)
                stack.append((pi + 1, high))
                stack.append((low, pi - 1))
                
        self.colors = [self.COLOR_SORTED] * n
        self.set_step('Sorting complete!')
        yield True
        
    # Event handlers
    def on_algorithm_change(self, label):
        self.current_algorithm = label
        self.update_info_panel()
        if not self.sorting:
            self.generate_array()
            
    def on_size_change(self, val):
        if not self.sorting:
            self.size = int(val)
            self.generate_array()
            
    def on_speed_change(self, val):
        self.speed = int(val)
        
    def on_new_array(self, event):
        if not self.sorting:
            self.generate_array()
            
    def on_start(self, event):
        if not self.sorting:
            self.sorting = True
            if self.current_algorithm == 'Bubble Sort':
                self.generator = self.bubble_sort()
            elif self.current_algorithm == 'Insertion Sort':
                self.generator = self.insertion_sort()
            elif self.current_algorithm == 'Merge Sort':
                self.generator = self.merge_sort()
            elif self.current_algorithm == 'Quick Sort':
                self.generator = self.quick_sort()
            self.anim = animation.FuncAnimation(
                self.fig, self.animate, interval=self.speed,
                repeat=False, cache_frame_data=False
            )
            self.fig.canvas.draw_idle()
            
    def on_stop(self, event):
        self.sorting = False
        if hasattr(self, 'anim'):
            self.anim.event_source.stop()
        self.set_step('Stopped')
        self.fig.canvas.draw_idle()
        
    def animate(self, frame):
        if not self.sorting:
            return
        try:
            next(self.generator)
            self.update_bars()
        except StopIteration:
            self.sorting = False
            self.update_bars()
            
    def run(self):
        plt.show()


if __name__ == '__main__':
    visualizer = SortingVisualizer()
    visualizer.run()
