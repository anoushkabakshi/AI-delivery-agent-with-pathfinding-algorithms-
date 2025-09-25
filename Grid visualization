"""
Visualization utilities for the grid and agent path.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class GridVisualizer:
    def __init__(self, grid):
        self.grid = grid
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.colors = {
            'start': 'green',
            'goal': 'red',
            'obstacle': 'black',
            'path': 'blue',
            'agent': 'orange',
            'text': 'white'
        }
    
    def plot_grid(self, agent_path: List[Tuple[int, int]] = None, 
                 current_time: int = 0, title: str = "Autonomous Delivery Agent",
                 current_agent_pos: Tuple[int, int] = None):
        """Plot the grid with obstacles, terrain costs, and agent path."""
        self.ax.clear()
        
        # Create grid visualization
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cost = self.grid.get_cost(x, y)
                is_obstacle = self.grid.is_obstacle(x, y, current_time)
                is_start = (x, y) == self.grid.start
                is_goal = (x, y) == self.grid.goal
                is_agent = current_agent_pos and (x, y) == current_agent_pos
                
                # Set cell color based on content
                if is_start:
                    color = self.colors['start']
                    text = 'S'
                elif is_goal:
                    color = self.colors['goal']
                    text = 'G'
                elif is_obstacle:
                    color = self.colors['obstacle']
                    text = 'X'
                elif is_agent:
                    color = self.colors['agent']
                    text = 'A'
                else:
                    # Color based on terrain cost (lighter for lower cost)
                    intensity = max(0.3, 1.0 - (min(cost, 10) / 20.0))
                    color = (intensity, intensity, 1.0)  # Blue tint for higher costs
                    text = str(cost)
                
                # Create rectangle for cell
                rect = patches.Rectangle((x, y), 1, 1, linewidth=2, 
                                       edgecolor='black', facecolor=color, alpha=0.8)
                self.ax.add_patch(rect)
                
                # Add text
                text_color = 'white' if is_obstacle or is_start or is_goal else 'black'
                self.ax.text(x + 0.5, y + 0.5, text, ha='center', va='center', 
                           fontweight='bold', color=text_color, fontsize=12)
        
        # Plot agent path if provided
        if agent_path and len(agent_path) > 1:
            path_x = [pos[0] + 0.5 for pos in agent_path]
            path_y = [pos[1] + 0.5 for pos in agent_path]
            self.ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.7, label='Planned Path')
            self.ax.plot(path_x, path_y, 'ro', markersize=8, alpha=0.5)
        
        # Plot current agent position
        if current_agent_pos:
            agent_x, agent_y = current_agent_pos
            self.ax.plot(agent_x + 0.5, agent_y + 0.5, 'o', markersize=15, 
                       color=self.colors['agent'], label='Current Position')
        
        self.ax.set_xlim(-0.5, self.grid.width + 0.5)
        self.ax.set_ylim(-0.5, self.grid.height + 0.5)
        self.ax.set_aspect('equal')
        self.ax.set_title(title, fontsize=16, fontweight='bold')
        self.ax.set_xlabel('X Coordinate', fontsize=12)
        self.ax.set_ylabel('Y Coordinate', fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        
        # Invert y-axis to match matrix coordinates
        self.ax.invert_yaxis()
        
        plt.tight_layout()
    
    def animate_path(self, path: List[Tuple[int, int]], 
                    obstacle_manager=None, interval: float = 1.0):
        """Animate the agent following a path with dynamic obstacles."""
        if not path:
            print("No path to animate")
            return
        
        for time_step, position in enumerate(path):
            if obstacle_manager:
                obstacle_manager.update_obstacles(time_step)
            
            self.plot_grid(path, time_step, 
                          f"Time Step: {time_step}, Position: {position}", 
                          position)
            plt.pause(interval)
        
        plt.show()
    
    def save_plot(self, filename: str, dpi: int = 300):
        """Save the current plot to file."""
        plt.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"Plot saved as {filename}")
    
    def show(self):
        """Display the plot."""
        plt.show()


# Test visualization
if __name__ == "__main__":
    from grid import Grid
    from search_algorithms import SearchAlgorithms
    
    # Create a test grid
    grid = Grid(5, 5)
    grid.add_static_obstacle(2, 2)
    grid.set_terrain_cost(1, 1, 3)
    grid.set_terrain_cost(3, 3, 2)
    
    # Find a path
    searcher = SearchAlgorithms(grid)
    result = searcher.a_star(grid.start, grid.goal)
    
    # Visualize
    visualizer = GridVisualizer(grid)
    visualizer.plot_grid(result.path, title="A* Path Planning")
    visualizer.show()
