# RFID Antenna Optimization using PSO (Particle Swarm Optimization)

## Project Overview

This project aims to optimize the placement of RFID antennas in a warehouse environment using Particle Swarm Optimization (PSO). The goal is to maximize the coverage area while minimizing interference between antennas. The project uses a simulation of signal propagation and considers wall reflections and critical zones for more accurate results. It is an application of optimization techniques in real-world scenarios like asset tracking in a warehouse setting.

## Key Features
- **RFID Antenna Placement**: Optimizes the placement of RFID antennas to achieve maximum coverage in a warehouse layout.
- **Signal Propagation**: The algorithm simulates signal decay and wall reflections to estimate coverage.
- **Critical Zone Adjustment**: Special adjustments are made for narrow or critical zones that require more coverage.
- **Repulsion Penalty**: The PSO algorithm penalizes placements that are too close to avoid interference between antennas.

## How the Code is Structured

The code is divided into several key sections:

1. **Warehouse Layout**: The layout of the warehouse is represented by a 2D numpy array where `1` denotes a wall and `0` denotes an empty space where antennas can be placed.
2. **PSO Algorithm**: The core optimization algorithm. It adjusts the position of the antennas using the principles of PSO to maximize coverage while considering repulsion between antennas.
3. **Signal Propagation Simulation**: The signal decay from each antenna is simulated, and wall reflections are accounted for. Critical zones are also identified and handled.
4. **Visualization**: Several visualizations are provided, including a heatmap of coverage, a map showing antenna overlap, and the optimized placement of antennas.

## Key Functions and Their Roles

### `compute_coverage(antennas)`
- **Description**: Calculates the coverage score for a given set of antenna placements. It accounts for signal decay, wall reflections, critical zones, and antenna repulsion.
- **Parameters**: 
  - `antennas`: A list of antenna coordinates (x, y).
  - `repulsion_weight`: The weight for the repulsion penalty.
  - `critical_zone_weight`: The weight for the adjustment in critical zones.
  
### `plot_coverage_heatmap(warehouse_map, antennas)`
- **Description**: Generates and displays a heatmap of the signal coverage in the warehouse layout, including antenna placements.
- **Parameters**:
  - `warehouse_map`: The layout of the warehouse.
  - `antennas`: The optimized antenna placements.

### `plot_coverage_overlap(warehouse_map, antennas)`
- **Description**: Displays a map of coverage overlap, showing how many antennas cover each cell.
- **Parameters**:
  - `warehouse_map`: The layout of the warehouse.
  - `antennas`: The optimized antenna placements.

### `PSO Main Loop`
- **Description**: The main loop of the PSO algorithm, which updates the positions of the antennas and calculates the fitness of each position.

## Hyperparameters and Tuning

### Key Hyperparameters:

1. **`num_ants`**: Number of RFID antennas. 
   - **Effect**: More antennas may improve coverage but also increase complexity and computation time.

2. **`num_particles`**: Number of particles in the PSO algorithm.
   - **Effect**: More particles provide better exploration of the search space but require more computation. A larger number may lead to slower convergence.

3. **`num_iters`**: Number of iterations for the PSO optimization process.
   - **Effect**: More iterations typically improve the optimization results but at the cost of additional computation time.

4. **`signalrange`**: Signal decay factor for the propagation simulation.
   - **Effect**: Higher values result in a larger coverage area per antenna, whereas lower values make the antennas cover smaller areas.

5. **`w` (Inertia Weight)**: Controls the influence of the previous velocity of particles in the PSO algorithm.
   - **Effect**: A higher `w` encourages exploration, while a lower `w` promotes exploitation of the best solutions found.

6. **`c1` and `c2` (Cognitive and Social Weights)**: These parameters control how much the particle is influenced by its own best-known position and the global best-known position.
   - **Effect**: Larger values of `c1` and `c2` encourage faster convergence but can lead to premature convergence (stopping at local optima).

7. **`repulsion_weight`**: The penalty applied to close antenna placements.
   - **Effect**: Increasing this value increases the penalty for placing antennas too close together, encouraging better distribution and reducing interference.

8. **`critical_zone_weight`**: The weight for adjusting coverage in critical zones.
   - **Effect**: Increasing this weight increases the importance of optimizing coverage in narrow or critical zones.

### Effect of Tuning:

- Increasing **`num_particles`** and **`num_iters`** can improve the results but will also slow down the algorithm.
- Adjusting the **`signalrange`** will affect the size of the coverage area; a larger range might reduce the overall number of antennas needed but could lead to interference issues.
- Increasing **`repulsion_weight`** helps to spread out the antennas and reduces interference but can lead to suboptimal coverage if set too high.
- **`c1` and `c2`** play a crucial role in controlling the exploration and exploitation balance, and their values can influence the convergence rate of the algorithm.

## Assumptions
- The warehouse layout is static and known in advance.
- The signal range is assumed to be uniform and isotropic.
- The algorithm only considers two-dimensional layouts (no height or 3D considerations).

## Known Issues
- The algorithm currently uses a simplified model for signal propagation, which may not perfectly reflect real-world RF conditions.
- Wall reflections are treated as simple horizontal and vertical reflections. More complex behaviors (e.g., diffraction, scattering) are not simulated.
- Critical zone detection might not cover all possible cases of narrow aisles or areas that need special attention.

## Instructions to Run the Code

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/RFID-Optimization.git
