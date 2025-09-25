"""
Main CLI interface for the autonomous delivery agent with text-based visualization.
"""

import argparse
import time
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from grid import Grid
from agent import DeliveryAgent
from search_algorithms import SearchAlgorithms
from dynamic_obstacles import DynamicObstacleManager
from text_visualizer import TextVisualizer
from map_generator import MapGenerator

def create_sample_maps():
    """Create sample map files if they don't exist."""
    maps_dir = "maps"
    if not os.path.exists(maps_dir):
        print("📁 Creating maps directory...")
        os.makedirs(maps_dir)
    
    required_maps = ['small.map', 'medium.map', 'large.map', 'dynamic.map']
    maps_exist = all(os.path.exists(f"{maps_dir}/{map_file}") for map_file in required_maps)
    
    if not maps_exist:
        print("🗺️ Generating sample maps...")
        MapGenerator.generate_all_maps()
    else:
        print("✅ Maps already exist.")

def run_single_algorithm(grid, algorithm: str, use_dynamic: bool = False) -> dict:
    """Run a single algorithm and return results."""
    print(f"\n{'='*60}")
    print(f"🚀 RUNNING {algorithm.upper()} ALGORITHM")
    print(f"{'='*60}")
    
    # Add dynamic obstacles if requested
    obstacle_manager = None
    if use_dynamic:
        obstacle_manager = DynamicObstacleManager(grid)
        obstacle_manager.add_random_moving_obstacle(path_length=5, speed=2, start_time=2)
        obstacle_manager.add_random_moving_obstacle(path_length=4, speed=3, start_time=5)
        print("✅ Added dynamic obstacles")
    
    # Create agent and run delivery
    agent = DeliveryAgent(grid)
    start_time = time.time()
    metrics = agent.deliver_package(algorithm, max_replans=3, max_steps=100)
    metrics['total_time_taken'] = time.time() - start_time
    
    # Display results
    visualizer = TextVisualizer(grid)
    visualizer.display_grid(
        agent.position, 
        metrics.get('final_path', []), 
        metrics.get('total_time', 0),
        f"Results - {algorithm.upper()}"
    )
    
    print(f"\n📊 {algorithm.upper()} RESULTS:")
    print(f"   Success: {'✅' if metrics['success'] else '❌'}")
    print(f"   Total Cost: {metrics['total_cost']}")
    print(f"   Time Steps: {metrics['total_time']}")
    print(f"   Nodes Expanded: {metrics['nodes_expanded']}")
    print(f"   Replans: {metrics['replans']}")
    print(f"   Planning Time: {metrics['planning_time']:.4f}s")
    print(f"   Total Time: {metrics['total_time_taken']:.4f}s")
    
    if metrics['success']:
        print(f"   Path Length: {len(metrics['final_path'])} steps")
    
    # Show execution log for dynamic scenarios
    if use_dynamic and metrics['replans'] > 0:
        print(f"\n📝 EXECUTION LOG (Last 5 entries):")
        for log_entry in agent.log[-5:]:
            print(f"   {log_entry}")
    
    return metrics

def compare_algorithms(grid, algorithms: list, use_dynamic: bool = False) -> dict:
    """Compare multiple algorithms and display results."""
    print(f"\n{'='*80}")
    print("📊 ALGORITHM COMPARISON")
    print(f"{'='*80}")
    
    results = {}
    
    for algorithm in algorithms:
        print(f"\n🔍 Testing {algorithm}...")
        results[algorithm] = run_single_algorithm(grid, algorithm, use_dynamic)
        time.sleep(1)  # Brief pause between algorithms
    
    # Display comparison table
    visualizer = TextVisualizer(grid)
    visualizer.show_algorithm_comparison(results)
    
    return results

def demonstrate_dynamic_replanning():
    """Demonstrate dynamic replanning capabilities."""
    print(f"\n{'='*80}")
    print("🔄 DYNAMIC REPLANNING DEMONSTRATION")
    print(f"{'='*80}")
    
    # Create a suitable map
    grid = MapGenerator.create_dynamic_map()
    
    # Add dynamic obstacles
    obstacle_manager = DynamicObstacleManager(grid)
    
    # Add obstacles with interesting patterns
    path1 = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    path2 = [(5, 5), (4, 5), (3, 5), (2, 5), (1, 5)]
    
    obstacle_manager.add_moving_obstacle((1, 1), path1, speed=2, start_time=2)
    obstacle_manager.add_moving_obstacle((5, 5), path2, speed=3, start_time=1)
    
    # Run the demonstration
    visualizer = TextVisualizer(grid)
    visualizer.show_dynamic_replanning_demo(DeliveryAgent(grid), obstacle_manager)

def main():
    parser = argparse.ArgumentParser(description="Autonomous Delivery Agent - Text Interface")
    parser.add_argument("--map", type=str, help="Map file to load (e.g., maps/small.map)")
    parser.add_argument("--algorithm", choices=["bfs", "ucs", "astar", "hillclimb", "all"], 
                       default="all", help="Search algorithm to use")
    parser.add_argument("--size", type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'), 
                       help="Grid size for random map")
    parser.add_argument("--dynamic", action="store_true", help="Add dynamic obstacles")
    parser.add_argument("--compare", action="store_true", help="Compare all algorithms")
    parser.add_argument("--demo", action="store_true", help="Run dynamic replanning demo")
    parser.add_argument("--generate-maps", action="store_true", help="Generate sample maps")
    
    args = parser.parse_args()
    
    # Generate maps if requested or if they don't exist
    if args.generate_maps or not os.path.exists("maps"):
        MapGenerator.generate_all_maps()
    
    # Run demonstration if requested
    if args.demo:
        demonstrate_dynamic_replanning()
        return
    
    # Create or load grid
    grid = Grid(5, 5)  # Default size
    
    if args.map:
        grid = Grid()
        grid.load_from_file(args.map)
        print(f"✅ Loaded map from {args.map}")
    elif args.size:
        grid = Grid(args.size[0], args.size[1])
        # Add random obstacles
        for _ in range(args.size[0] * args.size[1] // 6):
            x = random.randint(0, args.size[0]-1)
            y = random.randint(0, args.size[1]-1)
            if (x, y) != grid.start and (x, y) != grid.goal:
                grid.add_static_obstacle(x, y)
        print(f"✅ Created random {args.size[0]}x{args.size[1]} map")
    else:
        # Use default small map
        create_sample_maps()
        grid.load_from_file("maps/small.map")
        print("✅ Using default small map")
    
    # Display initial grid
    visualizer = TextVisualizer(grid)
    visualizer.display_grid(grid.start, [], 0, "Initial Grid State")
    
    # Determine algorithms to run
    if args.algorithm == "all" or args.compare:
        algorithms = ["bfs", "ucs", "astar", "hillclimb"]
    else:
        algorithms = [args.algorithm]
    
    # Run the selected operation
    if args.compare:
        results = compare_algorithms(grid, algorithms, args.dynamic)
    else:
        for algorithm in algorithms:
            run_single_algorithm(grid, algorithm, args.dynamic)
    
    print(f"\n{'='*60}")
    print("🎉 AUTONOMOUS DELIVERY AGENT SIMULATION COMPLETED!")
    print(f"{'='*60}")

if __name__ == "__main__":
    import random
    main()
