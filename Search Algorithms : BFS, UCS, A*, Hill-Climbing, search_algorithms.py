
"""
Implementation of search algorithms: BFS, Uniform-Cost Search, A*, and Hill-Climbing.
"""

import heapq
import time
import random
from typing import List, Tuple, Dict, Set, Optional
from collections import deque

class SearchResult:
    def __init__(self, path: List[Tuple[int, int]], cost: int, 
                 nodes_expanded: int, time_taken: float, success: bool = True):
        self.path = path
        self.cost = cost
        self.nodes_expanded = nodes_expanded
        self.time_taken = time_taken
        self.success = success

class SearchAlgorithms:
    def __init__(self, grid):
        self.grid = grid
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Admissible heuristic for A* search."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def bfs(self, start: Tuple[int, int], goal: Tuple[int, int], 
            time_step: int = 0) -> SearchResult:
        """Breadth-First Search implementation."""
        start_time = time.time()
        nodes_expanded = 0
        
        if start == goal:
            return SearchResult([start], 0, 0, time.time() - start_time)
        
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            nodes_expanded += 1
            
            if current == goal:
                # Calculate actual path cost (not just steps)
                cost = sum(self.grid.get_cost(x, y) for x, y in path[1:])
                return SearchResult(path, cost, nodes_expanded, time.time() - start_time)
            
            current_time = time_step + len(path)
            for nx, ny, move_cost in self.grid.get_neighbors(current[0], current[1], current_time):
                neighbor = (nx, ny)
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return SearchResult([], float('inf'), nodes_expanded, time.time() - start_time, False)
    
    def uniform_cost_search(self, start: Tuple[int, int], goal: Tuple[int, int], 
                           time_step: int = 0) -> SearchResult:
        """Uniform-Cost Search implementation."""
        start_time = time.time()
        nodes_expanded = 0
        
        if start == goal:
            return SearchResult([start], 0, 0, time.time() - start_time)
        
        # Priority queue: (cost, position, path)
        queue = [(0, start, [start])]
        visited = set()
        cost_so_far = {start: 0}
        
        while queue:
            current_cost, current, path = heapq.heappop(queue)
            nodes_expanded += 1
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == goal:
                return SearchResult(path, current_cost, nodes_expanded, time.time() - start_time)
            
            current_time = time_step + len(path)
            for nx, ny, move_cost in self.grid.get_neighbors(current[0], current[1], current_time):
                neighbor = (nx, ny)
                new_cost = current_cost + move_cost
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))
        
        return SearchResult([], float('inf'), nodes_expanded, time.time() - start_time, False)
    
    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int], 
               time_step: int = 0) -> SearchResult:
        """A* Search implementation with Manhattan heuristic."""
        start_time = time.time()
        nodes_expanded = 0
        
        if start == goal:
            return SearchResult([start], 0, 0, time.time() - start_time)
        
        # Priority queue: (f_cost, g_cost, position, path)
        queue = [(self.manhattan_distance(start, goal), 0, start, [start])]
        cost_so_far = {start: 0}
        
        while queue:
            f_cost, g_cost, current, path = heapq.heappop(queue)
            nodes_expanded += 1
            
            if current == goal:
                return SearchResult(path, g_cost, nodes_expanded, time.time() - start_time)
            
            current_time = time_step + len(path)
            for nx, ny, move_cost in self.grid.get_neighbors(current[0], current[1], current_time):
                neighbor = (nx, ny)
                new_g_cost = g_cost + move_cost
                
                if neighbor not in cost_so_far or new_g_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_g_cost
                    h_cost = self.manhattan_distance(neighbor, goal)
                    f_cost = new_g_cost + h_cost
                    heapq.heappush(queue, (f_cost, new_g_cost, neighbor, path + [neighbor]))
        
        return SearchResult([], float('inf'), nodes_expanded, time.time() - start_time, False)
    
    def hill_climbing(self, start: Tuple[int, int], goal: Tuple[int, int], 
                     max_restarts: int = 10, max_steps: int = 100, 
                     time_step: int = 0) -> SearchResult:
        """Hill Climbing with Random Restarts for local search."""
        start_time = time.time()
        best_path = []
        best_cost = float('inf')
        total_nodes_expanded = 0
        
        for restart in range(max_restarts):
            current = start
            path = [start]
            current_cost = 0
            nodes_expanded = 0
            stuck = False
            
            for step in range(max_steps):
                if current == goal:
                    break
                    
                nodes_expanded += 1
                current_time = time_step + len(path)
                neighbors = self.grid.get_neighbors(current[0], current[1], current_time)
                
                if not neighbors:
                    stuck = True
                    break
                
                # Evaluate neighbors using heuristic
                neighbor_scores = []
                for nx, ny, move_cost in neighbors:
                    h = self.manhattan_distance((nx, ny), goal)
                    # Avoid revisiting recent positions
                    penalty = 10 if (nx, ny) in path[-3:] else 0
                    score = h + move_cost + penalty
                    neighbor_scores.append((score, nx, ny, move_cost))
                
                neighbor_scores.sort(key=lambda x: x[0])
                
                # Check for local optimum
                current_h = self.manhattan_distance(current, goal)
                if (neighbor_scores[0][0] >= current_h + current_cost and 
                    random.random() > 0.2):  # 20% chance to make suboptimal move
                    stuck = True
                    break
                
                # Choose best neighbor
                best_neighbor = neighbor_scores[0]
                nx, ny, move_cost = best_neighbor[1], best_neighbor[2], best_neighbor[3]
                
                current = (nx, ny)
                path.append(current)
                current_cost += move_cost
            
            total_nodes_expanded += nodes_expanded
            
            if current == goal and current_cost < best_cost:
                best_path = path
                best_cost = current_cost
                break  # Found satisfactory solution
            
            if stuck and restart < max_restarts - 1:
                # Random restart: start from a random position
                if len(path) > 3:
                    current = path[random.randint(1, min(3, len(path)-1))]
                    path = path[:path.index(current)+1]
                    current_cost = sum(self.grid.get_cost(x, y) for x, y in path[1:])
        
        success = best_path and best_path[-1] == goal
        return SearchResult(best_path, best_cost, total_nodes_expanded, 
                          time.time() - start_time, success)


# Test the search algorithms
if __name__ == "__main__":
    from grid import Grid
    
    # Create a test grid
    grid = Grid(5, 5)
    grid.add_static_obstacle(2, 2)
    grid.set_terrain_cost(1, 1, 3)
    
    searcher = SearchAlgorithms(grid)
    
    # Test BFS
    result = searcher.bfs((0, 0), (4, 4))
    print(f"BFS: Cost={result.cost}, Nodes={result.nodes_expanded}, Time={result.time_taken:.4f}s")
    
    # Test UCS
    result = searcher.uniform_cost_search((0, 0), (4, 4))
    print(f"UCS: Cost={result.cost}, Nodes={result.nodes_expanded}, Time={result.time_taken:.4f}s")
    
    # Test A*
    result = searcher.a_star((0, 0), (4, 4))
    print(f"A*: Cost={result.cost}, Nodes={result.nodes_expanded}, Time={result.time_taken:.4f}s")
    
    # Test Hill Climbing
    result = searcher.hill_climbing((0, 0), (4, 4))
    print(f"HC: Cost={result.cost}, Nodes={result.nodes_expanded}, Time={result.time_taken:.4f}s")
