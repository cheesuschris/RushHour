#--------------------------------------------------------------------------------------------------------

#PRE-FEATURES, TESTING TIMES TO RUN GRAPHPLAN FROM THE EXAMPLE INPUT
#Took 71.4382 seconds to find a valid plan
#Took 161.9183 seconds to fail to find a valid plan when no valid solution existed

#--------------------------------------------------------------------------------------------------------

import pytest
from planning import *
from logic import *
import time

def rush_hour_with_trucks(config):
    """
    Returns a PlanningProblem object, emulating rush_hour_4x4()
    """
    N = 4
    cars = config['cars']
    trucks = config['trucks']
    vehicle_goals = config['goal']
    
    initial_parts = []
    car_domain_parts = []
    truck_domain_parts = []
    goal_parts = []
    
    empty_cells = {f'C{r+1}_{c+1}' for r in range(N) for c in range(N)}
    
    for car, info in cars.items():
        pos = info['pos']
        direction = info['dir']
        cell = f'C{pos[0]}_{pos[1]}'
        
        initial_parts.extend([f'At({car}, {cell})', f'{direction}({car})'])
        car_domain_parts.append(f'Car({car})')
        empty_cells.discard(cell)
    
    for truck, info in trucks.items():
        pos = sorted(info['pos'], reverse=True)
        direction = info['dir']
        cell1 = f'C{pos[0][0]}_{pos[0][1]}'
        cell2 = f'C{pos[1][0]}_{pos[1][1]}'
        
        initial_parts.extend([f'AtFront({truck}, {cell1})', f'AtRear({truck}, {cell2})', f'{direction}({truck})'])
        truck_domain_parts.append(f'Truck({truck})')
        empty_cells.discard(cell1)
        empty_cells.discard(cell2)
        
    initial_parts.extend([f'Clear({cell})' for cell in sorted(empty_cells)])
    
    for vehicle, goal_pos in vehicle_goals.items():
        if vehicle in cars:
            goal_cell = f'C{goal_pos[0]}_{goal_pos[1]}'
            goal_parts.append(f'At({vehicle}, {goal_cell})')
        else:
            goal_pos_sorted = sorted(goal_pos, reverse=True)
            goal_cell1 = f'C{goal_pos_sorted[0][0]}_{goal_pos_sorted[0][1]}'
            goal_cell2 = f'C{goal_pos_sorted[1][0]}_{goal_pos_sorted[1][1]}'
            goal_parts.extend([f'AtFront({vehicle}, {goal_cell1})', f'AtRear({vehicle}, {goal_cell2})'])
    
    
    initial = ' & '.join(initial_parts)
    goals = ' & '.join(goal_parts)
    domain = ' & '.join(car_domain_parts + truck_domain_parts)
    
    car_actions = [
        Action('MoveRight(c, frm, to)',
                precond=expr('At(c, frm) & Clear(to) & Horizontal(c) & AdjacentRight(frm, to)'),
                effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
                domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentRight(frm, to)')),
            
        Action('MoveLeft(c, frm, to)',
            precond=expr('At(c, frm) & Clear(to) & Horizontal(c) & AdjacentLeft(frm, to)'),
            effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
            domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentLeft(frm, to)')),

        Action('MoveUp(c, frm, to)',
            precond=expr('At(c, frm) & Clear(to) & Vertical(c) & AdjacentUp(frm, to)'),
            effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
            domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentUp(frm, to)')),

        Action('MoveDown(c, frm, to)',
            precond=expr('At(c, frm) & Clear(to) & Vertical(c) & AdjacentDown(frm, to)'),
            effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
            domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentDown(frm, to)'))
    ]
    
    truck_actions = [
        Action('TruckMoveRight(t, oldrear, oldfront, newfront)',
            precond=expr('AtRear(t, oldrear) & AtFront(t, oldfront) & Horizontal(t) & AdjacentRight(oldrear, oldfront) & AdjacentRight(oldfront, newfront) & Clear(newfront)'),
            effect=expr('AtRear(t, oldfront) & AtFront(t, newfront) & Clear(oldrear) & ~AtRear(t, oldrear) & ~AtFront(t, oldfront) & ~Clear(newfront)'),
            domain=expr('Truck(t) & Cell(oldrear) & Cell(oldfront) & Cell(newfront)')),
        
        Action('TruckMoveLeft(t, oldrear, oldfront, newrear)',
            precond=expr('AtRear(t, oldrear) & AtFront(t, oldfront) & Horizontal(t) & AdjacentRight(oldrear, oldfront) & AdjacentLeft(oldrear, newrear) & Clear(newrear)'),
            effect=expr('AtFront(t, oldrear) & AtRear(t, newrear) & Clear(oldfront) & ~AtRear(t, oldrear) & ~AtFront(t, oldfront) & ~Clear(newrear)'),
            domain=expr('Truck(t) & Cell(oldrear) & Cell(oldfront) & Cell(newrear)')),
        
        Action('TruckMoveUp(t, oldrear, oldfront, newrear)',
            precond=expr('AtRear(t, oldrear) & AtFront(t, oldfront) & Vertical(t) & AdjacentDown(oldrear, oldfront) & AdjacentUp(oldrear, newrear) & Clear(newrear)'),
            effect=expr('AtFront(t, oldrear) & AtRear(t, newrear) & Clear(oldfront) & ~AtRear(t, oldrear) & ~AtFront(t, oldfront) & ~Clear(newrear)'),
            domain=expr('Truck(t) & Cell(oldrear) & Cell(oldfront) & Cell(newrear)')),
        
        Action('TruckMoveDown(t, oldrear, oldfront, newfront)',
            precond=expr('AtRear(t, oldrear) & AtFront(t, oldfront) & Vertical(t) & AdjacentDown(oldrear, oldfront) & AdjacentDown(oldfront, newfront) & Clear(newfront)'),
            effect=expr('AtRear(t, oldfront) & AtFront(t, newfront) & Clear(oldrear) & ~AtRear(t, oldrear) & ~AtFront(t, oldfront) & ~Clear(newfront)'),
            domain=expr('Truck(t) & Cell(oldrear) & Cell(oldfront) & Cell(newfront)'))
    ]

    actions = car_actions + truck_actions

    return PlanningProblem(
        initial=expr(initial),
        goals=expr(goals),
        actions=actions,
        domain=expr(
            domain + ' & '
            
            'Cell(C1_1) & Cell(C1_2) & Cell(C1_3) & Cell(C1_4) & '
            'Cell(C2_1) & Cell(C2_2) & Cell(C2_3) & Cell(C2_4) & '
            'Cell(C3_1) & Cell(C3_2) & Cell(C3_3) & Cell(C3_4) & '
            'Cell(C4_1) & Cell(C4_2) & Cell(C4_3) & Cell(C4_4) & '
            
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

if __name__ == "__main__":
    p = rush_hour_with_trucks(config = {
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
            'R': (3, 4),                                 # Red car must reach exit
            'T1': ((1, 2), (2, 2))                       # Truck T2 must move up two cells
        }
    })
    # print(f"Initial: {p.initial}")
    # print(f"Goals: {p.goals}")
    # print(f"Actions: {p.actions}")
    # print(f"Domain: {p.domain}")
    start = time.time()
    g = GraphPlan(p).execute()
    l = Linearize(p).execute()
    end = time.time()
    print(f"Elapsed CPU time: {end-start} seconds")
    print(g[0], l)