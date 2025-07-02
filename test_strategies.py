#!/usr/bin/env python3
"""
Test script to compare different strategies.
"""

import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main module
import mississippi_stud_sim as sim_module

if __name__ == "__main__":
    print("Testing different strategies with 100 hands each:")
    print("=" * 60)
    
    print("\nPoint Strategy (default):")
    sim_module.simulate(100, show_each_hand=False, strategy_name='point')
    
    print("\nConservative Strategy:")
    sim_module.simulate(100, show_each_hand=False, strategy_name='conservative')
    
    print("\nOptimal Strategy:")
    sim_module.simulate(100, show_each_hand=False, strategy_name='optimal')
    
    print("\n" + "=" * 60)
    print("All strategies comparison complete!")
