#--------------------------------------------------------------------------------------------------------


#MERGED FEATURES VER. 1: TAKES FEAT1VER1 AND FEAT2VER1, INTRODUCING BOTH 6X6 GRID & MULTISTEP ACTIONS TO THE NORMAL PROBLEM
#Could NOT find a valid plan, simply printed "Killed" when I ran this on the sample input. Apparently this happened because of the OOM killer
#killing the most memory-hungry processes to prevent system crashes. This signaled a VERY computationaly expensive program, very unreasonable
#No runner for any configuration yet

#From here, I DEFINITELY need to convert to PDDL and find a more optimal representation. This is addressed in the pddl version of this file


#--------------------------------------------------------------------------------------------------------

from planning import *
from logic import *

def rush_hour_6x6_multistep_with_trucks(config):
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

    cells = {f'C{r}_{c}' for r in range(1, 7) for c in range(1, 7)}

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
            Action('CarMoveRightFour(c, frm, between, between2, between3, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Clear(between3) & Horizontal(c) & AdjacentRight(frm, between) & AdjacentRight(between, between2) & AdjacentRight(between2, between3) & AdjacentRight(between3, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(between3) & Cell(to) & AdjacentRight(frm, between) & AdjacentRight(between, between2) & AdjacentRight(between2, between3) & AdjacentRight(between3, to)')),
            Action('CarMoveRightFive(c, frm, between, between2, between3, between4, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Clear(between3) & Clear(between4) & Horizontal(c) & AdjacentRight(frm, between) & AdjacentRight(between, between2) & AdjacentRight(between2, between3) & AdjacentRight(between3, between4) & AdjacentRight(between4, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(between3) & Cell(between4) & Cell(to) & AdjacentRight(frm, between) & AdjacentRight(between, between2) & AdjacentRight(between2, between3) & AdjacentRight(between3, between4) & AdjacentRight(between4, to)')),
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
            Action('CarMoveLeftFour(c, frm, between, between2, between3, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Clear(between3) & Horizontal(c) & AdjacentLeft(frm, between) & AdjacentLeft(between, between2) & AdjacentLeft(between2, between3) & AdjacentLeft(between3, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(between3) & Cell(to) & AdjacentLeft(frm, between) & AdjacentLeft(between, between2) & AdjacentLeft(between2, between3) & AdjacentLeft(between3, to)')),
            Action('CarMoveLeftFive(c, frm, between, between2, between3, between4, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Clear(between3) & Clear(between4) & Horizontal(c) & AdjacentLeft(frm, between) & AdjacentLeft(between, between2) & AdjacentLeft(between2, between3) & AdjacentLeft(between3, between4) & AdjacentLeft(between4, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(between3) & Cell(between4) & Cell(to) & AdjacentLeft(frm, between) & AdjacentLeft(between, between2) & AdjacentLeft(between2, between3) & AdjacentLeft(between3, between4) & AdjacentLeft(between4, to)')),
            Action('TruckMoveRight(t, t_head, t_tail, to)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to) & Horizontal(t) & AdjacentRight(t_tail, t_head) & AdjacentRight(t_head, to)'),
                    effect=expr('~Clear(to) & Occupies(t, to) & Clear(t_tail) & ~Occupies(t, t_tail)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to)')),
            Action('TruckMoveRightTwo(t, t_head, t_tail, to_head, to_tail)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to_head) & Clear(to_tail) & Horizontal(t) & AdjacentRight(t_tail, t_head) & AdjacentRight(t_head, to_tail) & AdjacentRight(to_tail, to_head)'),
                    effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveRightThree(t, t_head, t_tail, between, to_head, to_tail)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(between) & Clear(to_head) & Clear(to_tail) & Horizontal(t) & AdjacentRight(t_tail, t_head) & AdjacentRight(t_head, between) & AdjacentRight(between, to_tail) & AdjacentRight(to_tail, to_head)'),
                    effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(between) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveRightFour(t, t_head, t_tail, between, between2, to_head, to_tail)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(between) & Clear(between2) & Clear(to_head) & Clear(to_tail) & Horizontal(t) & AdjacentRight(t_tail, t_head) & AdjacentRight(t_head, between) & AdjacentRight(between, between2) & AdjacentRight(between2, to_tail) & AdjacentRight(to_tail, to_head)'),
                    effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(between) & Cell(between2) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveLeft(t, t_head, t_tail, to)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to) & Horizontal(t) & AdjacentLeft(t_head, t_tail) & AdjacentLeft(t_tail, to)'),
                    effect=expr('~Clear(to) & Occupies(t, to) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to)')),
            Action('TruckMoveLeftTwo(t, t_head, t_tail, to_head, to_tail)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to_head) & Clear(to_tail) & Horizontal(t) & AdjacentLeft(t_head, t_tail) & AdjacentLeft(t_tail, to_head) & AdjacentLeft(to_head, to_tail)'),
                    effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveLeftThree(t, t_head, t_tail, between, to_head, to_tail)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(between) & Clear(to_head) & Clear(to_tail) & Horizontal(t) & AdjacentLeft(t_head, t_tail) & AdjacentLeft(t_tail, between) & AdjacentLeft(between, to_head) & AdjacentLeft(to_head, to_tail)'),
                    effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(between) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveLeftFour(t, t_head, t_tail, between, between2, to_head, to_tail)',
                    precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(between) & Clear(between2) & Clear(to_head) & Clear(to_tail) & Horizontal(t) & AdjacentLeft(t_head, t_tail) & AdjacentLeft(t_tail, between) & AdjacentLeft(between, between2) & AdjacentLeft(between2, to_head) & AdjacentLeft(to_head, to_tail)'),
                    effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                    domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(between) & Cell(between2) & Cell(to_head) & Cell(to_tail)')),
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
            Action('CarMoveUpFour(c, frm, between, between2, between3, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Clear(between3) & Vertical(c) & AdjacentUp(frm, between) & AdjacentUp(between, between2) & AdjacentUp(between2, between3) & AdjacentUp(between3, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(between3) & Cell(to) & AdjacentUp(frm, between) & AdjacentUp(between, between2) & AdjacentUp(between2, between3) & AdjacentUp(between3, to)')),
            Action('CarMoveUpFive(c, frm, between, between2, between3, between4, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Clear(between3) & Clear(between4) & Vertical(c) & AdjacentUp(frm, between) & AdjacentUp(between, between2) & AdjacentUp(between2, between3) & AdjacentUp(between3, between4) & AdjacentUp(between4, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(between3) & Cell(between4) & Cell(to) & AdjacentUp(frm, between) & AdjacentUp(between, between2) & AdjacentUp(between2, between3) & AdjacentUp(between3, between4) & AdjacentUp(between4, to)')),
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
            Action('CarMoveDownFour(c, frm, between, between2, between3, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Clear(between3) & Vertical(c) & AdjacentDown(frm, between) & AdjacentDown(between, between2) & AdjacentDown(between2, between3) & AdjacentDown(between3, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(between3) & Cell(to) & AdjacentDown(frm, between) & AdjacentDown(between, between2) & AdjacentDown(between2, between3) & AdjacentDown(between3, to)')),
            Action('CarMoveDownFive(c, frm, between, between2, between3, between4, to)',
                precond=expr('At(c, frm) & Clear(to) & Clear(between) & Clear(between2) & Clear(between3) & Clear(between4) & Vertical(c) & AdjacentDown(frm, between) & AdjacentDown(between, between2) & AdjacentDown(between2, between3) & AdjacentDown(between3, between4) & AdjacentDown(between4, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(between) & Cell(between2) & Cell(between3) & Cell(between4) & Cell(to) & AdjacentDown(frm, between) & AdjacentDown(between, between2) & AdjacentDown(between2, between3) & AdjacentDown(between3, between4) & AdjacentDown(between4, to)')),
            Action('TruckMoveUp(t, t_head, t_tail, to)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to) & Vertical(t) & AdjacentUp(t_head, t_tail) & AdjacentUp(t_tail, to)'),
                   effect=expr('Occupies(t, t_tail) & ~Clear(to) & Occupies(t, to) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to)')),
            Action('TruckMoveUpTwo(t, t_head, t_tail, to_head, to_tail)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to_head) & Clear(to_tail) & Vertical(t) & AdjacentUp(t_head, t_tail) & AdjacentUp(t_tail, to_head) & AdjacentUp(to_head, to_tail)'),
                   effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveUpThree(t, t_head, t_tail, between, to_head, to_tail)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(between) & Clear(to_head) & Clear(to_tail) & Vertical(t) & AdjacentUp(t_head, t_tail) & AdjacentUp(t_tail, between) & AdjacentUp(between, to_head) & AdjacentUp(to_head, to_tail)'),
                   effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(between) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveUpFour(t, t_head, t_tail, between, between2, to_head, to_tail)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(between) & Clear(between2) & Clear(to_head) & Clear(to_tail) & Vertical(t) & AdjacentUp(t_head, t_tail) & AdjacentUp(t_tail, between) & AdjacentUp(between, between2) & AdjacentUp(between2, to_head) & AdjacentUp(to_head, to_tail)'),
                   effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(between) & Cell(between2) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveDown(t, t_head, t_tail, to)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to) & Vertical(t) & AdjacentDown(t_tail, t_head) & AdjacentDown(t_head, to)'),
                   effect=expr('Occupies(t, t_head) & ~Clear(to) & Occupies(t, to) & Clear(t_tail) & ~Occupies(t, t_tail)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to)')),
            Action('TruckMoveDownTwo(t, t_head, t_tail, to_head, to_tail)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(to_head) & Clear(to_tail) & Vertical(t) & AdjacentDown(t_tail, t_head) & AdjacentDown(t_head, to_tail) & AdjacentDown(to_tail, to_head)'),
                   effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveDownThree(t, t_head, t_tail, between, to_head, to_tail)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(between) & Clear(to_head) & Clear(to_tail) & Vertical(t) & AdjacentDown(t_tail, t_head) & AdjacentDown(t_head, between) & AdjacentDown(between, to_tail) & AdjacentDown(to_tail, to_head)'),
                   effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(between) & Cell(to_head) & Cell(to_tail)')),
            Action('TruckMoveDownFour(t, t_head, t_tail, between, between2, to_head, to_tail)',
                   precond=expr('Occupies(t, t_head) & Occupies(t, t_tail) & Clear(between) & Clear(between2) & Clear(to_head) & Clear(to_tail) & Vertical(t) & AdjacentDown(t_tail, t_head) & AdjacentDown(t_head, between) & AdjacentDown(between, between2) & AdjacentDown(between2, to_tail) & AdjacentDown(to_tail, to_head)'),
                   effect=expr('~Clear(to_tail) & Occupies(t, to_tail) & ~Clear(to_head) & Occupies(t, to_head) & Clear(t_tail) & ~Occupies(t, t_tail) & Clear(t_head) & ~Occupies(t, t_head)'),
                   domain=expr('Truck(t) & Cell(t_head) & Cell(t_tail) & Cell(between) & Cell(between2) & Cell(to_head) & Cell(to_tail)')),
        ],
        domain=expr(
            # --- Car & Truck definitions ---
            domain + ' & '
            # --- Cell definitions ---
            'Cell(C1_1) & Cell(C1_2) & Cell(C1_3) & Cell(C1_4) & Cell(C1_5) & Cell(C1_6) & '
            'Cell(C2_1) & Cell(C2_2) & Cell(C2_3) & Cell(C2_4) & Cell(C2_5) & Cell(C2_6) & '
            'Cell(C3_1) & Cell(C3_2) & Cell(C3_3) & Cell(C3_4) & Cell(C3_5) & Cell(C3_6) & '
            'Cell(C4_1) & Cell(C4_2) & Cell(C4_3) & Cell(C4_4) & Cell(C4_5) & Cell(C4_6) & '
            'Cell(C5_1) & Cell(C5_2) & Cell(C5_3) & Cell(C5_4) & Cell(C5_5) & Cell(C5_6) & '
            'Cell(C6_1) & Cell(C6_2) & Cell(C6_3) & Cell(C6_4) & Cell(C6_5) & Cell(C6_6) & '
            # --- Adjacency (complete, propositional) ---
            'AdjacentRight(C1_1, C1_2) & AdjacentRight(C1_2, C1_3) & AdjacentRight(C1_3, C1_4) & AdjacentRight(C1_4, C1_5) & AdjacentRight(C1_5, C1_6) & '
            'AdjacentRight(C2_1, C2_2) & AdjacentRight(C2_2, C2_3) & AdjacentRight(C2_3, C2_4) & AdjacentRight(C2_4, C2_5) & AdjacentRight(C2_5, C2_6) & '
            'AdjacentRight(C3_1, C3_2) & AdjacentRight(C3_2, C3_3) & AdjacentRight(C3_3, C3_4) & AdjacentRight(C3_4, C3_5) & AdjacentRight(C3_5, C3_6) & '
            'AdjacentRight(C4_1, C4_2) & AdjacentRight(C4_2, C4_3) & AdjacentRight(C4_3, C4_4) & AdjacentRight(C4_4, C4_5) & AdjacentRight(C4_5, C4_6) & '
            'AdjacentRight(C5_1, C5_2) & AdjacentRight(C5_2, C5_3) & AdjacentRight(C5_3, C5_4) & AdjacentRight(C5_4, C5_5) & AdjacentRight(C5_5, C5_6) & '
            'AdjacentRight(C6_1, C6_2) & AdjacentRight(C6_2, C6_3) & AdjacentRight(C6_3, C6_4) & AdjacentRight(C6_4, C6_5) & AdjacentRight(C6_5, C6_6) & '
            'AdjacentLeft(C1_2, C1_1) & AdjacentLeft(C1_3, C1_2) & AdjacentLeft(C1_4, C1_3) & AdjacentLeft(C1_5, C1_4) & AdjacentLeft(C1_6, C1_5) & '
            'AdjacentLeft(C2_2, C2_1) & AdjacentLeft(C2_3, C2_2) & AdjacentLeft(C2_4, C2_3) & AdjacentLeft(C2_5, C2_4) & AdjacentLeft(C2_6, C2_5) & '
            'AdjacentLeft(C3_2, C3_1) & AdjacentLeft(C3_3, C3_2) & AdjacentLeft(C3_4, C3_3) & AdjacentLeft(C3_5, C3_4) & AdjacentLeft(C3_6, C3_5) & '
            'AdjacentLeft(C4_2, C4_1) & AdjacentLeft(C4_3, C4_2) & AdjacentLeft(C4_4, C4_3) & AdjacentLeft(C4_5, C4_4) & AdjacentLeft(C4_6, C4_5) & '
            'AdjacentLeft(C5_2, C5_1) & AdjacentLeft(C5_3, C5_2) & AdjacentLeft(C5_4, C5_3) & AdjacentLeft(C5_5, C5_4) & AdjacentLeft(C5_6, C5_5) & '
            'AdjacentLeft(C6_2, C6_1) & AdjacentLeft(C6_3, C6_2) & AdjacentLeft(C6_4, C6_3) & AdjacentLeft(C6_5, C6_4) & AdjacentLeft(C6_6, C6_5) & '
            'AdjacentDown(C1_1, C2_1) & AdjacentDown(C2_1, C3_1) & AdjacentDown(C3_1, C4_1) & AdjacentDown(C4_1, C5_1) & AdjacentDown(C5_1, C6_1) & '
            'AdjacentDown(C1_2, C2_2) & AdjacentDown(C2_2, C3_2) & AdjacentDown(C3_2, C4_2) & AdjacentDown(C4_2, C5_2) & AdjacentDown(C5_2, C6_2) & '
            'AdjacentDown(C1_3, C2_3) & AdjacentDown(C2_3, C3_3) & AdjacentDown(C3_3, C4_3) & AdjacentDown(C4_3, C5_3) & AdjacentDown(C5_3, C6_3) & '
            'AdjacentDown(C1_4, C2_4) & AdjacentDown(C2_4, C3_4) & AdjacentDown(C3_4, C4_4) & AdjacentDown(C4_4, C5_4) & AdjacentDown(C5_4, C6_4) & '
            'AdjacentDown(C1_5, C2_5) & AdjacentDown(C2_5, C3_5) & AdjacentDown(C3_5, C4_5) & AdjacentDown(C4_5, C5_5) & AdjacentDown(C5_5, C6_5) & '
            'AdjacentDown(C1_6, C2_6) & AdjacentDown(C2_6, C3_6) & AdjacentDown(C3_6, C4_6) & AdjacentDown(C4_6, C5_6) & AdjacentDown(C5_6, C6_6) & '
            'AdjacentUp(C2_1, C1_1) & AdjacentUp(C3_1, C2_1) & AdjacentUp(C4_1, C3_1) & AdjacentUp(C5_1, C4_1) & AdjacentUp(C6_1, C5_1) & '
            'AdjacentUp(C2_2, C1_2) & AdjacentUp(C3_2, C2_2) & AdjacentUp(C4_2, C3_2) & AdjacentUp(C5_2, C4_2) & AdjacentUp(C6_2, C5_2) & '
            'AdjacentUp(C2_3, C1_3) & AdjacentUp(C3_3, C2_3) & AdjacentUp(C4_3, C3_3) & AdjacentUp(C5_3, C4_3) & AdjacentUp(C6_3, C5_3) & '
            'AdjacentUp(C2_4, C1_4) & AdjacentUp(C3_4, C2_4) & AdjacentUp(C4_4, C3_4) & AdjacentUp(C5_4, C4_4) & AdjacentUp(C6_4, C5_4) & '
            'AdjacentUp(C2_5, C1_5) & AdjacentUp(C3_5, C2_5) & AdjacentUp(C4_5, C3_5) & AdjacentUp(C5_5, C4_5) & AdjacentUp(C6_5, C5_5) & '
            'AdjacentUp(C2_6, C1_6) & AdjacentUp(C3_6, C2_6) & AdjacentUp(C4_6, C3_6) & AdjacentUp(C5_6, C4_6) & AdjacentUp(C6_6, C5_6)'
        )
    )