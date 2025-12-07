def compare_6x6():
    #4x4 Grid Partially Ordered & Linearized Plan
    #I'M ASSUMING P MEANS PRECONDITION???
    set1 = set(["PCell(C3_2)", "PCell(C3_4)", "PAdjacentRight(C3_2, C3_3)", "PCell(C1_2)", "PCell(C2_2)", "PAdjacentDown(C2_2, C3_2)", "PCell(C3_1)", "PHorizontal(R)", "PVertical(T1)", "PCar(R)", "PAt(R, C3_1)", "TruckMoveUp(T1, C3_2, C4_2, C2_2)", "TruckMoveUp(T2, C2_3, C3_3, C1_3)", "PClear(C1_2)", "PClear(C3_4)", "PAdjacentRight(C3_3, C3_4)", "PCell(C3_3)", "PAdjacentUp(C2_2, C1_2)", "PTruck(T1)", "PAdjacentRight(C3_1, C3_2)"])
    set2 = set(["PCell(C3_2)", "PCell(C3_4)", "PCell(C3_1)", "PAdjacentRight(C3_2, C3_3)", "PAdjacentRight(C3_3, C3_4)", "PCell(C3_3)", "PClear(C3_3)", "TruckMoveUp(T1, C2_2, C3_2, C1_2)", "PHorizontal(R)", "PCar(R)", "PAt(R, C3_1)", "PAdjacentRight(C3_1, C3_2)", "PClear(C3_4)"])
    set3 = set(["PAtFront(T1, C2_2)", "PCell(C3_4)", "PCell(C3_2)", "PAdjacentRight(C3_3, C3_4)", "PAdjacentRight(C3_2, C3_3)", "MoveRight(R, C3_1, C3_2)", "PAtRear(T1, C1_2)", "PCell(C3_3)", "PHorizontal(R)", "PCar(R)", "PClear(C3_3)", "PClear(C3_4)"])
    set4 = set(["PAtFront(T1, C2_2)", "PCell(C3_4)", "PAdjacentRight(C3_3, C3_4)", "PAtRear(T1, C1_2)", "MoveRight(R, C3_2, C3_3)", "PCell(C3_3)", "PHorizontal(R)", "PCar(R)", "PClear(C3_4)"])
    set5 = set(["MoveRight(R, C3_3, C3_4)", "PAtFront(T1, C2_2)", "PAtRear(T1, C1_2)"])
    finalans = set(["TruckMoveUp(T1, C3_2, C4_2, C2_2)", "TruckMoveUp(T2, C2_3, C3_3, C1_3)", "TruckMoveUp(T1, C2_2, C3_2, C1_2)", "MoveRight(R, C3_1, C3_2)", "MoveRight(R, C3_2, C3_3)", "MoveRight(R, C3_3, C3_4)"])

    #6x6 Grid Partially Ordered & Linearized Plan
    #I'M ASSUMING P MEANS PRECONDITION???
    set6 = set(["PVertical(T1)", "PAdjacentUp(C2_2, C1_2)", "PTruck(T1)", "PCell(C3_2)", "PAdjacentRight(C3_2, C3_3)", "PCell(C2_2)", "PCell(C3_4)", "PHorizontal(R)", "PClear(C1_2)", "PAdjacentRight(C3_3, C3_4)", "TruckMoveUp(T2, C3_3, C2_3, C1_3)", "PClear(C3_4)", "POccupies(T1, C3_2)", "PCell(C1_2)", "TruckMoveUp(T1, C4_2, C3_2, C2_2)", "PAt(R, C3_1)", "PCell(C3_1)", "PCell(C3_3)", "PCar(R)", "PAdjacentRight(C3_1, C3_2)"])
    set7 = set(["PCell(C3_4)", "PHorizontal(R)", "PCell(C3_2)", "PAdjacentRight(C3_3, C3_4)", "PClear(C3_3)", "PAt(R, C3_1)", "PCar(R)", "PCell(C3_1)", "TruckMoveUp(T1, C3_2, C2_2, C1_2)", "PClear(C3_4)", "PAdjacentRight(C3_1, C3_2)", "PAdjacentRight(C3_2, C3_3)", "POccupies(T1, C2_2)", "PCell(C3_3)"])
    set8 = set(["PCell(C3_4)", "PHorizontal(R)", "CarMoveRight(R, C3_1, C3_2)", "PAdjacentRight(C3_3, C3_4)", "PClear(C3_3)", "PCar(R)", "POccupies(T1, C1_2)", "PClear(C3_4)", "PCell(C3_2)", "PAdjacentRight(C3_2, C3_3)", "POccupies(T1, C2_2)", "PCell(C3_3)"])
    set9 = set(["PCell(C3_4)", "PHorizontal(R)", "CarMoveRight(R, C3_2, C3_3)", "PAdjacentRight(C3_3, C3_4)", "PCar(R)", "POccupies(T1, C1_2)", "PClear(C3_4)", "POccupies(T1, C2_2)", "PCell(C3_3)"])
    set10 = set(["POccupies(T1, C1_2)", "POccupies(T1, C2_2)", "CarMoveRight(R, C3_3, C3_4)"]) 
    finalans2 = set(["TruckMoveUp(T2, C3_3, C2_3, C1_3)", "TruckMoveUp(T1, C4_2, C3_2, C2_2)", "TruckMoveUp(T1, C3_2, C2_2, C1_2)", "CarMoveRight(R, C3_1, C3_2)", "CarMoveRight(R, C3_2, C3_3)", "CarMoveRight(R, C3_3, C3_4)"])

    print(f"\n{set1 ^ set6}")
    print(f"\n{set2 ^ set7}")
    print(f"\n{set3 ^ set8}")
    print(f"\n{set4 ^ set9}")
    print(f"\n{finalans ^ finalans2}")
    print("These are example outputs from the same problem run on a 4x4 and 6x6 grid.")
    print("Upon manual inspection, the preconditions for the Partially-Ordered Plan are mostly the same besides lexical syntax as well as order of head/tail blocks.")
    print("Similarly, the linearized plan is exactly same besides lexical syntax and order of head/tail blocks.")