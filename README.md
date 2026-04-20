# Content-Aware Image Resizing

> CS311: Algorithms Design and Analysis — King Saud University  
> College of Computer and Information Sciences, Computer Science Department

## Overview

Content-aware image resizing is a sophisticated technique that allows for the dynamic scaling of images. Unlike standard resizing methods, which simply distort images, this technique preserves important visual content while intelligently changing the size of the image using **seam carving** — the removal of low-energy pixel paths that traverse the image from top to bottom.

The project implements and compares **three algorithmic approaches** to seam carving: Brute Force, Dynamic Programming, and Greedy.

---

## How It Works

1. **Energy Map Calculation**: Each pixel is assigned an energy value representing its visual importance (e.g., via gradient magnitude).
2. **Seam Finding**: A connected path of pixels (one per row) with minimum total energy is identified — this is the "seam."
3. **Seam Removal**: The identified seam is removed, reducing the image width by 1. This is repeated `k` times to achieve the desired reduction.

---

## Algorithms

### 1. Brute Force

Recursively explores all possible seam paths by branching left, center, and right at each row.

- **Time Complexity**: `O(k × 3^H)` — exponential in image height
- **Space Complexity**: `O(H)` — call stack depth
- **Characteristics**: Guaranteed to find the optimal seam, but extremely slow. Only practical on very small images (e.g., 8×8). Tested using Google Colab due to resource constraints.

**Pseudocode — `findBestSeam()`:**
```
Function findBestSeam(grid):
    minCost = ∞
    opPath = []
    For each column i from 0 to width-1:
        Call findBestSeamRec(row=0, col=i, curCost=0, path=[])

Function findBestSeamRec(grid, row, col, curCost, path):
    If col out of bounds: return
    If row >= height:
        If curCost < minCost: update minCost and opPath
    Else:
        Add grid[row][col] to curCost, append col to path
        Recurse for (row+1, col-1), (row+1, col), (row+1, col+1)
        Backtrack: path.pop()
```

---

### 2. Dynamic Programming *(Recommended)*

Builds a cumulative energy map bottom-up, then traces the optimal seam in a single backward pass.

- **Time Complexity**: `O(k × H × W)`
- **Space Complexity**: `O(H × W)`
- **Characteristics**: Finds the globally optimal seam. Supports two modes:
  - **Standard**: Recalculates the energy map after every single seam removal — highest quality output.
  - **Batched**: Removes multiple seams per batch before recalculating — faster but slightly lower quality. The user can choose between modes.

**Pseudocode — `getCumulativeEnergyMap()` + `findBestSeam()`:**
```
Function getCumulativeEnergyMap(energyMap):
    cumulativeEnergyMap[0] = energyMap[0]
    For each row x from 1 to height-1:
        For each column y:
            min_energy = min of cumulativeEnergyMap[x-1][y],
                         [x-1][y-1] (if exists), [x-1][y+1] (if exists)
            cumulativeEnergyMap[x][y] = energyMap[x][y] + min_energy
    Return cumulativeEnergyMap

Function findBestSeam(grid):
    opPath[height-1] = index of min value in last row
    For each row from height-2 down to 0:
        prev_col = opPath[row+1]
        min_col = least-cost neighbor among (prev_col-1, prev_col, prev_col+1)
        opPath[row] = min_col
    Return opPath
```

---

### 3. Greedy

Starts from the minimum-energy pixel in the first row, then greedily selects the cheapest adjacent pixel in each subsequent row.

- **Time Complexity**: `O(k × H × W)`
- **Space Complexity**: `O(H)`
- **Characteristics**: Fast and simple, but does not guarantee an optimal seam since it commits to local minimums without considering the full image. An iterative approach was ultimately chosen over a recursive one for clarity and debuggability.

**Pseudocode — `findBestSeam()`:**
```
Function findBestSeam(grid):
    minidx = index of minimum in first row
    opPath = [minidx]
    For each row i from 0 to height-1:
        next = ∞
        For each neighbor j of minidx in row i+1:
            If grid[i+1][j] < next:
                next = grid[i+1][j]
                curcol = j
        minCost += next
        minidx = curcol
        opPath.append(curcol)
    Return opPath
```

---

## Algorithm Comparison

> Time complexities below are for finding **1 seam**.

| Approach | Time Complexity | Space Complexity | Notes |
|---|---|---|---|
| **Greedy** | `O(H × W)` | `O(H)` | Fast, simple; may not find optimal path |
| **Dynamic Programming** | `O(H × W)` | `O(H × W)` | Globally optimal; supports batched mode |
| **Brute Force** | `O(3^H)` | `O(H)` | Optimal but exponentially slow; impractical for large images |

*H = Image Height, W = Image Width, k = Number of seams to remove*

---

## Key Features

- **Three algorithmic approaches** with different quality/speed trade-offs
- **Batch seam removal** option in the DP approach for faster processing
- **Energy map visualization** to inspect which regions the algorithm treats as low-importance
- **User control** over number of seams and processing mode

---

## Getting Started

### Prerequisites

- Python 3.x
- NumPy
- OpenCV

### Installation

```bash
git clone https://github.com/Ghaidahiz/Content-aware-image-resizing.git
cd Content-aware-image-resizing
pip install -r requirements.txt
```

### Usage

```bash
python resize.py [options]
```

| Option | Description |
|---|---|
| `-input <filepath>` | Path to the input image |
| `-output <filepath>` | Path to save the resized image |
| `-width <width>` | Desired output width |
| `-height <height>` | Desired output height |

### Example

```bash
python resize.py -input my_image.jpg -output resized_image.jpg -width 800 -height 600
```

---

## Challenges & Lessons Learned

- **Brute Force** was tested on 8×8 images only due to the exponential explosion in computation time on larger inputs.
- **Dynamic Programming** initially had long runtimes, leading to the development of the batched variant — both modes were preserved to give users flexibility.
- **Greedy** was first implemented recursively, but an iterative approach proved simpler and easier to debug given that only a single path needs to be traced.
- The team learned Python from scratch during this project, which added an additional layer of challenge alongside the algorithmic work.
