#--------------------------------------------------------------------------------------------------------


#MERGED FEATURES VER. 3: IMPLEMENTING PDDL-FOUND OPTIMIZATIONS w/ featsmerged_domainver3 & featsmerged_problemver2
#This version implements the optimized PDDL logic with EXPLICIT MULTI-STEP ACTIONS:
#MANUALLY DEFINED multi-step actions (Move 1-5 for Cars, Move 1-4 for Trucks) matching the accompanying PDDL domain file exactly.
#Could NOT find a valid plan, terminated similar to featsmergedver1.py.
#No runner for any configuration yet

#From here, I think I will stick with post-processing (still solves the multi-step action problem). I still need
#to create a driver file to run any problem representation. This is addressed in expanded_rush_hour_driver.py


#--------------------------------------------------------------------------------------------------------

from planning import *
from logic import *

def rush_hour_6x6_multistep_with_trucks3(config):
    """
    Problem modifications (Optimized Version based on PDDL Ver. 2):
    - Supports configuration for any valid rush_hour setup.
    - The board is 6x6.
    - Uses a factored state representation (rows and columns) instead of propositional cells.
    - Uses single-step actions only, relying on the planner to chain them.
    - This maps to the PDDL domain/problem ver. 2.
    - Ex input:
        ```
        config = {
            'cars': {
                'R': {'pos': (3, 1), 'dir': 'Horizontal'},   # Red car
                'A': {'pos': (1, 1), 'dir': 'Horizontal'},   # Car A
                'B': {'pos': (4, 3), 'dir': 'Vertical'}      # Car B
            },
            'trucks': {
                'T1': {'pos': ((3, 2), (4, 2)), 'dir': 'Vertical'},  # Truck T1
                'T2': {'pos': ((2, 3), (3, 3)), 'dir': 'Vertical'}     # Truck T2
            },
            'goal': {
                'R': (3, 6),                                 # Red car must reach (r3, c6)
                'T1': ((1, 2), (2, 2))                       # Truck T1 must reach (r1, c2), (r2, c2)
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

    rows = [f'r{i}' for i in range(1, 7)]
    cols = [f'c{i}' for i in range(1, 7)]
    domain.extend([f'Row({r})' for r in rows])
    domain.extend([f'Col({c})' for c in cols])

    for i in range(1, 6):
        initial.append(f'NextRow(r{i}, r{i+1})')
        initial.append(f'NextCol(c{i}, c{i+1})')
    clear_cells = {(r, c) for r in range(1, 7) for c in range(1, 7)}

    for car, car_info in init_cars.items():
        r, c = car_info['pos']
        car_row = f'r{r}'
        car_col = f'c{c}'
        car_dir = car_info['dir']
        domain.append(f'Car({car})')
        if car_dir == 'Horizontal':
            initial.append(f'AtHorizontal({car}, {car_row}, {car_col})')
        else:
            initial.append(f'AtVertical({car}, {car_row}, {car_col})')
        clear_cells.discard((r, c))
    
    for truck, truck_info in init_trucks.items():
        pos1, pos2 = truck_info['pos']
        r1, c1 = pos1
        r2, c2 = pos2
        truck_dir = truck_info['dir']
        domain.append(f'Truck({truck})')
        if truck_dir == 'Horizontal':
            initial.append(f'AtHorizontal({truck}, r{r1}, c{c1})')
            initial.append(f'AtHorizontal({truck}, r{r2}, c{c2})')
        elif truck_dir == 'Vertical':
            initial.append(f'AtVertical({truck}, r{r1}, c{c1})')
            initial.append(f'AtVertical({truck}, r{r2}, c{c2})')
        clear_cells.discard((r1, c1))
        clear_cells.discard((r2, c2))
    
    for r, c in sorted(clear_cells):
        initial.append(f'Clear(r{r}, c{c})')

    for vehicle, goal_data in init_goals.items():
        if vehicle in init_cars:
            r, c = goal_data
            if init_cars[vehicle]['dir'] == 'Horizontal':
                 goals.append(f'AtHorizontal({vehicle}, r{r}, c{c})')
            else: 
                 goals.append(f'AtVertical({vehicle}, r{r}, c{c})')
        elif vehicle in init_trucks:
            pos1, pos2 = goal_data
            r1, c1 = pos1
            r2, c2 = pos2
            if init_trucks[vehicle]['dir'] == 'Horizontal':
                goals.append(f'AtHorizontal({vehicle}, r{r1}, c{c1})')
                goals.append(f'AtHorizontal({vehicle}, r{r2}, c{c2})')
            else:
                goals.append(f'AtVertical({vehicle}, r{r1}, c{c1})')
                goals.append(f'AtVertical({vehicle}, r{r2}, c{c2})')

    initial = ' & '.join(initial)
    goals = ' & '.join(goals)
    domain_str = ' & '.join(domain)

    # --- Returning filled out & desired data ---

    return PlanningProblem(
        initial=expr(initial),
        goals=expr(goals),
        actions=[
            # --- Horizontal moves ---
            Action('CarMoveRight1(c, r, p1, p2)',
                precond=expr('AtHorizontal(c, r, p1) & NextCol(p1, p2) & Clear(r, p2)'),
                effect=expr('~AtHorizontal(c, r, p1) & AtHorizontal(c, r, p2) & Clear(r, p1) & ~Clear(r, p2)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2)')),
            Action('CarMoveRight2(c, r, p1, p2, p3)',
                precond=expr('AtHorizontal(c, r, p1) & NextCol(p1, p2) & NextCol(p2, p3) & Clear(r, p2) & Clear(r, p3)'),
                effect=expr('~AtHorizontal(c, r, p1) & AtHorizontal(c, r, p3) & Clear(r, p1) & ~Clear(r, p3)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2) & Col(p3)')),
            Action('CarMoveRight3(c, r, p1, p2, p3, p4)',
                precond=expr('AtHorizontal(c, r, p1) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & Clear(r, p2) & Clear(r, p3) & Clear(r, p4)'),
                effect=expr('~AtHorizontal(c, r, p1) & AtHorizontal(c, r, p4) & Clear(r, p1) & ~Clear(r, p4)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4)')),
            Action('CarMoveRight4(c, r, p1, p2, p3, p4, p5)',
                precond=expr('AtHorizontal(c, r, p1) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & NextCol(p4, p5) & Clear(r, p2) & Clear(r, p3) & Clear(r, p4) & Clear(r, p5)'),
                effect=expr('~AtHorizontal(c, r, p1) & AtHorizontal(c, r, p5) & Clear(r, p1) & ~Clear(r, p5)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4) & Col(p5)')),
            Action('CarMoveRight5(c, r, p1, p2, p3, p4, p5, p6)',
                precond=expr('AtHorizontal(c, r, p1) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & NextCol(p4, p5) & NextCol(p5, p6) & Clear(r, p2) & Clear(r, p3) & Clear(r, p4) & Clear(r, p5) & Clear(r, p6)'),
                effect=expr('~AtHorizontal(c, r, p1) & AtHorizontal(c, r, p6) & Clear(r, p1) & ~Clear(r, p6)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4) & Col(p5) & Col(p6)')),
            Action('CarMoveLeft1(c, r, p1, p2)',
                precond=expr('AtHorizontal(c, r, p2) & NextCol(p1, p2) & Clear(r, p1)'),
                effect=expr('~AtHorizontal(c, r, p2) & AtHorizontal(c, r, p1) & Clear(r, p2) & ~Clear(r, p1)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2)')),
            Action('CarMoveLeft2(c, r, p1, p2, p3)',
                precond=expr('AtHorizontal(c, r, p3) & NextCol(p1, p2) & NextCol(p2, p3) & Clear(r, p2) & Clear(r, p1)'),
                effect=expr('~AtHorizontal(c, r, p3) & AtHorizontal(c, r, p1) & Clear(r, p3) & ~Clear(r, p1)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2) & Col(p3)')),
            Action('CarMoveLeft3(c, r, p1, p2, p3, p4)',
                precond=expr('AtHorizontal(c, r, p4) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & Clear(r, p3) & Clear(r, p2) & Clear(r, p1)'),
                effect=expr('~AtHorizontal(c, r, p4) & AtHorizontal(c, r, p1) & Clear(r, p4) & ~Clear(r, p1)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4)')),
            Action('CarMoveLeft4(c, r, p1, p2, p3, p4, p5)',
                precond=expr('AtHorizontal(c, r, p5) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & NextCol(p4, p5) & Clear(r, p4) & Clear(r, p3) & Clear(r, p2) & Clear(r, p1)'),
                effect=expr('~AtHorizontal(c, r, p5) & AtHorizontal(c, r, p1) & Clear(r, p5) & ~Clear(r, p1)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4) & Col(p5)')),
            Action('CarMoveLeft5(c, r, p1, p2, p3, p4, p5, p6)',
                precond=expr('AtHorizontal(c, r, p6) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & NextCol(p4, p5) & NextCol(p5, p6) & Clear(r, p5) & Clear(r, p4) & Clear(r, p3) & Clear(r, p2) & Clear(r, p1)'),
                effect=expr('~AtHorizontal(c, r, p6) & AtHorizontal(c, r, p1) & Clear(r, p6) & ~Clear(r, p1)'),
                domain=expr('Car(c) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4) & Col(p5) & Col(p6)')),
            Action('TruckMoveRight1(t, r, p1, p2, p3)',
                precond=expr('AtHorizontal(t, r, p1) & AtHorizontal(t, r, p2) & NextCol(p1, p2) & NextCol(p2, p3) & Clear(r, p3)'),
                effect=expr('~AtHorizontal(t, r, p1) & AtHorizontal(t, r, p3) & Clear(r, p1) & ~Clear(r, p3)'),
                domain=expr('Truck(t) & Row(r) & Col(p1) & Col(p2) & Col(p3)')),
            Action('TruckMoveRight2(t, r, p1, p2, p3, p4)',
                precond=expr('AtHorizontal(t, r, p1) & AtHorizontal(t, r, p2) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & Clear(r, p3) & Clear(r, p4)'),
                effect=expr('~AtHorizontal(t, r, p1) & ~AtHorizontal(t, r, p2) & AtHorizontal(t, r, p3) & AtHorizontal(t, r, p4) & Clear(r, p1) & Clear(r, p2) & ~Clear(r, p3) & ~Clear(r, p4)'),
                domain=expr('Truck(t) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4)')),
            Action('TruckMoveRight3(t, r, p1, p2, p3, p4, p5)',
                precond=expr('AtHorizontal(t, r, p1) & AtHorizontal(t, r, p2) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & NextCol(p4, p5) & Clear(r, p3) & Clear(r, p4) & Clear(r, p5)'),
                effect=expr('~AtHorizontal(t, r, p1) & ~AtHorizontal(t, r, p2) & AtHorizontal(t, r, p4) & AtHorizontal(t, r, p5) & Clear(r, p1) & Clear(r, p2) & ~Clear(r, p4) & ~Clear(r, p5)'),
                domain=expr('Truck(t) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4) & Col(p5)')),
            Action('TruckMoveRight4(t, r, p1, p2, p3, p4, p5, p6)',
                precond=expr('AtHorizontal(t, r, p1) & AtHorizontal(t, r, p2) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & NextCol(p4, p5) & NextCol(p5, p6) & Clear(r, p3) & Clear(r, p4) & Clear(r, p5) & Clear(r, p6)'),
                effect=expr('~AtHorizontal(t, r, p1) & ~AtHorizontal(t, r, p2) & AtHorizontal(t, r, p5) & AtHorizontal(t, r, p6) & Clear(r, p1) & Clear(r, p2) & ~Clear(r, p5) & ~Clear(r, p6)'),
                domain=expr('Truck(t) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4) & Col(p5) & Col(p6)')),
            Action('TruckMoveLeft1(t, r, p1, p2, p3)',
                precond=expr('AtHorizontal(t, r, p2) & AtHorizontal(t, r, p3) & NextCol(p1, p2) & NextCol(p2, p3) & Clear(r, p1)'),
                effect=expr('~AtHorizontal(t, r, p3) & AtHorizontal(t, r, p1) & Clear(r, p3) & ~Clear(r, p1)'),
                domain=expr('Truck(t) & Row(r) & Col(p1) & Col(p2) & Col(p3)')),
            Action('TruckMoveLeft2(t, r, p1, p2, p3, p4)',
                precond=expr('AtHorizontal(t, r, p3) & AtHorizontal(t, r, p4) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & Clear(r, p1) & Clear(r, p2)'),
                effect=expr('~AtHorizontal(t, r, p3) & ~AtHorizontal(t, r, p4) & AtHorizontal(t, r, p1) & AtHorizontal(t, r, p2) & Clear(r, p3) & Clear(r, p4) & ~Clear(r, p1) & ~Clear(r, p2)'),
                domain=expr('Truck(t) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4)')),
            Action('TruckMoveLeft3(t, r, p1, p2, p3, p4, p5)',
                precond=expr('AtHorizontal(t, r, p4) & AtHorizontal(t, r, p5) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & NextCol(p4, p5) & Clear(r, p1) & Clear(r, p2) & Clear(r, p3)'),
                effect=expr('~AtHorizontal(t, r, p4) & ~AtHorizontal(t, r, p5) & AtHorizontal(t, r, p1) & AtHorizontal(t, r, p2) & Clear(r, p4) & Clear(r, p5) & ~Clear(r, p1) & ~Clear(r, p2)'),
                domain=expr('Truck(t) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4) & Col(p5)')),
            Action('TruckMoveLeft4(t, r, p1, p2, p3, p4, p5, p6)',
                precond=expr('AtHorizontal(t, r, p5) & AtHorizontal(t, r, p6) & NextCol(p1, p2) & NextCol(p2, p3) & NextCol(p3, p4) & NextCol(p4, p5) & NextCol(p5, p6) & Clear(r, p1) & Clear(r, p2) & Clear(r, p3) & Clear(r, p4)'),
                effect=expr('~AtHorizontal(t, r, p5) & ~AtHorizontal(t, r, p6) & AtHorizontal(t, r, p1) & AtHorizontal(t, r, p2) & Clear(r, p5) & Clear(r, p6) & ~Clear(r, p1) & ~Clear(r, p2)'),
                domain=expr('Truck(t) & Row(r) & Col(p1) & Col(p2) & Col(p3) & Col(p4) & Col(p5) & Col(p6)')),
            
            # --- Vertical moves ---
            Action('CarMoveDown1(c, c1, p1, p2)',
                precond=expr('AtVertical(c, p1, c1) & NextRow(p1, p2) & Clear(p2, c1)'),
                effect=expr('~AtVertical(c, p1, c1) & AtVertical(c, p2, c1) & Clear(p1, c1) & ~Clear(p2, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2)')),
            Action('CarMoveDown2(c, c1, p1, p2, p3)',
                precond=expr('AtVertical(c, p1, c1) & NextRow(p1, p2) & NextRow(p2, p3) & Clear(p2, c1) & Clear(p3, c1)'),
                effect=expr('~AtVertical(c, p1, c1) & AtVertical(c, p3, c1) & Clear(p1, c1) & ~Clear(p3, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2) & Row(p3)')),
            Action('CarMoveDown3(c, c1, p1, p2, p3, p4)',
                precond=expr('AtVertical(c, p1, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & Clear(p2, c1) & Clear(p3, c1) & Clear(p4, c1)'),
                effect=expr('~AtVertical(c, p1, c1) & AtVertical(c, p4, c1) & Clear(p1, c1) & ~Clear(p4, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4)')),
            Action('CarMoveDown4(c, c1, p1, p2, p3, p4, p5)',
                precond=expr('AtVertical(c, p1, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & NextRow(p4, p5) & Clear(p2, c1) & Clear(p3, c1) & Clear(p4, c1) & Clear(p5, c1)'),
                effect=expr('~AtVertical(c, p1, c1) & AtVertical(c, p5, c1) & Clear(p1, c1) & ~Clear(p5, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4) & Row(p5)')),
            Action('CarMoveDown5(c, c1, p1, p2, p3, p4, p5, p6)',
                precond=expr('AtVertical(c, p1, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & NextRow(p4, p5) & NextRow(p5, p6) & Clear(p2, c1) & Clear(p3, c1) & Clear(p4, c1) & Clear(p5, c1) & Clear(p6, c1)'),
                effect=expr('~AtVertical(c, p1, c1) & AtVertical(c, p6, c1) & Clear(p1, c1) & ~Clear(p6, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4) & Row(p5) & Row(p6)')),
            Action('CarMoveUp1(c, c1, p1, p2)',
                precond=expr('AtVertical(c, p2, c1) & NextRow(p1, p2) & Clear(p1, c1)'),
                effect=expr('~AtVertical(c, p2, c1) & AtVertical(c, p1, c1) & Clear(p2, c1) & ~Clear(p1, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2)')),
            Action('CarMoveUp2(c, c1, p1, p2, p3)',
                precond=expr('AtVertical(c, p3, c1) & NextRow(p1, p2) & NextRow(p2, p3) & Clear(p2, c1) & Clear(p1, c1)'),
                effect=expr('~AtVertical(c, p3, c1) & AtVertical(c, p1, c1) & Clear(p3, c1) & ~Clear(p1, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2) & Row(p3)')),
            Action('CarMoveUp3(c, c1, p1, p2, p3, p4)',
                precond=expr('AtVertical(c, p4, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & Clear(p3, c1) & Clear(p2, c1) & Clear(p1, c1)'),
                effect=expr('~AtVertical(c, p4, c1) & AtVertical(c, p1, c1) & Clear(p4, c1) & ~Clear(p1, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4)')),
            Action('CarMoveUp4(c, c1, p1, p2, p3, p4, p5)',
                precond=expr('AtVertical(c, p5, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & NextRow(p4, p5) & Clear(p4, c1) & Clear(p3, c1) & Clear(p2, c1) & Clear(p1, c1)'),
                effect=expr('~AtVertical(c, p5, c1) & AtVertical(c, p1, c1) & Clear(p5, c1) & ~Clear(p1, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4) & Row(p5)')),
            Action('CarMoveUp5(c, c1, p1, p2, p3, p4, p5, p6)',
                precond=expr('AtVertical(c, p6, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & NextRow(p4, p5) & NextRow(p5, p6) & Clear(p5, c1) & Clear(p4, c1) & Clear(p3, c1) & Clear(p2, c1) & Clear(p1, c1)'),
                effect=expr('~AtVertical(c, p6, c1) & AtVertical(c, p1, c1) & Clear(p6, c1) & ~Clear(p1, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4) & Row(p5) & Row(p6)')),
            Action('TruckMoveDown1(t, c1, p1, p2, p3)',
                precond=expr('AtVertical(t, p1, c1) & AtVertical(t, p2, c1) & NextRow(p1, p2) & NextRow(p2, p3) & Clear(p3, c1)'),
                effect=expr('~AtVertical(t, p1, c1) & AtVertical(t, p3, c1) & Clear(p1, c1) & ~Clear(p3, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(p1) & Row(p2) & Row(p3)')),
            Action('TruckMoveDown2(t, c1, p1, p2, p3, p4)',
                precond=expr('AtVertical(t, p1, c1) & AtVertical(t, p2, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & Clear(p3, c1) & Clear(p4, c1)'),
                effect=expr('~AtVertical(t, p1, c1) & ~AtVertical(t, p2, c1) & AtVertical(t, p3, c1) & AtVertical(t, p4, c1) & Clear(p1, c1) & Clear(p2, c1) & ~Clear(p3, c1) & ~Clear(p4, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4)')),
            Action('TruckMoveDown3(t, c1, p1, p2, p3, p4, p5)',
                precond=expr('AtVertical(t, p1, c1) & AtVertical(t, p2, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & NextRow(p4, p5) & Clear(p3, c1) & Clear(p4, c1) & Clear(p5, c1)'),
                effect=expr('~AtVertical(t, p1, c1) & ~AtVertical(t, p2, c1) & AtVertical(t, p4, c1) & AtVertical(t, p5, c1) & Clear(p1, c1) & Clear(p2, c1) & ~Clear(p4, c1) & ~Clear(p5, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4) & Row(p5)')),
            Action('TruckMoveDown4(t, c1, p1, p2, p3, p4, p5, p6)',
                precond=expr('AtVertical(t, p1, c1) & AtVertical(t, p2, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & NextRow(p4, p5) & NextRow(p5, p6) & Clear(p3, c1) & Clear(p4, c1) & Clear(p5, c1) & Clear(p6, c1)'),
                effect=expr('~AtVertical(t, p1, c1) & ~AtVertical(t, p2, c1) & AtVertical(t, p5, c1) & AtVertical(t, p6, c1) & Clear(p1, c1) & Clear(p2, c1) & ~Clear(p5, c1) & ~Clear(p6, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4) & Row(p5) & Row(p6)')),
            Action('TruckMoveUp1(t, c1, p1, p2, p3)',
                precond=expr('AtVertical(t, p2, c1) & AtVertical(t, p3, c1) & NextRow(p1, p2) & NextRow(p2, p3) & Clear(p1, c1)'),
                effect=expr('~AtVertical(t, p3, c1) & AtVertical(t, p1, c1) & Clear(p3, c1) & ~Clear(p1, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(p1) & Row(p2) & Row(p3)')),
            Action('TruckMoveUp2(t, c1, p1, p2, p3, p4)',
                precond=expr('AtVertical(t, p3, c1) & AtVertical(t, p4, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & Clear(p1, c1) & Clear(p2, c1)'),
                effect=expr('~AtVertical(t, p3, c1) & ~AtVertical(t, p4, c1) & AtVertical(t, p1, c1) & AtVertical(t, p2, c1) & Clear(p3, c1) & Clear(p4, c1) & ~Clear(p1, c1) & ~Clear(p2, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4)')),
            Action('TruckMoveUp3(t, c1, p1, p2, p3, p4, p5)',
                precond=expr('AtVertical(t, p4, c1) & AtVertical(t, p5, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & NextRow(p4, p5) & Clear(p1, c1) & Clear(p2, c1) & Clear(p3, c1)'),
                effect=expr('~AtVertical(t, p4, c1) & ~AtVertical(t, p5, c1) & AtVertical(t, p1, c1) & AtVertical(t, p2, c1) & Clear(p4, c1) & Clear(p5, c1) & ~Clear(p1, c1) & ~Clear(p2, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4) & Row(p5)')),
            Action('TruckMoveUp4(t, c1, p1, p2, p3, p4, p5, p6)',
                precond=expr('AtVertical(t, p5, c1) & AtVertical(t, p6, c1) & NextRow(p1, p2) & NextRow(p2, p3) & NextRow(p3, p4) & NextRow(p4, p5) & NextRow(p5, p6) & Clear(p1, c1) & Clear(p2, c1) & Clear(p3, c1) & Clear(p4, c1)'),
                effect=expr('~AtVertical(t, p5, c1) & ~AtVertical(t, p6, c1) & AtVertical(t, p1, c1) & AtVertical(t, p2, c1) & Clear(p5, c1) & Clear(p6, c1) & ~Clear(p1, c1) & ~Clear(p2, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(p1) & Row(p2) & Row(p3) & Row(p4) & Row(p5) & Row(p6)'))
        ],
        domain=expr(domain_str)
    )