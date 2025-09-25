# AI-delivery-agent-with-pathfinding-algorithms-
Autonomous Delivery Agent: AI pathfinding in dynamic 2D grid cities. Implements BFS, Uniform-Cost, A*, and local search algorithms. Handles static obstacles, terrain costs, and moving vehicles. Features intelligent replanning with performance comparison across multiple map complexities. Python implementation with modular design.

The agent must efficiently navigate through static obstacles, varying terrain costs, and dynamic moving obstacles to deliver packages while optimizing for cost and time.

Key Requirements:
1. Model environment with static/dynamic obstacles and terrain costs
2. Implement uninformed (BFS, UCS) and informed (A*) search algorithms
3. Implement local search with replanning (Hill-Climbing)
4. Handle dynamic obstacles with real-time replanning
5. Compare algorithm performance experimentally
6. Provide comprehensive analysis and documentation

   PROJECT STRUCTURE 
   autonomous_delivery_agent/
├── src/                    # Source code
│   ├── grid.py            # Grid environment representation
│   ├── agent.py           # Delivery agent implementation
│   ├── search_algorithms.py # BFS, UCS, A*, Hill-Climbing
│   ├── dynamic_obstacles.py # Moving obstacles management
│   ├── text_visualizer.py # Console-based visualization
│   ├── map_generator.py   # Map creation utilities
│   └── __init__.py        # Package initialization
├── maps/                  # Test map files

License
This project is part of CSA2001 - Fundamentals of AI and ML coursework. The code is provided for educational purposes.


