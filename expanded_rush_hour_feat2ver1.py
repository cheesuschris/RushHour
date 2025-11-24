#--------------------------------------------------------------------------------------------------------


#SECOND FEATURE VER. 1: MANUALLY ADDING MULTI-STEP ACTIONS W/O POST-PROCESSING SLIDING OR DYNAMICALLY CALCULATING HOW FAR TO SLIDE
#This representation took a decently long time to solve for Graphplan
#Took 822.6485 seconds to find a valid plan - 11.5X slower than same problem w/ a normal actionset
#No 6x6 grid implementation yet
#No runner for any configuration yet

#From here, the partially ordered and linearized plan returns from example_EC_1 and this file shows that the preconditions, actions, 
#and finalized plans required between the same problem on a multistep action set is a good amount less (but still correct) than on a 
#normal action set (highlighted in check_multistep_actions.py). While the overall action (path) cost with this multistep-action 
#feature is less, it similarly significantly expands the search tree similarly to how a 6x6 grid does; this is due to the extreme many times
#more actions now available at each step. 
#There are two things I'm concerned about with this implementation:
# - I'm worried that the returned solution won't always slide as far as possible, or isn't at max efficiency (how does GraphPlan choose w/o a heuristic?)
#  --> [ANSWERED] Upon further thought I realize BFS will always reach the shortest action plan first, so it will always choose correct multi-action step
# - I'm worried that for hard-coding multi-step actions for the 6x6 grid (there'll be way more than the ones here), the actions will explode the search tree.
#  --> [ANSWERED] This DOES explode the search tree in the merged version, I needed to debug this using PDDL and choose a better representation.
#For now, I'll accept this OK runtime and attempt merging this feature with the 6x6 grid feature. However, if this computationally
#starts exploding the merged search tree (it did; see ANSWERED #2), I might try dynamic sliding or post-processing sliding (suggested by LLM) 
#in future merged versions.


#--------------------------------------------------------------------------------------------------------

from planning import *
from logic import *

def rush_hour_multistep_with_trucks(config):
    """
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

    # --- Deconstructing input ---

    init_cars = config['cars']
    init_trucks = config['trucks']
    init_goals = config['goal']

    # --- Filling out required PlanningProblem data ---

    initial = []
    goals = []
    domain = []

    cells = {f'C{r}_{c}' for r in range(1, 5) for c in range(1, 5)}

    for car, car_info in init_cars.items():
        car_cell = f'C{car_info["pos"][0]}_{car_info["pos"][1]}'
        car_dir = car_info['dir']
        domain.append(f'Car({car})')
        initial.append(f'At({car}, {car_cell})')
        initial.append(f'{car_dir}({car})')
        cells.discard(car_cell)
    
    for truck, truck_info in init_trucks.items():
        truck_cells = [f'C{truck_info["pos"][0][0]}_{truck_info["pos"][0][1]}', f'C{truck_info["pos"][1][0]}_{truck_info["pos"][1][1]}']
        truck_dir = truck_info['dir']
        domain.append(f'Truck({truck})')
        initial.append(f'Occupies({truck}, {truck_cells[0]})')
        initial.append(f'Occupies({truck}, {truck_cells[1]})')
        initial.append(f'{truck_dir}({truck})')
        cells.discard(truck_cells[0])
        cells.discard(truck_cells[1])
    
    initial.extend([f'Clear({cell})' for cell in sorted(cells)])

    for vehicle, goal in init_goals.items():
        if vehicle in init_cars:
            goals.append(f'At({vehicle}, C{goal[0]}_{goal[1]})')
        elif vehicle in init_trucks:
            goals.append(f'Occupies({vehicle}, C{goal[0][0]}_{goal[0][1]})')
            goals.append(f'Occupies({vehicle}, C{goal[1][0]}_{goal[1][1]})')

    initial = ' & '.join(initial)
    goals = ' & '.join(goals)
    domain = ' & '.join(domain)

    # ---  Returning filled out & desired data ---

    return PlanningProblem(
        initial=expr(initial),
        goals=expr(goals),
        actions=[
            # --- Horizontal moves ---
            Action('CarMoveRight(c, frm, to)',
                precond=expr('At(c, frm) & Clear(to) & Horizontal(c) & AdjacentRight(frm, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentRight(frm, to)')),
            Action('CarMoveRightTwo(c, frm, between, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Horizontal(c) & AdjacentRight(frm, between) & AdjacentRight(between, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(to) & AdjacentRight(frm, between) & AdjacentRight(between, to)')),
            Action('CarMoveRightThree(c, frm, between, between2, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Horizontal(c) & AdjacentRight(frm, between) & AdjacentRight(between, between2) & AdjacentRight(between2, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(to) & AdjacentRight(frm, between) & AdjacentRight(between, between2) & AdjacentRight(between2, to)')),
            Action('CarMoveLeft(c, frm, to)',
                precond=expr('At(c, frm) & Clear(to) & Horizontal(c) & AdjacentLeft(frm, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentLeft(frm, to)')),
            Action('CarMoveLeftTwo(c, frm, between, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Horizontal(c) & AdjacentLeft(frm, between) & AdjacentLeft(between, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(to) & AdjacentLeft(frm, between) & AdjacentLeft(between, to)')),
            Action('CarMoveLeftThree(c, frm, between, between2, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Horizontal(c) & AdjacentLeft(frm, between) & AdjacentLeft(between, between2) & AdjacentLeft(between2, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(to) & AdjacentLeft(frm, between) & AdjacentLeft(between, between2) & AdjacentLeft(between2, to)')),
            Action('TruckMoveRight(t, t_head, t_tail, to)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to) & Horizontal(t) & AdjacentRight(t_tail, t_head) & AdjacentRight(t_head, to)'),
                    effect=expr('~Clear(to) & Occupies(t, to) & Clear(t_tail) & ~Occupies(t, t_tail)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to)')),
            Action('TruckMoveRightTwo(t, t_head, t_tail, to_head, to_tail)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to_head) & Clear(to_tail) & Horizontal(t) & AdjacentRight(t_tail, t_head) & AdjacentRight(t_head, to_tail) & AdjacentRight(to_tail, to_head)'),
                    effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveLeft(t, t_head, t_tail, to)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to) & Horizontal(t) & AdjacentLeft(t_head, t_tail) & AdjacentLeft(t_tail, to)'),
                    effect=expr('~Clear(to) & Occupies(t, to) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to)')),
            Action('TruckMoveLeftTwo(t, t_head, t_tail, to_head, to_tail)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to_head) & Clear(to_tail) & Horizontal(t) & AdjacentLeft(t_head, t_tail) & AdjacentLeft(t_tail, to_head) & AdjacentLeft(to_head, to_tail)'),
                    effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to_head) & Cell(to_tail)')),
            # --- Vertical moves ---
            Action('CarMoveUp(c, frm, to)',
                precond=expr('At(c, frm) & Clear(to) & Vertical(c) & AdjacentUp(frm, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentUp(frm, to)')),
            Action('CarMoveUpTwo(c, frm, between, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Vertical(c) & AdjacentUp(frm, between) & AdjacentUp(between, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(to) & AdjacentUp(frm, between) & AdjacentUp(between, to)')),
            Action('CarMoveUpThree(c, frm, between, between2, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Vertical(c) & AdjacentUp(frm, between) & AdjacentUp(between, between2) & AdjacentUp(between2, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(to) & AdjacentUp(frm, between) & AdjacentUp(between, between2) & AdjacentUp(between2, to)')),
            Action('CarMoveDown(c, frm, to)',
                precond=expr('At(c, frm) & Clear(to) & Vertical(c) & AdjacentDown(frm, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentDown(frm, to)')),
            Action('CarMoveDownTwo(c, frm, between, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Vertical(c) & AdjacentDown(frm, between) & AdjacentDown(between, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(to) & AdjacentDown(frm, between) & AdjacentDown(between, to)')),
            Action('CarMoveDownThree(c, frm, between, between2, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Vertical(c) & AdjacentDown(frm, between) & AdjacentDown(between, between2) & AdjacentDown(between2, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(to) & AdjacentDown(frm, between) & AdjacentDown(between, between2) & AdjacentDown(between2, to)')),
            Action('TruckMoveUp(t, t_head, t_tail, to)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to) & Vertical(t) & AdjacentUp(t_head, t_tail) & AdjacentUp(t_tail, to)'),
                   effect=expr('Occupies(t, t_tail) & ~Clear(to) & Occupies(t, to) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to)')),
            Action('TruckMoveUpTwo(t, t_head, t_tail, to_head, to_tail)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to_head) & Clear(to_tail) & Vertical(t) & AdjacentUp(t_head, t_tail) & AdjacentUp(t_tail, to_head) & AdjacentUp(to_head, to_tail)'),
                   effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveDown(t, t_head, t_tail, to)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to) & Vertical(t) & AdjacentDown(t_tail, t_head) & AdjacentDown(t_head, to)'),
                   effect=expr('Occupies(t, t_head) & ~Clear(to) & Occupies(t, to) & Clear(t_tail) & ~Occupies(t, t_tail)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to)')),
            Action('TruckMoveDownTwo(t, t_head, t_tail, to_head, to_tail)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to_head) & Clear(to_tail) & Vertical(t) & AdjacentDown(t_tail, t_head) & AdjacentDown(t_head, to_tail) & AdjacentDown(to_tail, to_head)'),
                   effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to_head) & Cell(to_tail)')),
        ],
        domain=expr(
            # --- Car & Truck definitions ---
            domain + ' & '
            # --- Cell definitions ---
            'Cell(C1_1) & Cell(C1_2) & Cell(C1_3) & Cell(C1_4) & '
            'Cell(C2_1) & Cell(C2_2) & Cell(C2_3) & Cell(C2_4) & '
            'Cell(C3_1) & Cell(C3_2) & Cell(C3_3) & Cell(C3_4) & '
            'Cell(C4_1) & Cell(C4_2) & Cell(C4_3) & Cell(C4_4) & '
            # --- Adjacency (complete, propositional) ---
            'AdjacentRight(C1_1, C1_2) & AdjacentRight(C1_2, C1_3) & AdjacentRight(C1_3, C1_4) & '
            'AdjacentRight(C2_1, C2_2) & AdjacentRight(C2_2, C2_3) & AdjacentRight(C2_3, C2_4) & '
            'AdjacentRight(C3_1, C3_2) & AdjacentRight(C3_2, C3_3) & AdjacentRight(C3_3, C3_4) & '
            'AdjacentRight(C4_1, C4_2) & AdjacentRight(C4_2, C4_3) & AdjacentRight(C4_3, C4_4) & '
            'AdjacentLeft(C1_2, C1_1) & AdjacentLeft(C1_3, C1_2) & AdjacentLeft(C1_4, C1_3) & '
            'AdjacentLeft(C2_2, C2_1) & AdjacentLeft(C2_3, C2_2) & AdjacentLeft(C2_4, C2_3) & '
            'AdjacentLeft(C3_2, C3_1) & AdjacentLeft(C3_3, C3_2) & AdjacentLeft(C3_4, C3_3) & '
            'AdjacentLeft(C4_2, C4_1) & AdjacentLeft(C4_3, C4_2) & AdjacentLeft(C4_4, C4_3) & '
            'AdjacentDown(C1_1, C2_1) & AdjacentDown(C2_1, C3_1) & AdjacentDown(C3_1, C4_1) & '
            'AdjacentDown(C1_2, C2_2) & AdjacentDown(C2_2, C3_2) & AdjacentDown(C3_2, C4_2) & '
            'AdjacentDown(C1_3, C2_3) & AdjacentDown(C2_3, C3_3) & AdjacentDown(C3_3, C4_3) & '
            'AdjacentDown(C1_4, C2_4) & AdjacentDown(C2_4, C3_4) & AdjacentDown(C3_4, C4_4) & '
            'AdjacentUp(C2_1, C1_1) & AdjacentUp(C3_1, C2_1) & AdjacentUp(C4_1, C3_1) & '
            'AdjacentUp(C2_2, C1_2) & AdjacentUp(C3_2, C2_2) & AdjacentUp(C4_2, C3_2) & '
            'AdjacentUp(C2_3, C1_3) & AdjacentUp(C3_3, C2_3) & AdjacentUp(C4_3, C3_3) & '
            'AdjacentUp(C2_4, C1_4) & AdjacentUp(C3_4, C2_4) & AdjacentUp(C4_4, C3_4)'
        )
    )