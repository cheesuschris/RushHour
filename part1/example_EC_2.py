#--------------------------------------------------------------------------------------------------------

#PRE-FEATURES, TESTING TIMES TO RUN GRAPHPLAN FROM THE EXAMPLE INPUT
#Took 75.5459 seconds to find a valid plan
#Took 155.3042 seconds to fail to find a valid plan when no valid solution existed

#--------------------------------------------------------------------------------------------------------

from planning import *
from logic import *

def rush_hour_with_trucks2(config):
    """
    Returns a PlanningProblem object, emulating rush_hour_4x4()
    """
    
    # BEGIN_WORK_HERE

    initials = []
    occupied_cells = [[False for _ in range(4)] for _ in range(4)]

    domain_parts = []

    for car, data in config["cars"].items():
        pos_x, pos_y = data['pos']
        direction = data['dir']

        initials.append(f'Car({car})')
        initials.append(f"At({car}, C{pos_x}_{pos_y})")
        initials.append(f"{direction}({car})")
        occupied_cells[pos_x - 1][pos_y - 1] = True

        domain_parts.append(f"Car({car}) & {direction}({car})")

    for truck, data in config["trucks"].items():
        (f_pos_x, f_pos_y), (s_pos_x, s_pos_y) = data['pos']
        direction = data['dir']

        initials.append(f"Truck({truck})")
        initials.append(f"Occupies({truck}, C{f_pos_x}_{f_pos_y})")
        initials.append(f"Occupies({truck}, C{s_pos_x}_{s_pos_y})")
        initials.append(f"{direction}({truck})")

        occupied_cells[f_pos_x - 1][f_pos_y - 1] = True
        occupied_cells[s_pos_x - 1][s_pos_y - 1] = True

        domain_parts.append(f"Truck({truck}) & {direction}({truck})")
    
    for i in range(len(occupied_cells)):
        for j in range(len(occupied_cells[0])):
            if not occupied_cells[i][j]:
                initials.append(f"Clear(C{i + 1}_{j + 1})")
    
    initials = " & ".join(initials)

    goals = []
    for vehicle, pos in config["goal"].items():
        if isinstance(pos[0], tuple):
            (x1, y1), (x2, y2) = pos
            goals.append(f"Occupies({vehicle}, C{x1}_{y1})")
            goals.append(f"Occupies({vehicle}, C{x2}_{y2})")
        else:
            x, y = pos
            goals.append(f"At({vehicle}, C{x}_{y})")

    goals = " & ".join(goals)



    domain = expr(        
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
        
        # BEGIN_YOUR_CODE
        
        'AdjacentUp(C2_1, C1_1) & AdjacentUp(C3_1, C2_1) & AdjacentUp(C4_1, C3_1) & '
        'AdjacentUp(C2_2, C1_2) & AdjacentUp(C3_2, C2_2) & AdjacentUp(C4_2, C3_2) & '
        'AdjacentUp(C2_3, C1_3) & AdjacentUp(C3_3, C2_3) & AdjacentUp(C4_3, C3_3) & '
        'AdjacentUp(C2_4, C1_4) & AdjacentUp(C3_4, C2_4) & AdjacentUp(C4_4, C3_4)'
        
        # END_YOUR_CODE
    )
    
    actions=[
        # --- Horizontal moves ---
        Action('MoveRight(c, frm, to)',
            precond=expr('At(c, frm) & Clear(to) & Horizontal(c) & AdjacentRight(frm, to)'),
            effect=expr('At(c, to) & Clear(frm) & ~At(c, frm) & ~Clear(to)'),
            domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentRight(frm, to)')),
        
        # BEGIN_YOUR_CODE

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
            domain=expr('Car(c) & Cell(frm) & Cell(to) & AdjacentDown(frm, to)')),
        
        # END_YOUR_CODE
        
    ]


    actions += [
        Action('MoveRightTruck(t, frm1, frm2, to)',
            precond=expr('Occupies(t, frm1) & Occupies(t, frm2) & Clear(to) & Horizontal(t) & AdjacentRight(frm2, to)'),
            effect=expr('Occupies(t, frm2) & Occupies(t, to) & Clear(frm1) & ~Occupies(t, frm1) & ~Clear(to)'),
            domain=expr('Truck(t) & Cell(frm1) & Cell(frm2) & Cell(to)')),

        Action('MoveLeftTruck(t, frm1, frm2, to)',
            precond=expr('Occupies(t, frm1) & Occupies(t, frm2) & Clear(to) & Horizontal(t) & AdjacentLeft(frm1, to)'),
            effect=expr('Occupies(t, to) & Occupies(t, frm1) & Clear(frm2) & ~Occupies(t, frm2) & ~Clear(to)'),
            domain=expr('Truck(t) & Cell(frm1) & Cell(frm2) & Cell(to)')),

        Action('MoveUpTruck(t, frm1, frm2, to)',
            precond=expr('Occupies(t, frm1) & Occupies(t, frm2) & Clear(to) & Vertical(t) & AdjacentUp(frm1, to)'),
            effect=expr('Occupies(t, to) & Occupies(t, frm1) & Clear(frm2) & ~Occupies(t, frm2) & ~Clear(to)'),
            domain=expr('Truck(t) & Cell(frm1) & Cell(frm2) & Cell(to)')),

        Action('MoveDownTruck(t, frm1, frm2, to)',
            precond=expr('Occupies(t, frm1) & Occupies(t, frm2) & Clear(to) & Vertical(t) & AdjacentDown(frm2, to)'),
            effect=expr('Occupies(t, frm2) & Occupies(t, to) & Clear(frm1) & ~Occupies(t, frm1) & ~Clear(to)'),
            domain=expr('Truck(t) & Cell(frm1) & Cell(frm2) & Cell(to)')),
    ]


    return PlanningProblem(
        initial=expr(initials),
        goals=expr(goals), 
        actions=actions, 
        domain=domain
    )
    # #END_WORK_HERE