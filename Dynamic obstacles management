"""
Dynamic obstacles management for the grid environment.
"""

import random
from typing import List, Tuple, Dict

class DynamicObstacleManager:
    def __init__(self, grid):
        self.grid = grid
        self.moving_obstacles = []  # List of moving obstacles with schedules
    
    def add_moving_obstacle(self, start_pos: Tuple[int, int], path: List[Tuple[int, int]], 
                           speed: int = 1, start_time: int = 0):
        """Add a moving obstacle that follows a path."""
        obstacle = {
            'position': start_pos,
            'path': path,
            'current_index': 0,
            'speed': speed,
            'start_time': start_time,
            'cycle_length': len(path)
        }
        self.moving_obstacles.append(obstacle)
        
        # Add initial position to grid
        self.grid.add_dynamic_obstacle(start_pos[0], start_pos[1], [start_time])
    
    def add_random_moving_obstacle(self, path_length: int = 5, speed: int = 2, 
                                  start_time: int = 0):
        """Add a randomly moving obstacle."""
        # Find a valid starting position (not on start, goal, or obstacle)
        valid_positions = []
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                pos = (x, y)
                if (not self.grid.is_obstacle(x, y) and 
                    pos != self.grid.start and 
                    pos != self.grid.goal):
                    valid_positions.append(pos)
        
        if not valid_positions:
            return False
        
        start_pos = random.choice(valid_positions)
        
        # Generate a random path using random walk
        path = [start_pos]
        current_pos = start_pos
        
        for _ in range(path_length - 1):
            neighbors = self.grid.get_neighbors(current_pos[0], current_pos[1])
            if not neighbors:
                break
            
            # Filter out positions that are start, goal, or already in path
            valid_neighbors = [n for n in neighbors 
                             if (n[0], n[1]) != self.grid.start 
                             and (n[0], n[1]) != self.grid.goal
                             and (n[0], n[1]) not in path]
            
            if not valid_neighbors:
                # If no valid neighbors, choose from all neighbors
                valid_neighbors = neighbors
            
            next_pos = random.choice(valid_neighbors)
            path.append((next_pos[0], next_pos[1]))
            current_pos = (next_pos[0], next_pos[1])
        
        self.add_moving_obstacle(start_pos, path, speed, start_time)
        return True
    
    def update_obstacles(self, current_time: int):
        """Update positions of all moving obstacles for the given time."""
        # Clear all dynamic obstacles
        self.grid.dynamic_obstacles.clear()
        
        for obstacle in self.moving_obstacles:
            if current_time < obstacle['start_time']:
                continue
            
            time_since_start = current_time - obstacle['start_time']
            step_index = (time_since_start // obstacle['speed']) % obstacle['cycle_length']
            position = obstacle['path'][step_index]
            
            # Add obstacle position for this time step
            if current_time not in self.grid.dynamic_obstacles:
                self.grid.dynamic_obstacles[current_time] = set()
            self.grid.dynamic_obstacles[current_time].add(position)
    
    def add_scheduled_obstacle(self, schedule: Dict[int, Tuple[int, int]]):
        """Add an obstacle with a specific schedule."""
        for time, position in schedule.items():
            self.grid.add_dynamic_obstacle(position[0], position[1], [time])
    
    def get_obstacle_positions(self, current_time: int) -> List[Tuple[int, int]]:
        """Get all dynamic obstacle positions at the given time."""
        positions = []
        if current_time in self.grid.dynamic_obstacles:
            positions = list(self.grid.dynamic_obstacles[current_time])
        return positions
    
    def clear_all_obstacles(self):
        """Clear all dynamic obstacles."""
        self.grid.dynamic_obstacles.clear()
        self.moving_obstacles.clear()


# Test dynamic obstacles
if __name__ == "__main__":
    from grid import Grid
    
    grid = Grid(5, 5)
    manager = DynamicObstacleManager(grid)
    
    # Add a moving obstacle that goes right 3 steps then back
    path = [(1, 1), (2, 1), (3, 1), (2, 1), (1, 1)]
    manager.add_moving_obstacle((1, 1), path, speed=1, start_time=0)
    
    # Test obstacle movement
    for t in range(10):
        manager.update_obstacles(t)
        obstacles = manager.get_obstacle_positions(t)
        print(f"Time {t}: Obstacles at {obstacles}")
