#--------------------------------------------------------------------------------------------------------


#MERGED FEATURES VER. 2: IMPLEMENTING PDDL-FOUND OPTIMIZATIONS w/ featsmerged_domainver2 & featsmerged_problemver2
#This version implements the optimized PDDL logic:
# 1. States: Uses 'Row' and 'Col' objects (r1, c1) instead of
#    a single propositional 'Cell(C1_1)'.
# 2. Predicates: Uses 'NextRow(r1, r2)' and 'NextCol(c1, c2)' instead of
#    'AdjacentRight', etc. Also gets rid of up and left adjacencies, and moves into initial instead of domain. 
#    Also uses AtHorizontal() and AtVertical(), combining two checks into one.
# 3. Actions: Removes all multi-step actions (e.g., 'CarMoveRightTwo')
#    and relies on POST-PROCESSING to put together single-step moves. I'VE SURPRISINGLY FOUND THIS IS 
#    NON-TRIVIAL (more details in expanded_rush_hour_driver.py).
#    
#Took 365.5319 seconds to find a valid plan - 5.1X slower than same problem on an unoptimized 4x4 grid
#Decent runtime tradeoff for the 6x6 grid
#No runner for any configuration yet

#From here, I need to create a driver file to run any problem representation. This is addressed in expanded_rush_hour_driver.py


#--------------------------------------------------------------------------------------------------------

from planning import *
from logic import *

def rush_hour_6x6_multistep_with_trucks2(config):
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
        elif car_dir == 'Vertical':
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
    domain = ' & '.join(domain)

    # ---  Returning filled out & desired data ---

    return PlanningProblem(
        initial=expr(initial),
        goals=expr(goals),
        actions=[
            # --- Horizontal moves --- 
            Action('CarMoveRight(c, r, frm, to)',
                precond=expr('AtHorizontal(c, r, frm) & NextCol(frm, to) & Clear(r, to)'),
                effect=expr('~AtHorizontal(c, r, frm) & AtHorizontal(c, r, to) & Clear(r, frm) & ~Clear(r, to)'),
                domain=expr('Car(c) & Row(r) & Col(frm) & Col(to)')),
            Action('CarMoveLeft(c, r, frm, to)',
                precond=expr('AtHorizontal(c, r, frm) & NextCol(to, frm) & Clear(r, to)'),
                effect=expr('~AtHorizontal(c, r, frm) & AtHorizontal(c, r, to) & Clear(r, frm) & ~Clear(r, to)'),
                domain=expr('Car(c) & Row(r) & Col(frm) & Col(to)')),
            Action('TruckMoveRight(t, r, from1, from2, to)',
                precond=expr('AtHorizontal(t, r, from1) & AtHorizontal(t, r, from2) & NextCol(from1, from2) & NextCol(from2, to) & Clear(r, to)'),
                effect=expr('~AtHorizontal(t, r, from1) & AtHorizontal(t, r, to) & Clear(r, from1) & ~Clear(r, to)'),
                domain=expr('Truck(t) & Row(r) & Col(from1) & Col(from2) & Col(to)')),
            Action('TruckMoveLeft(t, r, from1, from2, to)',
                precond=expr('AtHorizontal(t, r, from2) & AtHorizontal(t, r, from1) & NextCol(to, from1) & NextCol(from1, from2) & Clear(r, to)'),
                effect=expr('~AtHorizontal(t, r, from2) & AtHorizontal(t, r, to) & Clear(r, from2) & ~Clear(r, to)'),
                domain=expr('Truck(t) & Row(r) & Col(from1) & Col(from2) & Col(to)')),
            # --- Vertical moves ---
            Action('CarMoveDown(c, c1, frm, to)',
                precond=expr('AtVertical(c, frm, c1) & NextRow(frm, to) & Clear(to, c1)'),
                effect=expr('~AtVertical(c, frm, c1) & AtVertical(c, to, c1) & Clear(frm, c1) & ~Clear(to, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(frm) & Row(to)')),
            Action('CarMoveUp(c, c1, frm, to)',
                precond=expr('AtVertical(c, frm, c1) & NextRow(to, frm) & Clear(to, c1)'),
                effect=expr('~AtVertical(c, frm, c1) & AtVertical(c, to, c1) & Clear(frm, c1) & ~Clear(to, c1)'),
                domain=expr('Car(c) & Col(c1) & Row(frm) & Row(to)')),
            Action('TruckMoveDown(t, c1, from1, from2, to)',
                precond=expr('AtVertical(t, from1, c1) & AtVertical(t, from2, c1) & NextRow(from1, from2) & NextRow(from2, to) & Clear(to, c1)'),
                effect=expr('~AtVertical(t, from1, c1) & AtVertical(t, to, c1) & Clear(from1, c1) & ~Clear(to, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(from1) & Row(from2) & Row(to)')),
            Action('TruckMoveUp(t, c1, from1, from2, to)',
                precond=expr('AtVertical(t, from2, c1) & AtVertical(t, from1, c1) & NextRow(to, from1) & NextRow(from1, from2) & Clear(to, c1)'),
                effect=expr('~AtVertical(t, from2, c1) & AtVertical(t, to, c1) & Clear(from2, c1) & ~Clear(to, c1)'),
                domain=expr('Truck(t) & Col(c1) & Row(from1) & Row(from2) & Row(to)'))
        ],
        domain=expr(domain)
    )