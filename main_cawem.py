#! /bin/env python
#
#  Radostin Simitev, orcid.org/0000-0002-2207-5789
#  Glasgow, 2024-11-05
#
#  Interactive Cellular Automaton of Cardiac Tissue
#  (hands-on fun for SofTMech Parient Dialogue Day 2024-11-26, Clydebank)
#
import sys
import numpy as np
np.set_printoptions(linewidth=2000, threshold=sys.maxsize)
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define cell states
RESTING = 0
EXCITED = 1

# Interactive user input for simulation parameters
def get_user_inputs():

    # Prompt for default or custom parameters
    print("")
    print("Choose an experiment to simulate:")
    print("")
    print("1. Plane Wave")
    print("2. Spiral Wave")
    print("3. Pair of Spiral Waves")
    print("4. Defibrillation of a Spiral Wave")
    print("5. Re-entry around an obstacle")
    print("6. Chaos & fibrillation")
    print("7. Annihilation")
    print("")
    
    experiment_choice = int(input("Enter your choice (1-7): "))
    grid_size = 100
    steps = 300
    animation_speed = 200
    defibrillation_time = None

    if experiment_choice == 6:   # Chaos
            n = 2+1
            max_refractory_period = 10
            vary_refractory_period = 1  # no
    else:
        print('')
        use_custom = input("Would you like to run with custom parameters? (yes/no): ").strip().lower()
        
        # Default values for parameters
        if use_custom == "no":
            if experiment_choice == 1:  # Simple Plane Wave
                n = 1+1
                max_refractory_period = 10
                vary_refractory_period = 0  # no
            elif experiment_choice == 2:  # Spiral Wave
                n = 2+1
                max_refractory_period = 10
                vary_refractory_period = 0  # no
            elif experiment_choice == 3:  # Pair of Spiral Waves
                n = 2+1
                max_refractory_period = 6
                vary_refractory_period = 0  # no
            elif experiment_choice == 4:  # Defibrillation
                n = 2+1
                max_refractory_period = 6
                vary_refractory_period = 0  # no
                defibrillation_time = 80
            elif experiment_choice == 5: # reentry around an obstacle
                n = 1+1
                max_refractory_period = 6
                vary_refractory_period = 0  # no
            if experiment_choice == 7:  # Annihilation
                n = 1+1
                max_refractory_period = 5
                vary_refractory_period = 0  # no
        else:
            print("")
            print("Set cardiac cell properties. ")
            n = int(input("Enter excitability (the minimum number of excited neighbors required to excite a cell) (1-4): ")) + 1
            max_refractory_period = int(input("Enter maximum refractory period (e.g., 10): "))
            vary_refractory_period= int(input("Cell-specific refractory period? (no = 0, yes = 1): "))
            
            if experiment_choice in [4,100]:
                defibrillation_time = int(input("Enter the time step for defibrillation shock (> 80): "))
                
    return experiment_choice, grid_size, steps, max_refractory_period, animation_speed, defibrillation_time, n, vary_refractory_period

# Define obstacle region
def obstacle(n_grid,refractory_grid):
    region0 = (slice(0,100), slice(0, 100))
    region1 = (slice(1,33), slice(30, 99))
    region2 = (slice(33, 65), slice(30, 70))
    region3 = (slice(65, 99), slice(30, 60))

    n_grid[region1] = 1
    n_grid[region2] = 10
    n_grid[region3] = 1
    refractory_grid[region1] = 3 
    refractory_grid[region2] = 1000
    refractory_grid[region3] = 30
    return n_grid,refractory_grid

# Set up the initial conditions based on user choice
def setup_initial_conditions(grid, n_grid, refractory_grid, experiment_choice, n, max_refractory_period,vary_refractory_period):
    n_grid[:, :] = np.random.randint(1, n, size=grid.shape)
    if vary_refractory_period == 1:
        refractory_grid[:, :] = np.random.randint(1, max_refractory_period + 1, size=grid.shape)
        #refractory_grid[:, :] = np.random.randint(max_refractory_period-max_refractory_period*0.2, max_refractory_period + 1, size=grid.shape)
    else:
        refractory_grid[:, :] = max_refractory_period

    if experiment_choice == 1:  # Simple Plane Wave
        grid[:, 0] = EXCITED
    elif experiment_choice == 2:  # Spiral Wave
        excited_region = (slice(30, 99), slice(40, 45))
        refractory_region = (slice(50, 99), slice(45, 50))
        grid[excited_region] = EXCITED
        grid[refractory_region] = -1
    elif experiment_choice == 3 or experiment_choice == 6 :  # Pair of Spiral Waves
        excited_region1 = (slice(60, 99), slice(70, 75))
        refractory_region1 = (slice(80, 99), slice(75, 80))
        grid[excited_region1] = EXCITED
        grid[refractory_region1] = -1
        excited_region2 = (slice(20, 99), slice(20, 25))
        refractory_region2 = (slice(40, 99), slice(15, 20))
        grid[excited_region2] = EXCITED
        grid[refractory_region2] = -1
    elif experiment_choice == 4:  # Defibrillation
        excited_region = (slice(30, 99), slice(40, 45))
        refractory_region = (slice(50, 99), slice(45, 50))
        grid[excited_region] = EXCITED
        grid[refractory_region] = -1
        grid[:, 0] = EXCITED
    elif experiment_choice == 5: # reentry around an obstacle
        refractory_grid[:, :] = max_refractory_period
        n_grid,refractory_grid = obstacle(n_grid,refractory_grid)
        grid[:, 0] = EXCITED
        # print(n_grid)
        # print(refractory_grid)
    if experiment_choice == 7:  # Annihilation
        grid[:, 0] = EXCITED
        grid[:, -1] = EXCITED

# Cellular automaton state transition rules
def update_grid(grid, refractory_grid, current_time, defibrillation_time, experiment_choice, n_grid):
    if experiment_choice == 4 and current_time == defibrillation_time:
        grid[1:99, 1:99] = EXCITED  # Apply defibrillation shock
        print('* * * DEFIBRILLATE * * *')

    if experiment_choice in [5,7] and current_time > 20:
        grid[:,0] = RESTING
        grid[:,-1] = RESTING
    
    new_grid = grid.copy()
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            if grid[i, j] == RESTING:
                excited_neighbors = np.sum(grid[i-1:i+2, j-1:j+2] == EXCITED) - (grid[i, j] == EXCITED)
                if excited_neighbors >= n_grid[i, j]:
                    new_grid[i, j] = EXCITED
            elif grid[i, j] == EXCITED:
                new_grid[i, j] = -refractory_grid[i, j]
            elif grid[i, j] < 0:
                new_grid[i, j] += 1
    
    if experiment_choice == 4 and current_time > defibrillation_time:
        new_grid[:, 0] = EXCITED
    return new_grid


def visualize(grid, steps, refractory_grid, animation_speed, defibrillation_time, experiment_choice, n_grid):
    # Enable interactive mode
    plt.ion()
    
    fig, ax = plt.subplots(figsize=(6, 6))
    cmap = plt.cm.coolwarm
    img = ax.imshow(grid, cmap=cmap, vmin=-1, vmax=1)
    time_text = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha="center")
    
    def animate(step):
        global grid
        grid[:] = update_grid(grid, refractory_grid, step, defibrillation_time, experiment_choice, n_grid)
        img.set_data(grid)
        time_text.set_text(f'Time step: {step}')
        return [img, time_text]

    ani = animation.FuncAnimation(fig, animate, frames=steps, interval=animation_speed, blit=True, repeat=False)

    # Function to close the figure after animation ends
    def on_animation_complete(*args):
        plt.close(fig)

    # Set up callback to close figure when animation completes
    ani._stop = on_animation_complete  # Override internal stop to trigger on completion
    
    # Display the plot without blocking
    plt.show(block=False)
    
    # Keep the plot active until animation completes
    plt.pause((steps * animation_speed) / 1000)
    plt.close(fig)
    
# Main program
if __name__ == "__main__":
    print("")
    print("=====================================================================")
    print("=                                                                   =")
    print("= Welcome to the Interactive Cellular Automaton for Cardiac Tissue! =")
    print("=                                                                   =")
    print("=====================================================================")


    while True:
        experiment_choice, grid_size, steps, max_refractory_period, animation_speed, defibrillation_time, n, vary_refractory_period = get_user_inputs()
        grid = np.zeros((grid_size, grid_size), dtype=int)
        n_grid = np.zeros((grid_size, grid_size), dtype=int)
        refractory_grid = np.zeros((grid_size, grid_size), dtype=int)
        
        # Set up initial conditions for the chosen scenario
        setup_initial_conditions(grid, n_grid, refractory_grid, experiment_choice, n, max_refractory_period, vary_refractory_period)
        
        # Run the visualization for the selected scenario
        visualize(grid, steps, refractory_grid, animation_speed, defibrillation_time, experiment_choice, n_grid)
        
        # Ask if the user wants to try another scenario
        print('')
        run_again = input("Would you like to explore another scenario? (yes/no): ").strip().lower()
        print('')
        print("---------------------------------------------------------------------")
        
        # Exit if the user chooses not to run another simulation
        if run_again != "yes":
            print("Exiting the simulation. Thank you!")
            break


