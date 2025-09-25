#!/usr/bin/env python3
"""
Simplified runner for the autonomous delivery agent with text interface.
"""

import os
import sys

def main():
    # Create necessary directories
    os.makedirs("maps", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    print("🚚 Autonomous Delivery Agent - Text Interface")
    print("=" * 50)
    
    # Check if maps exist, offer to generate them
    if not os.path.exists("maps/small.map"):
        print("📁 Maps not found. Generating sample maps...")
        from src.map_generator import MapGenerator
        MapGenerator.generate_all_maps()
    
    # Run the main interface
    from main import main as run_main
    run_main()

if __name__ == "__main__":
    main()
