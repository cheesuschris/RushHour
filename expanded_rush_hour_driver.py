#--------------------------------------------------------------------------------------------------------


"""
FINAL DRIVER: ALL FEATURES MERGED AND FINISHED PROJECT
Problem modifications:
- Supports configuration for any valid rush_hour setup.
- The board is now 6x6 instead of 4x4.
- There can be both single-cell cars as well as double-cell trucks.
- Positions are 1-indexed.
- The direction of trucks only move in direction of the longest axis (even though their direction is included).
- There can be any number of vehicles.
- There can be multi-step moves at the same time.
- Takes in as input "config": the same dictionary definition that the original Extra Credit had.
- Supports multi-step moves
- Ex input:
    ```
        config = {
            'cars': {
                'R': {'pos': (3, 1), 'dir': 'Horizontal'},   # Red car, horizontal
                'A': {'pos': (1, 1), 'dir': 'Horizontal'},   # Car A, horizontal
                'B': {'pos': (4, 3), 'dir': 'Vertical'}      # Car B, vertical
            },
            'trucks': {
                'T1': {'pos': ((3, 2), (4, 2)), 'dir': 'Vertical'},  # Horizontal truck
                'T2': {'pos': ((2, 3), (3, 3)), 'dir': 'Vertical'}     # Vertical truck
            },
            'goal': {
                'R': (3, 6),                                 # Red car must reach exit
                'T1': ((1, 2), (2, 2))                       # Truck T2 must move up two cells
            }
        }
    ```
"""


#--------------------------------------------------------------------------------------------------------

from example_EC_1 import rush_hour_with_trucks1
from example_EC_2 import rush_hour_with_trucks2
from expanded_rush_hour_feat1ver1 import rush_hour_6x6_with_trucks
from check_6x6 import compare_6x6
from expanded_rush_hour_feat1ver2 import rush_hour_6x6_with_trucks2
from expanded_rush_hour_feat2ver1 import rush_hour_multistep_with_trucks
from check_multistep_actions import compare_multistep
from expanded_rush_hour_featsmergedver1 import rush_hour_6x6_multistep_with_trucks
from expanded_rush_hour_featsmergedver2 import rush_hour_6x6_multistep_with_trucks2

from planning import *
import time

def display_board(config):
    board = [['...' for _ in range(6)] for _ in range(6)]
    for name, data in config['cars'].items():
        x, y = data['pos']
        if 1 <= x <= 6 and 1 <= y <= 6:
            board[x-1][y-1] = (name[:2] if len(name) >= 2 else name[0]).ljust(3)
    for name, data in config['trucks'].items():
        (x1, y1), (x2, y2) = data['pos']
        display_name = (name[:2] if len(name) >= 2 else name[0]).ljust(3)
        if 1 <= x1 <= 6 and 1 <= y1 <= 6:
            board[x1-1][y1-1] = display_name
        if 1 <= x2 <= 6 and 1 <= y2 <= 6:
            board[x2-1][y2-1] = display_name
    for name, position in config['goal'].items():
        goal_name = f"G{name[:2] if len(name) >= 2 else name[0]}"
        if name in config['cars']:
            x, y = position
            if 1 <= x <= 6 and 1 <= y <= 6:
                board[x-1][y-1] = goal_name.ljust(3)
        else:
            (x1, y1), (x2, y2) = position
            if 1 <= x1 <= 6 and 1 <= y1 <= 6:
                board[x1-1][y1-1] = goal_name.ljust(3)
            if 1 <= x2 <= 6 and 1 <= y2 <= 6:
                board[x2-1][y2-1] = goal_name.ljust(3)
    print("\n    1   2   3   4   5   6")
    for i, row in enumerate(board):
        print(f"{i+1}  {' '.join(row)}")

def get_user_config():
    config = {'cars': {}, 'trucks': {}, 'goal': {}}
    occupied_positions = set()
    all_vehicle_names = set()
    goal_vehicles = set()
    
    #Car
    while True:
        #Get name
        name = input("Enter car name (or 'truck' to continue to trucks): ").strip().lower()
        if name == 'truck':
            break
        if name in all_vehicle_names:
            print(f"Error: Name '{name}' already used. Please choose a different name.")
            continue
        #Get position
        while True:
            x = int(input("\nX position: "))
            y = int(input("\nY position: "))
            if (x, y) in occupied_positions:
                print("Error: Position already occupied. Please choose a different position.")
            else:
                occupied_positions.add((x, y))
                break
        #Get direction
        while True:
            direction = input("\nDirection (h for Horizontal, v for Vertical): ").strip().lower()
            if direction == 'h':
                direction = 'Horizontal'
                break
            elif direction == 'v':
                direction = 'Vertical'
                break
            else:
                print("Error: Please enter 'h' or 'v'.")
        all_vehicle_names.add(name)
        config['cars'][name] = {'pos': (x, y), 'dir': direction}
    
    #Truck
    while True:
        #Get name
        name = input("\nEnter truck name (or 'goal' to continue to goal): ").strip().lower()
        if name == 'goal':
            break
        if name in all_vehicle_names:
            print(f"Error: Name '{name}' already used. Please choose a different name.")
            continue
        #Get positions
        while True:
            x1 = int(input("\nFirst cell X position: "))
            y1 = int(input("\nFirst cell Y position: "))
            x2 = int(input("\nSecond cell X position: "))
            y2 = int(input("\nSecond cell Y position: "))
            if (x1, y1) in occupied_positions or (x2, y2) in occupied_positions:
                print("Error: One or both positions already occupied. Please choose different positions.")
            elif (x1, y1) == (x2, y2):
                print("Error: Both positions are the same. Please choose different positions.")
            else:
                occupied_positions.add((x1, y1))
                occupied_positions.add((x2, y2))
                break
        #Get direction
        while True:
            direction = input("\nDirection (h for Horizontal, v for Vertical): ").strip().lower()
            if direction == 'h':
                direction = 'Horizontal'
                break
            elif direction == 'v':
                direction = 'Vertical'
                break
            else:
                print("Error: Please enter 'h' or 'v'.")
        all_vehicle_names.add(name)
        config['trucks'][name] = {'pos': ((x1, y1), (x2, y2)), 'dir': direction}
    
    #Goal
    while True:
        #Get Name
        name = input("\nEnter vehicle name for goal (or 'done' when done): ").strip().lower()
        if name == 'done':
            break
        if name not in all_vehicle_names:
            print(f"Error: Vehicle '{name}' not found. Please enter a valid vehicle name.")
            continue
        if name in goal_vehicles:
            print(f"Error: Goal for '{name}' already specified. Please choose a different vehicle.")
            continue
        if name in config['cars']:
            x = int(input("\nGoal X position: "))
            y = int(input("\nGoal Y position: "))
            config['goal'][name] = (x, y)
        else:
            x1 = int(input("\nFirst cell goal X position: "))
            y1 = int(input("\nFirst cell goal Y position: "))
            x2 = int(input("\nSecond cell goal X position: "))
            y2 = int(input("\nSecond cell goal Y position: "))
            if (x1, y1) == (x2, y2):
                print("Error: Both positions are the same. Please choose different positions.")
            else:
                config['goal'][name] = ((x1, y1), (x2, y2))
        goal_vehicles.add(name)
    
    # Display board and confirm
    display_board(config)
    confirm = input("\nIs this configuration correct? (y/n): ").strip().lower()
    if confirm == 'y':
        return config
    else:
        print("\nRestarting configuration...\n")
        return get_user_config()


if __name__ == "__main__":
    
    print("Current Problem Representations Available (in order of production): 'EX1', 'EX2', '6x61', 'compare6x6', '6x62', 'multistep', 'compareMultistep', '6x6multistep', '6x6multistep2'")
    problem = input("Enter a problem representation from above to try GraphPlan on (or compare sample answers against original assignment's problem representation) or press q to quit: ")
    while problem != "q" and problem != "EX1" and problem != "EX2" and problem != "6x61" and problem != "compare6x6" and problem != "6x62" and problem != "multistep" and problem != "compareMultistep" and problem != "6x6multistep" and problem != "6x6multistep2":
        problem = input("Please enter a valid problem representation or press q to quit: ")
    
    if problem == "q":
        print("Terminated program")
    elif problem == "compare6x6":
        compare_6x6()
    elif problem == "compareMultistep":
        compare_multistep()
    elif problem == "EX1":
        print("THIS REQUIRES YOUR PROBLEM TO BE LIMITED TO A 4X4 GRID")
        config = get_user_config()
        p = rush_hour_with_trucks1(config=config)
    elif problem == "EX2":
        print("THIS REQUIRES YOUR PROBLEM TO BE LIMITED TO A 4X4 GRID")
        config = get_user_config()
        p = rush_hour_with_trucks2(config=config)
    elif problem == "6x61":
        config = get_user_config()
        p = rush_hour_6x6_with_trucks(config=config)
    elif problem == "6x62":
        config = get_user_config()
        p = rush_hour_6x6_with_trucks2(config=config)
    elif problem == "multistep":
        print("THIS REQUIRES YOUR PROBLEM TO BE LIMITED TO A 4X4 GRID")
        config = get_user_config()
        p = rush_hour_multistep_with_trucks(config=config)
    elif problem == "6x6multistep":
        config = get_user_config()
        p = rush_hour_6x6_multistep_with_trucks(config=config)
    elif problem == "6x6multistep2":
        config = get_user_config()
        p = rush_hour_6x6_multistep_with_trucks2(config=config)

    if problem not in ["q", "compare6x6", "compareMultistep"]:
        start = time.time()
        start2 = time.process_time()
        g = GraphPlan(p).execute()
        l = Linearize(p).execute()
        end = time.time()
        end2 = time.process_time()
        print(f"Elapsed Wall time: {end-start} seconds")
        print(f"Elapsed CPU time: {end2-start2} seconds")
        print(g[0], l)