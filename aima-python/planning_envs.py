from planning import *

def air_cargo():
    """
    [Figure 10.1] AIR-CARGO-PROBLEM

    An air-cargo shipment problem for delivering cargo to different locations,
    given the starting location and airplanes.

    Example:
    >>> from planning import *
    >>> ac = air_cargo()
    >>> ac.goal_test()
    False
    >>> ac.act(expr('Load(C2, P2, JFK)'))
    >>> ac.act(expr('Load(C1, P1, SFO)'))
    >>> ac.act(expr('Fly(P1, SFO, JFK)'))
    >>> ac.act(expr('Fly(P2, JFK, SFO)'))
    >>> ac.act(expr('Unload(C2, P2, SFO)'))
    >>> ac.goal_test()
    False
    >>> ac.act(expr('Unload(C1, P1, JFK)'))
    >>> ac.goal_test()
    True
    >>>
    """

    return PlanningProblem(initial='At(C1, SFO) & At(C2, JFK) & At(P1, SFO) & At(P2, JFK)',
                           goals='At(C1, JFK) & At(C2, SFO)',
                           actions=[Action('Load(c, p, a)',
                                           precond='At(c, a) & At(p, a)',
                                           effect='In(c, p) & ~At(c, a)',
                                           domain='Cargo(c) & Plane(p) & Airport(a)'),
                                    Action('Unload(c, p, a)',
                                           precond='In(c, p) & At(p, a)',
                                           effect='At(c, a) & ~In(c, p)',
                                           domain='Cargo(c) & Plane(p) & Airport(a)'),
                                    Action('Fly(p, f, to)',
                                           precond='At(p, f)',
                                           effect='At(p, to) & ~At(p, f)',
                                           domain='Plane(p) & Airport(f) & Airport(to)')],
                           domain='Cargo(C1) & Cargo(C2) & Plane(P1) & Plane(P2) & Airport(SFO) & Airport(JFK)')


def spare_tire():
    """
    [Figure 10.2] SPARE-TIRE-PROBLEM

    A problem involving changing the flat tire of a car
    with a spare tire from the trunk.

    Example:
    >>> from planning import *
    >>> st = spare_tire()
    >>> st.goal_test()
    False
    >>> st.act(expr('Remove(Spare, Trunk)'))
    >>> st.act(expr('Remove(Flat, Axle)'))
    >>> st.goal_test()
    False
    >>> st.act(expr('PutOn(Spare, Axle)'))
    >>> st.goal_test(
    True
    >>>
    """

    return PlanningProblem(initial='At(Flat, Axle) & At(Spare, Trunk)',
                           goals='At(Spare, Axle) & At(Flat, Ground)',
                           actions=[Action('Remove(obj, loc)',
                                           precond='At(obj, loc)',
                                           effect='At(obj, Ground) & ~At(obj, loc)',
                                           domain='Tire(obj)'),
                                    Action('PutOn(t, Axle)',
                                           precond='At(t, Ground) & ~At(Flat, Axle)',
                                           effect='At(t, Axle) & ~At(t, Ground)',
                                           domain='Tire(t)'),
                                    Action('LeaveOvernight',
                                           precond='',
                                           effect='~At(Spare, Ground) & ~At(Spare, Axle) & ~At(Spare, Trunk) & \
                                        ~At(Flat, Ground) & ~At(Flat, Axle) & ~At(Flat, Trunk)')],
                           domain='Tire(Flat) & Tire(Spare)')


def three_block_tower():
    """
    [Figure 10.3] THREE-BLOCK-TOWER

    A blocks-world problem of stacking three blocks in a certain configuration,
    also known as the Sussman Anomaly.

    Example:
    >>> from planning import *
    >>> tbt = three_block_tower()
    >>> tbt.goal_test()
    False
    >>> tbt.act(expr('MoveToTable(C, A)'))
    >>> tbt.act(expr('Move(B, Table, C)'))
    >>> tbt.goal_test()
    False
    >>> tbt.act(expr('Move(A, Table, B)'))
    >>> tbt.goal_test()
    True
    >>>
    """
    return PlanningProblem(initial='On(A, Table) & On(B, Table) & On(C, A) & Clear(B) & Clear(C)',
                           goals='On(A, B) & On(B, C)',
                           actions=[Action('Move(b, x, y)',
                                           precond='On(b, x) & Clear(b) & Clear(y)',
                                           effect='On(b, y) & Clear(x) & ~On(b, x) & ~Clear(y)',
                                           domain='Block(b) & Block(y)'),
                                    Action('MoveToTable(b, x)',
                                           precond='On(b, x) & Clear(b)',
                                           effect='On(b, Table) & Clear(x) & ~On(b, x)',
                                           domain='Block(b) & Block(x)')],
                           domain='Block(A) & Block(B) & Block(C)')

def logisticsPlanCustom(initial_state=None, goal_state=None):
    if initial_state == None: 
        initial_state = 'In(C1, R1) & In(C2, D1) & In(C3, D2) & In(R1, D1) & Holding(R1)'
    if goal_state == None:
        raise ValueError("Goal must be defined")

    planning_problem = \
    PlanningProblem(initial = initial_state,
                    goals = goal_state,
                    actions=[Action('PickUp(r, c, d)',
                                    precond='In(r, d) & In (c, d) & ~Holding(r)',
                                    effect='Holding(r) & ~In(c, d) & In(c, r)', 
                                    domain='Robot(r) & Place(d) & Container(c)'),
                             Action('PutDown(r, c, d)', 
                                    precond='In(r, d) & In(c, r) & Holding(r)',
                                    effect='~Holding(r) & ~In(c, r) & In(c, d)',
                                    domain='Robot(r) & Place(d) & Container(c)'),
                            Action('Move(r, d_start, d_end)',
                                   precond='In(r,d_start)',
                                   effect='~In(r, d_start) & In(r, d_end)',
                                   domain='Robot(r) & Place(d_start) & Place(d_end)')],
                domain='Container(C1) & Container(C2) & Container(C3) & Place(D1) & Place(D2) & Place(D3) & Robot(R1)')
    
    return planning_problem


def simple_blocks_world():
    """
    SIMPLE-BLOCKS-WORLD

    A simplified definition of the Sussman Anomaly problem.

    Example:
    >>> from planning import *
    >>> sbw = simple_blocks_world()
    >>> sbw.goal_test()
    False
    >>> sbw.act(expr('ToTable(A, B)'))
    >>> sbw.act(expr('FromTable(B, A)'))
    >>> sbw.goal_test()
    False
    >>> sbw.act(expr('FromTable(C, B)'))
    >>> sbw.goal_test()
    True
    >>>
    """

    return PlanningProblem(initial='On(A, B) & Clear(A) & OnTable(B) & OnTable(C) & Clear(C)',
                           goals='On(B, A) & On(C, B)',
                           actions=[Action('ToTable(x, y)',
                                           precond='On(x, y) & Clear(x)',
                                           effect='~On(x, y) & Clear(y) & OnTable(x)'),
                                    Action('FromTable(y, x)',
                                           precond='OnTable(y) & Clear(y) & Clear(x)',
                                           effect='~OnTable(y) & ~Clear(x) & On(y, x)')])
    

def blocks_world(initial, goals, blocks):
    """
    GENERALIZED-BLOCKS-WORLD-PROBLEM

    A flexible constructor for creating blocks-world planning problems.
    You can specify any initial and goal configuration for a given set of blocks.

    Example:
    >>> from planning import *
    >>> # Let's define the classic Sussman Anomaly
    >>> initial_state = 'On(C, A) & On(A, Table) & On(B, Table) & Clear(C) & Clear(B)'
    >>> goal_state = 'On(A, B) & On(B, C)'
    >>> block_names = ['A', 'B', 'C']
    >>> sussman_anomaly = blocks_world(initial_state, goal_state, block_names)
    >>>
    >>> sussman_anomaly.goal_test()
    False
    >>> # A sequence of moves to solve it
    >>> sussman_anomaly.act(expr('MoveToTable(C, A)'))
    >>> sussman_anomaly.act(expr('Move(B, Table, C)'))
    >>> sussman_anomaly.act(expr('Move(A, Table, B)'))
    >>> sussman_anomaly.goal_test()
    True
    >>>
    """
    # Dynamically generate the domain knowledge based on the list of blocks
    domain_knowledge = ' & '.join([f'Block({b})' for b in blocks])

    # Define the fundamental actions for moving blocks
    actions = [
        Action('Move(b, x, y)',
               precond='On(b, x) & Clear(b) & Clear(y)',
               effect='On(b, y) & Clear(x) & ~On(b, x) & ~Clear(y)',
               domain='Block(b) & Block(y)'),  # 'x' can be another block or 'Table'
        Action('MoveToTable(b, x)',
               precond='On(b, x) & Clear(b)',
               effect='On(b, Table) & Clear(x) & ~On(b, x)',
               domain='Block(b) & Block(x)') # 'x' must be a block
    ]

    return PlanningProblem(initial=initial,
                           goals=goals,
                           actions=actions,
                           domain=domain_knowledge)


def have_cake_and_eat_cake_too():
    """
    [Figure 10.7] CAKE-PROBLEM

    A problem where we begin with a cake and want to
    reach the state of having a cake and having eaten a cake.
    The possible actions include baking a cake and eating a cake.

    Example:
    >>> from planning import *
    >>> cp = have_cake_and_eat_cake_too()
    >>> cp.goal_test()
    False
    >>> cp.act(expr('Eat(Cake)'))
    >>> cp.goal_test()
    False
    >>> cp.act(expr('Bake(Cake)'))
    >>> cp.goal_test()
    True
    >>>
    """

    return PlanningProblem(initial='Have(Cake)',
                           goals='Have(Cake) & Eaten(Cake)',
                           actions=[Action('Eat(Cake)',
                                           precond='Have(Cake)',
                                           effect='Eaten(Cake) & ~Have(Cake)'),
                                    Action('Bake(Cake)',
                                           precond='~Have(Cake)',
                                           effect='Have(Cake)')])


def shopping_problem():
    """
    SHOPPING-PROBLEM

    A problem of acquiring some items given their availability at certain stores.

    Example:
    >>> from planning import *
    >>> sp = shopping_problem()
    >>> sp.goal_test()
    False
    >>> sp.act(expr('Go(Home, HW)'))
    >>> sp.act(expr('Buy(Drill, HW)'))
    >>> sp.act(expr('Go(HW, SM)'))
    >>> sp.act(expr('Buy(Banana, SM)'))
    >>> sp.goal_test()
    False
    >>> sp.act(expr('Buy(Milk, SM)'))
    >>> sp.goal_test()
    True
    >>>
    """

    return PlanningProblem(initial='At(Home) & Sells(SM, Milk) & Sells(SM, Banana) & Sells(HW, Drill)',
                           goals='Have(Milk) & Have(Banana) & Have(Drill)',
                           actions=[Action('Buy(x, store)',
                                           precond='At(store) & Sells(store, x)',
                                           effect='Have(x)',
                                           domain='Store(store) & Item(x)'),
                                    Action('Go(x, y)',
                                           precond='At(x)',
                                           effect='At(y) & ~At(x)',
                                           domain='Place(x) & Place(y)')],
                           domain='Place(Home) & Place(SM) & Place(HW) & Store(SM) & Store(HW) & '
                                  'Item(Milk) & Item(Banana) & Item(Drill)')

def socks_and_shoes():
    """
    SOCKS-AND-SHOES-PROBLEM

    A task of wearing socks and shoes on both feet

    Example:
    >>> from planning import *
    >>> ss = socks_and_shoes()
    >>> ss.goal_test()
    False
    >>> ss.act(expr('RightSock'))
    >>> ss.act(expr('RightShoe'))
    >>> ss.act(expr('LeftSock'))
    >>> ss.goal_test()
    False
    >>> ss.act(expr('LeftShoe'))
    >>> ss.goal_test()
    True
    >>>
    """

    return PlanningProblem(initial='',
                           goals='RightShoeOn & LeftShoeOn',
                           actions=[Action('RightShoe',
                                           precond='RightSockOn',
                                           effect='RightShoeOn'),
                                    Action('RightSock',
                                           precond='',
                                           effect='RightSockOn'),
                                    Action('LeftShoe',
                                           precond='LeftSockOn',
                                           effect='LeftShoeOn'),
                                    Action('LeftSock',
                                           precond='',
                                           effect='LeftSockOn')])


def double_tennis_problem_simple():
    return PlanningProblem(
        initial='At(A, LeftNet) & At(B, RightNet) & Approaching(ball, RightBaseline)',
        goals='At(A, LeftBaseline) & Returned(ball)',
        actions=[Action('Hit(actor, ball, loc)',
                        precond='Approaching(ball, loc) & At(actor, loc)',
                        effect='Returned(ball)'),
                 Action('Go(actor, to, loc)',
                        precond='At(actor, loc)',
                        effect='At(actor, to) & ~At(actor, loc)')],
        domain="Loc(LeftBaseline)")

def double_tennis_problem_simple2():
    return PlanningProblem(
        initial='At(A, LeftNet) & At(B, LeftNet) & Approaching(ball, RightNet)',
        goals='At(A, LeftNet) & Returned(ball) & At(B, LeftNet)',
        actions=[Action('Hit(actor, ball, loc)',
                        precond='Approaching(ball, loc) & At(actor, loc)',
                        effect='Returned(ball)'),
                 Action('Go(actor, to, loc)',
                        precond='At(actor, loc)',
                        effect='At(actor, to) & ~At(actor, loc)')])

def double_tennis_problem_simple3():
    return PlanningProblem(
        initial='At(A, LeftNet) & Approaching(ball, RightNet)',
        goals='At(A, LeftNet) & Returned(ball)',
        actions=[Action('Hit(actor, ball, loc)',
                        precond='Approaching(ball, loc) & At(actor, loc)',
                        effect='Returned(ball)'),
                 Action('Go(actor, to, loc)',
                        precond='At(actor, loc)',
                        effect='At(actor, to) & ~At(actor, loc)')])


def double_tennis_problem():
    """
    [Figure 11.10] DOUBLE-TENNIS-PROBLEM

    A multiagent planning problem involving two partner tennis players
    trying to return an approaching ball and repositioning around in the court.

    Example:
    >>> from planning import *
    >>> dtp = double_tennis_problem()
    >>> goal_test(dtp.goals, dtp.initial)
    False
    >>> dtp.act(expr('Go(A, RightBaseLine, LeftNet)'))
    >>> dtp.act(expr('Hit(A, Ball, RightBaseLine)'))
    >>> goal_test(dtp.goals, dtp.initial)
    False
    >>> dtp.act(expr('Go(A, LeftBaseLine, RightBaseLine)'))
    >>> goal_test(dtp.goals, dtp.initial)
    True
    """

    return PlanningProblem(
        initial='At(A, LeftNet) & At(B, RightNet) & Approaching(Ball, RightBaseLine)',
        goals='At(A, LeftBaseLine) & At(B, LeftNet) & Returned(Ball)',
        actions=[Action('Hit(actor, ball, loc)',
                        precond='Approaching(ball, loc) & At(actor, loc)',
                        effect='Returned(ball)'),
                 Action('Go(actor, to, loc)',
                        precond='At(actor, loc)',
                        effect='At(actor, to) & ~At(actor, loc)')],
        domain="Loc(LeftBaseLine)")

def rush_hour():
    """
    RUSH-HOUR-PROBLEM (Non-Numeric Version)

    A planning problem for the Rush Hour sliding block puzzle. The goal is to
    maneuver the RedCar to the exit. This version uses non-numeric symbols for
    grid positions (e.g., R1, C1) instead of integers.

    This specific instance uses:
    - RedCar (2x1, horizontal) starting at (R3, C1)
    - GreenTruck (3x1, vertical) starting at (R1, C4)
    - BlueCar (2x1, vertical) starting at (R5, C2)
    """
    # Initial state: Define vehicle locations and clear spots using non-numeric identifiers.
    initial_state = 'At(RedCar, R3, C1) & At(GreenTruck, R1, C4) & At(BlueCar, R5, C2) & ' \
                    'IsHorizontal(RedCar) & IsVertical(GreenTruck) & IsVertical(BlueCar) & ' \
                    'Clear(R1, C1) & Clear(R1, C2) & Clear(R1, C3) & Clear(R1, C5) & Clear(R1, C6) & ' \
                    'Clear(R2, C1) & Clear(R2, C2) & Clear(R2, C3) & Clear(R2, C5) & Clear(R2, C6) & ' \
                    'Clear(R3, C3) & Clear(R3, C4) & Clear(R3, C5) & Clear(R3, C6) & ' \
                    'Clear(R4, C1) & Clear(R4, C2) & Clear(R4, C3) & Clear(R4, C4) & Clear(R4, C5) & Clear(R4, C6) & ' \
                    'Clear(R5, C1) & Clear(R5, C3) & Clear(R5, C4) & Clear(R5, C5) & Clear(R5, C6) & ' \
                    'Clear(R6, C1) & Clear(R6, C3) & Clear(R6, C4) & Clear(R6, C5) & Clear(R6, C6)'

    # Goal state: The RedCar's left-most part is at column C5.
    goal_state = 'At(RedCar, R3, C5)'

    # Domain: Define objects, types (Row, Col), and adjacency relationships.
    domain_knowledge = 'Vehicle(RedCar) & Vehicle(GreenTruck) & Vehicle(BlueCar) & ' \
                       'Car(RedCar) & Truck(GreenTruck) & Car(BlueCar) & ' \
                       'Row(R1) & Row(R2) & Row(R3) & Row(R4) & Row(R5) & Row(R6) & ' \
                       'Col(C1) & Col(C2) & Col(C3) & Col(C4) & Col(C5) & Col(C6) & ' \
                       'NextTo(R1, R2) & NextTo(R2, R3) & NextTo(R3, R4) & NextTo(R4, R5) & NextTo(R5, R6) & ' \
                       'NextTo(C1, C2) & NextTo(C2, C3) & NextTo(C3, C4) & NextTo(C4, C5) & NextTo(C5, C6)'

    actions = [
        # --- CAR ACTIONS (length 2) ---
        Action('MoveRightCar(v, r, c1, c2, c3)',
               precond='At(v, r, c1) & Car(v) & IsHorizontal(v) & NextTo(c1, c2) & NextTo(c2, c3) & Clear(r, c3)',
               effect='At(v, r, c2) & ~At(v, r, c1) & Clear(r, c1) & ~Clear(r, c3)',
               domain='Vehicle(v) & Row(r) & Col(c1) & Col(c2) & Col(c3)'),
        Action('MoveLeftCar(v, r, c1, c2, c3)',
               precond='At(v, r, c2) & Car(v) & IsHorizontal(v) & NextTo(c1, c2) & NextTo(c2, c3) & Clear(r, c1)',
               effect='At(v, r, c1) & ~At(v, r, c2) & Clear(r, c3) & ~Clear(r, c1)',
               domain='Vehicle(v) & Row(r) & Col(c1) & Col(c2) & Col(c3)'),
        Action('MoveDownCar(v, r1, r2, r3, c)',
               precond='At(v, r1, c) & Car(v) & IsVertical(v) & NextTo(r1, r2) & NextTo(r2, r3) & Clear(r3, c)',
               effect='At(v, r2, c) & ~At(v, r1, c) & Clear(r1, c) & ~Clear(r3, c)',
               domain='Vehicle(v) & Row(r1) & Row(r2) & Row(r3) & Col(c)'),
        Action('MoveUpCar(v, r1, r2, r3, c)',
               precond='At(v, r2, c) & Car(v) & IsVertical(v) & NextTo(r1, r2) & NextTo(r2, r3) & Clear(r1, c)',
               effect='At(v, r1, c) & ~At(v, r2, c) & Clear(r3, c) & ~Clear(r1, c)',
               domain='Vehicle(v) & Row(r1) & Row(r2) & Row(r3) & Col(c)'),

        # --- TRUCK ACTIONS (length 3) ---
        Action('MoveRightTruck(v, r, c1, c2, c3, c4)',
               precond='At(v, r, c1) & Truck(v) & IsHorizontal(v) & NextTo(c1, c2) & NextTo(c2, c3) & NextTo(c3, c4) & Clear(r, c4)',
               effect='At(v, r, c2) & ~At(v, r, c1) & Clear(r, c1) & ~Clear(r, c4)',
               domain='Vehicle(v) & Row(r) & Col(c1) & Col(c2) & Col(c3) & Col(c4)'),
        Action('MoveLeftTruck(v, r, c1, c2, c3, c4)',
               precond='At(v, r, c2) & Truck(v) & IsHorizontal(v) & NextTo(c1, c2) & NextTo(c2, c3) & NextTo(c3, c4) & Clear(r, c1)',
               effect='At(v, r, c1) & ~At(v, r, c2) & Clear(r, c4) & ~Clear(r, c1)',
               domain='Vehicle(v) & Row(r) & Col(c1) & Col(c2) & Col(c3) & Col(c4)'),
        Action('MoveDownTruck(v, r1, r2, r3, r4, c)',
               precond='At(v, r1, c) & Truck(v) & IsVertical(v) & NextTo(r1, r2) & NextTo(r2, r3) & NextTo(r3, r4) & Clear(r4, c)',
               effect='At(v, r2, c) & ~At(v, r1, c) & Clear(r1, c) & ~Clear(r4, c)',
               domain='Vehicle(v) & Row(r1) & Row(r2) & Row(r3) & Row(r4) & Col(c)'),
        Action('MoveUpTruck(v, r1, r2, r3, r4, c)',
               precond='At(v, r2, c) & Truck(v) & IsVertical(v) & NextTo(r1, r2) & NextTo(r2, r3) & NextTo(r3, r4) & Clear(r1, c)',
               effect='At(v, r1, c) & ~At(v, r2, c) & Clear(r4, c) & ~Clear(r1, c)',
               domain='Vehicle(v) & Row(r1) & Row(r2) & Row(r3) & Row(r4) & Col(c)')
    ]

    return PlanningProblem(initial=initial_state,
                           goals=goal_state,
                           actions=actions,
                           domain=domain_knowledge)


def rush_hour_optimized():
    """
    RUSH-HOUR-PROBLEM (Optimized Version)

    This version optimizes the planning problem by creating vehicle-specific
    actions. Since each vehicle's orientation is fixed, we can remove generic
    predicates like `IsHorizontal` and create actions that only apply to the
    correct vehicle on its fixed axis of movement. This drastically reduces
    the number of permutations the planner needs to generate and check.
    """
    # Initial state is simpler as orientation is now baked into the actions.
    initial_state = 'At(RedCar, R3, C1) & At(GreenTruck, R1, C4) & At(BlueCar, R5, C2) & ' \
                    'Clear(R1, C1) & Clear(R1, C2) & Clear(R1, C3) & Clear(R1, C5) & Clear(R1, C6) & ' \
                    'Clear(R2, C1) & Clear(R2, C2) & Clear(R2, C3) & Clear(R2, C5) & Clear(R2, C6) & ' \
                    'Clear(R3, C3) & Clear(R3, C4) & Clear(R3, C5) & Clear(R3, C6) & ' \
                    'Clear(R4, C1) & Clear(R4, C2) & Clear(R4, C3) & Clear(R4, C4) & Clear(R4, C5) & Clear(R4, C6) & ' \
                    'Clear(R5, C1) & Clear(R5, C3) & Clear(R5, C4) & Clear(R5, C5) & Clear(R5, C6) & ' \
                    'Clear(R6, C1) & Clear(R6, C3) & Clear(R6, C4) & Clear(R6, C5) & Clear(R6, C6)'

    # Goal state remains the same.
    goal_state = 'At(RedCar, R3, C5)'

    # Domain knowledge defines the grid and vehicles.
    domain_knowledge = 'Vehicle(RedCar) & Vehicle(GreenTruck) & Vehicle(BlueCar) & ' \
                       'Row(R1) & Row(R2) & Row(R3) & Row(R4) & Row(R5) & Row(R6) & ' \
                       'Col(C1) & Col(C2) & Col(C3) & Col(C4) & Col(C5) & Col(C6) & ' \
                       'NextTo(R1, R2) & NextTo(R2, R3) & NextTo(R3, R4) & NextTo(R4, R5) & NextTo(R5, R6) & ' \
                       'NextTo(C1, C2) & NextTo(C2, C3) & NextTo(C3, C4) & NextTo(C4, C5) & NextTo(C5, C6)'

    # Optimized Actions: Specific to each vehicle and its fixed orientation.
    actions = [
        # RedCar is horizontal on Row 3, length 2
        Action('MoveRedCarRight(c1, c2, c3)',
               precond='At(RedCar, R3, c1) & NextTo(c1, c2) & NextTo(c2, c3) & Clear(R3, c3)',
               effect='At(RedCar, R3, c2) & ~At(RedCar, R3, c1) & Clear(R3, c1) & ~Clear(R3, c3)',
               domain='Col(c1) & Col(c2) & Col(c3)'),
        Action('MoveRedCarLeft(c1, c2, c3)',
               precond='At(RedCar, R3, c2) & NextTo(c1, c2) & NextTo(c2, c3) & Clear(R3, c1)',
               effect='At(RedCar, R3, c1) & ~At(RedCar, R3, c2) & Clear(R3, c3) & ~Clear(R3, c1)',
               domain='Col(c1) & Col(c2) & Col(c3)'),

        # GreenTruck is vertical on Column 4, length 3
        Action('MoveGreenTruckDown(r1, r2, r3, r4)',
               precond='At(GreenTruck, r1, C4) & NextTo(r1, r2) & NextTo(r2, r3) & NextTo(r3, r4) & Clear(r4, C4)',
               effect='At(GreenTruck, r2, C4) & ~At(GreenTruck, r1, C4) & Clear(r1, C4) & ~Clear(r4, C4)',
               domain='Row(r1) & Row(r2) & Row(r3) & Row(r4)'),
        Action('MoveGreenTruckUp(r1, r2, r3, r4)',
               precond='At(GreenTruck, r2, C4) & NextTo(r1, r2) & NextTo(r2, r3) & NextTo(r3, r4) & Clear(r1, C4)',
               effect='At(GreenTruck, r1, C4) & ~At(GreenTruck, r2, C4) & Clear(r4, C4) & ~Clear(r1, C4)',
               domain='Row(r1) & Row(r2) & Row(r3) & Row(r4)'),

        # BlueCar is vertical on Column 2, length 2
        Action('MoveBlueCarDown(r1, r2, r3)',
               precond='At(BlueCar, r1, C2) & NextTo(r1, r2) & NextTo(r2, r3) & Clear(r3, C2)',
               effect='At(BlueCar, r2, C2) & ~At(BlueCar, r1, C2) & Clear(r1, C2) & ~Clear(r3, C2)',
               domain='Row(r1) & Row(r2) & Row(r3)'),
        Action('MoveBlueCarUp(r1, r2, r3)',
               precond='At(BlueCar, r2, C2) & NextTo(r1, r2) & NextTo(r2, r3) & Clear(r1, C2)',
               effect='At(BlueCar, r1, C2) & ~At(BlueCar, r2, C2) & Clear(r3, C2) & ~Clear(r1, C2)',
               domain='Row(r1) & Row(r2) & Row(r3)'),
    ]

    return PlanningProblem(initial=initial_state,
                           goals=goal_state,
                           actions=actions,
                           domain=domain_knowledge)
    

#### For pytests    
    
def spare_tire_graphPlan():
    """Solves the spare tire problem using GraphPlan"""
    return GraphPlan(spare_tire()).execute()


def three_block_tower_graphPlan():
    """Solves the Sussman Anomaly problem using GraphPlan"""
    return GraphPlan(three_block_tower()).execute()


def air_cargo_graphPlan():
    """Solves the air cargo problem using GraphPlan"""
    return GraphPlan(air_cargo()).execute()


def have_cake_and_eat_cake_too_graphPlan():
    """Solves the cake problem using GraphPlan"""
    return GraphPlan(have_cake_and_eat_cake_too()).execute()


def shopping_graphPlan():
    """Solves the shopping problem using GraphPlan"""
    return GraphPlan(shopping_problem()).execute()


def socks_and_shoes_graphPlan():
    """Solves the socks and shoes problem using GraphPlan"""
    return GraphPlan(socks_and_shoes()).execute()


def simple_blocks_world_graphPlan():
    """Solves the simple blocks world problem"""
    return GraphPlan(simple_blocks_world()).execute()
