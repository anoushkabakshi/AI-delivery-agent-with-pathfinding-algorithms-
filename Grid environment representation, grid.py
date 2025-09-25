"""
Grid environment representation for the autonomous delivery agent.
Handles static obstacles, terrain costs, and dynamic obstacles.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional

class Grid:
    def __init__(self, width: int = 5, height: int = 5):
        self.width = width
        self.height = height
        self.grid = np.ones((height, width), dtype=int)  # Default cost = 1
        self.static_obstacles = set()
        self.dynamic_obstacles = {}  # {time: set((x,y))}
        self.start = (0, 0)
        self.goal = (width-1, height-1)
    
    def set_terrain_cost(self, x: int, y: int, cost: int):
        """Set terrain cost for a cell (must be >= 1)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = max(1, cost)
    
    def add_static_obstacle(self, x: int, y: int):
        """Add a static obstacle at position (x, y)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.static_obstacles.add((x, y))
    
    def add_dynamic_obstacle(self, x: int, y: int, times: List[int]):
        """Add a dynamic obstacle that appears at specific times."""
        for time in times:
            if time not in self.dynamic_obstacles:
                self.dynamic_obstacles[time] = set()
            self.dynamic_obstacles[time].add((x, y))
    
    def is_obstacle(self, x: int, y: int, time: int = 0) -> bool:
        """Check if cell is blocked by obstacle at given time."""
        if (x, y) in self.static_obstacles:
            return True
        if time in self.dynamic_obstacles and (x, y) in self.dynamic_obstacles[time]:
            return True
        return False
    
    def get_cost(self, x: int, y: int) -> int:
        """Get terrain cost for a cell."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x]
        return float('inf')
    
    def get_neighbors(self, x: int, y: int, time: int = 0) -> List[Tuple[int, int, int]]:
        """Get valid neighboring cells (4-directional movement)."""
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.width and 0 <= ny < self.height and 
                not self.is_obstacle(nx, ny, time)):
                cost = self.get_cost(nx, ny)
                neighbors.append((nx, ny, cost))
        
        return neighbors
    
    def load_from_file(self, filename: str):
        """Load grid configuration from file."""
        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            if not lines:
                raise ValueError("Empty map file")
            
            # Determine grid size
            height = len(lines)
            width = len(lines[0].split(','))
            
            # Reinitialize grid with correct size
            self.width = width
            self.height = height
            self.grid = np.ones((height, width), dtype=int)
            self.static_obstacles = set()
            self.dynamic_obstacles = {}
            self.goal = (width-1, height-1)
            
            # Parse grid content
            for y, line in enumerate(lines):
                cells = line.split(',')
                for x, char in enumerate(cells):
                    if x >= width:
                        continue
                    char = char.strip()
                    if char == 'S':
                        self.start = (x, y)
                        self.set_terrain_cost(x, y, 1)
                    elif char == 'G':
                        self.goal = (x, y)
                        self.set_terrain_cost(x, y, 1)
                    elif char == 'X':
                        self.add_static_obstacle(x, y)
                    elif char.isdigit():
                        self.set_terrain_cost(x, y, int(char))
                    elif char == 'D':
                        # Mark for dynamic obstacle (to be added separately)
                        self.set_terrain_cost(x, y, 1)
                    else:
                        self.set_terrain_cost(x, y, 1)
                        
            print(f"Successfully loaded map from {filename} ({width}x{height})")
            
        except Exception as e:
            print(f"Error loading map file {filename}: {e}")
            # Create a default grid
            self.__init__(5, 5)
    
    def save_to_file(self, filename: str):
        """Save grid configuration to file."""
        with open(filename, 'w') as f:
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    if (x, y) == self.start:
                        row.append('S')
                    elif (x, y) == self.goal:
                        row.append('G')
                    elif (x, y) in self.static_obstacles:
                        row.append('X')
                    else:
                        row.append(str(self.grid[y, x]))
                f.write(','.join(row) + '\n')
    
    def __str__(self):
        """String representation of the grid."""
        result = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if (x, y) == self.start:
                    row.append('S')
                elif (x, y) == self.goal:
                    row.append('G')
                elif self.is_obstacle(x, y):
                    row.append('X')
                else:
                    row.append(str(self.grid[y, x]))
            result.append(' '.join(row))
        return '\n'.join(result)


# Test the Grid class
if __name__ == "__main__":
    # Create and test a grid
    grid = Grid(5, 5)
    grid.add_static_obstacle(2, 2)
    grid.set_terrain_cost(1, 1, 3)
    grid.set_terrain_cost(3, 3, 2)
    
    print("Grid created successfully:")
    print(grid)
    print(f"\nStart: {grid.start}, Goal: {grid.goal}")
    print(f"Neighbors of (0,0): {grid.get_neighbors(0, 0)}")
