#--------------------------------------------------------------------------------------------------------


#FIRST FEATURE VER. 2: LITERALLY TAKES ONLY EXAMPLE_EC_1 AND EXPANDS IT TO 6X6
#Representational changes made from Ver. 1: The Occupies() check turned into AtRear() and AtFront()
#This representation STILL takes a long time to solve for Graphplan
#Took 2193.0940 seconds to find a valid plan - 30.7X slower than same problem on a 4x4 grid
#No multi-step action implementation yet
#No runner for any configuration yet

#From here, I realize I made a mistake and that Occupies() is probably a simpler representational check. The answer is still 
#correct in this version, and still isn't efficient. I will backtrack back to version 1 and merge version 1 (STILL VERY SLOW) with the 
#multistep-action feature, and my GUESS is that it will be VERY computationally expensive. So from there I will continue to convert 
#to PDDL to debug and potentially find a better problem representation that includes both features. Basically this route was a dead-end, 
#but still I documented my process.
#An additional note: the 6x6 grid feature is way more expensive on runtime than the multistep-actionset is, so maybe I will focus
#on this 6x6 grid feature first before the multistep-actionset feature when debugging with PDDL/LLM suggestions on representational 
#improvement.


#--------------------------------------------------------------------------------------------------------

from planning import *
from logic import *

def rush_hour_6x6_with_trucks2(config):
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
    
    N = 6
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
            
            'Cell(C1_1) & Cell(C1_2) & Cell(C1_3) & Cell(C1_4) & Cell(C1_5) & Cell(C1_6) & '
            'Cell(C2_1) & Cell(C2_2) & Cell(C2_3) & Cell(C2_4) & Cell(C2_5) & Cell(C2_6) & '
            'Cell(C3_1) & Cell(C3_2) & Cell(C3_3) & Cell(C3_4) & Cell(C3_5) & Cell(C3_6) & '
            'Cell(C4_1) & Cell(C4_2) & Cell(C4_3) & Cell(C4_4) & Cell(C4_5) & Cell(C4_6) & '
            'Cell(C5_1) & Cell(C5_2) & Cell(C5_3) & Cell(C5_4) & Cell(C5_5) & Cell(C5_6) & '
            'Cell(C6_1) & Cell(C6_2) & Cell(C6_3) & Cell(C6_4) & Cell(C6_5) & Cell(C6_6) & '
            
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