import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


# 'warehouse_map' defines the layout of the warehouse with walls (1) and empty spaces (0).
warehouse_map = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])

map_size = warehouse_map.shape 
num_ants = 7  # Number of RFID antennas to be placed
num_particles = 80  # Number of PSO particles for optimization
num_iters = 100  # Number of optimization iterations

signalrange = 0.46  # Signal decay factor for coverage propagation

# Get valid placement positions (non-wall locations)
valid_positions = np.argwhere(warehouse_map == 0)
valid_set = set(map(tuple, valid_positions))  

# Initialize particles randomly in valid locations
particles = valid_positions[np.random.choice(len(valid_positions), (num_particles, num_ants))]
velocity = np.zeros_like(particles, dtype=float) 

# PSO parameters
w = 0.5  # Inertia weight for velocity update
c1, c2 = 1.5, 1.5  # Cognitive and social weights for PSO

def compute_coverage(antennas, repulsion_weight=0.7, critical_zone_weight=1.8):
    """
    Computes the coverage score for a given antenna placement.
    
    The coverage score is based on signal strength, critical zone adjustments, 
    and repulsion between antennas to avoid overlap.
    
    Args:
        antennas (ndarray): Array of antenna positions (x, y).
        repulsion_weight (float): Weight for repulsion penalty between antennas.
        critical_zone_weight (float): Weight for penalty in critical zones.
    
    Returns:
        float: The calculated coverage score.
    """
    coverage_map = np.zeros(map_size, dtype=float)  
    
  
    critical_zones = np.zeros_like(warehouse_map, dtype=float)
    for x in range(1, map_size[0] - 1):
        for y in range(1, map_size[1] - 1):
            if warehouse_map[x, y] == 0:  
                if ((warehouse_map[x-1, y] == 1 and warehouse_map[x+1, y] == 1 and warehouse_map[x, y-1] == 0 and warehouse_map[x, y+1] == 0) or
                    (warehouse_map[x, y-1] == 1 and warehouse_map[x, y+1] == 1 and warehouse_map[x-1, y] == 0 and warehouse_map[x+1, y] == 0)):
                    critical_zones[x, y] = 1 
    
    # Propagate signal from each antenna position
    for x, y in antennas:
        for i in range(-4, 5):
            for j in range(-4, 5):
                nx, ny = x + i, y + j
                if 0 <= nx < map_size[0] and 0 <= ny < map_size[1] and warehouse_map[nx, ny] == 0:
                    distance = np.sqrt(i**2 + j**2)
                    if distance < 8:  
                        decay = np.exp(-distance / signalrange) 
                        coverage_map[nx, ny] += decay 

                        # Reflections: simulate signal bounce from walls
                        if warehouse_map[nx, ny] == 0: 
                            for rx, ry in [(nx, 2*ny - y), (2*nx - x, ny)]: 
                                if 0 <= rx < map_size[0] and 0 <= ry < map_size[1]:
                                    if warehouse_map[rx, ry] == 1:  
                                        coverage_map[rx, ry] += decay / 2 

                        # Add critical zone adjustment
                        if critical_zones[nx, ny]:
                            coverage_map[nx, ny] += critical_zone_weight

    # Normalize the coverage score over valid spaces
    valid_mask = (warehouse_map == 0)
    coverage_score = np.mean(coverage_map[valid_mask])  # Average coverage over valid positions

    # Repulsion: penalize close antennas (distance between antennas)
    distances = cdist(antennas, antennas)
    np.fill_diagonal(distances, np.inf)  # Ignore diagonal (self-to-self distances)
    repulsion_score = np.sum(np.exp(-distances / 3))  # Repulsion based on distance

    return coverage_score - repulsion_weight * repulsion_score  # Return total fitness score

def plot_coverage_heatmap(warehouse_map, antennas):
    """
    Plots the heatmap of signal coverage across the warehouse, including antenna placement.
    
    Args:
        warehouse_map (ndarray): Layout of the warehouse with walls (1) and empty spaces (0).
        antennas (ndarray): Positions of the RFID antennas.
    """
    map_size = warehouse_map.shape
    coverage_map = np.zeros(map_size, dtype=float)

    # Propagate signal from each antenna with reflections
    for ant in antennas:
        x, y = ant
        for i in range(-4, 5):
            for j in range(-4, 5):
                nx, ny = x + i, y + j
                if 0 <= nx < map_size[0] and 0 <= ny < map_size[1]:
                    if warehouse_map[nx, ny] == 0:
                        signal_strength = np.exp(-np.sqrt(i**2 + j**2) / 2)  # Signal strength decay

                        coverage_map[nx, ny] += signal_strength

                        # Reflections from walls
                        if warehouse_map[nx, ny] == 0:  # Reflect off walls
                            for rx, ry in [(nx, 2*ny - y), (2*nx - x, ny)]:  
                                if 0 <= rx < map_size[0] and 0 <= ry < map_size[1]:
                                    if warehouse_map[rx, ry] == 1: 
                                        coverage_map[rx, ry] += signal_strength / 2 

    # Plot the coverage heatmap
    plt.figure(figsize=(7, 6))
    plt.imshow(coverage_map, cmap="viridis", origin='upper')
    plt.colorbar(label="Signal Strength")
    plt.imshow(warehouse_map, cmap="gray_r", alpha=0.3)  # Overlay warehouse layout
    plt.scatter(antennas[:, 1], antennas[:, 0], color='red', edgecolor='black', s=100, label="RFID Antennas")
    plt.title("RFID Coverage Heatmap with Antenna Placement and Reflections")
    plt.legend()
    plt.grid(False)
    plt.show()

def plot_coverage_overlap(warehouse_map, antennas):
    """
    Plots the overlap map showing the number of antennas covering each cell.
    
    Args:
        warehouse_map (ndarray): Layout of the warehouse.
        antennas (ndarray): Positions of the RFID antennas.
    """
    map_size = warehouse_map.shape
    overlap_map = np.zeros(map_size, dtype=int)

    for ant in antennas:
        x, y = ant
        for i in range(-4, 5):
            for j in range(-4, 5):
                nx, ny = x + i, y + j
                if 0 <= nx < map_size[0] and 0 <= ny < map_size[1]:
                    if warehouse_map[nx, ny] == 0:
                        overlap_map[nx, ny] += 1  # Count how many antennas cover this cell

    # Plot the overlap map
    plt.figure(figsize=(7, 6))
    plt.imshow(overlap_map, cmap='plasma', origin='upper')
    plt.colorbar(label="Number of Antennas Covering Cell")
    plt.imshow(warehouse_map, cmap="gray_r", origin='upper', alpha=0.3)
    plt.scatter(antennas[:, 1], antennas[:, 0], c='cyan', edgecolor='black', s=100, label='Antennas')
    plt.title("Coverage Overlap Map")
    plt.legend()
    plt.grid(False)
    plt.show()

# PSO Main Loop
global_best = None  # Best solution across all iterations
best_fitness = -np.inf  # Initialize the best fitness value
fitness_history = []  # Store fitness history for plotting

for _ in range(num_iters):
    fitness = np.array([compute_coverage(p) for p in particles])  # Calculate fitness for each particle

    # Update global best if current fitness is better
    if np.max(fitness) > best_fitness:
        best_fitness = np.max(fitness)
        global_best = particles[np.argmax(fitness)].copy()

    fitness_history.append(best_fitness) 

    # Update velocities and positions of particles
    r1, r2 = np.random.rand(), np.random.rand()  
    velocity = w * velocity + c1 * r1 * (particles - global_best) + c2 * r2 * (particles - global_best)
    new_particles = np.round(particles + velocity).astype(int)

    # Ensure that particles stay in valid positions
    for i in range(num_particles):
        for j in range(num_ants):
            if tuple(new_particles[i, j]) not in valid_set:
                new_particles[i, j] = particles[i, j]  

    particles = new_particles  # Update particle positions

# Plot final best placement
plot_coverage_heatmap(warehouse_map, global_best)

# Plot overlap map
plot_coverage_overlap(warehouse_map, global_best)

# Show fitness history
plt.plot(fitness_history)
plt.title("PSO Fitness History")
plt.xlabel("Iteration")
plt.ylabel("Best Fitness")
plt.show()
