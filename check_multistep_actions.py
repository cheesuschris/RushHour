def compare_multistep():
    #Normal 4x4 Grid Partially Ordered & Linearized Plan
    #I'M ASSUMING P MEANS PRECONDITION
    set1 = set(["PCell(C3_2)", "PCell(C3_4)", "PAdjacentRight(C3_2, C3_3)", "PCell(C1_2)", "PCell(C2_2)", "PAdjacentDown(C2_2, C3_2)", "PCell(C3_1)", "PHorizontal(R)", "PVertical(T1)", "PCar(R)", "PAt(R, C3_1)", "TruckMoveUp(T1, C3_2, C4_2, C2_2)", "TruckMoveUp(T2, C2_3, C3_3, C1_3)", "PClear(C1_2)", "PClear(C3_4)", "PAdjacentRight(C3_3, C3_4)", "PCell(C3_3)", "PAdjacentUp(C2_2, C1_2)", "PTruck(T1)", "PAdjacentRight(C3_1, C3_2)"])
    set2 = set(["PCell(C3_2)", "PCell(C3_4)", "PCell(C3_1)", "PAdjacentRight(C3_2, C3_3)", "PAdjacentRight(C3_3, C3_4)", "PCell(C3_3)", "PClear(C3_3)", "TruckMoveUp(T1, C2_2, C3_2, C1_2)", "PHorizontal(R)", "PCar(R)", "PAt(R, C3_1)", "PAdjacentRight(C3_1, C3_2)", "PClear(C3_4)"])
    set3 = set(["PAtFront(T1, C2_2)", "PCell(C3_4)", "PCell(C3_2)", "PAdjacentRight(C3_3, C3_4)", "PAdjacentRight(C3_2, C3_3)", "MoveRight(R, C3_1, C3_2)", "PAtRear(T1, C1_2)", "PCell(C3_3)", "PHorizontal(R)", "PCar(R)", "PClear(C3_3)", "PClear(C3_4)"])
    set4 = set(["PAtFront(T1, C2_2)", "PCell(C3_4)", "PAdjacentRight(C3_3, C3_4)", "PAtRear(T1, C1_2)", "MoveRight(R, C3_2, C3_3)", "PCell(C3_3)", "PHorizontal(R)", "PCar(R)", "PClear(C3_4)"])
    set5 = set(["MoveRight(R, C3_3, C3_4)", "PAtFront(T1, C2_2)", "PAtRear(T1, C1_2)"])
    finalans = set(["TruckMoveUp(T1, C3_2, C4_2, C2_2)", "TruckMoveUp(T2, C2_3, C3_3, C1_3)", "TruckMoveUp(T1, C2_2, C3_2, C1_2)", "MoveRight(R, C3_1, C3_2)", "MoveRight(R, C3_2, C3_3)", "MoveRight(R, C3_3, C3_4)"])

    #MultiStep Action Partially Ordered & Linearized Plan
    #I'M ASSUMING P MEANS PRECONDITION
    set6 = set(["PCell(C3_4)", "PAt(R, C3_1)", "PAdjacentRight(C3_3, C3_4)", "PCell(C3_3)", "PCell(C3_1)", "PHorizontal(R)", "PCell(C3_2)", "PAdjacentRight(C3_2, C3_3)", "PCar(R)", "PAdjacentRight(C3_1, C3_2)", "PClear(C3_4)", "TruckMoveUpTwo(T1, C4_2, C3_2, C2_2, C1_2)", "TruckMoveUp(T2, C3_3, C2_3, C1_3)"])
    set7 = set(["POccupies(T1, C2_2)", "CarMoveRightThree(R, C3_1, C3_2, C3_3, C3_4)", "POccupies(T1, C1_2)"])
    finalans2 = set(["TruckMoveUpTwo(T1, C4_2, C3_2, C2_2, C1_2)", "TruckMoveUp(T2, C3_3, C2_3, C1_3)", "CarMoveRightThree(R, C3_1, C3_2, C3_3, C3_4)"])

    print(f"\n{set1 ^ set6}")
    print(f"\n{set2 ^ set7}")
    print(f"\n{finalans ^ finalans2}")
    print("These are example outputs from the same problem run on a normal and multistep action grid.")
    print("Upon manual inspection, it seems that the search tree actually arrives at a decision earlier because there is less")
    print("actions to take and nodes searched in the multistep-action version.")
    print("The partially ordered plans reveal a lot less actions taken and nodes searched in multistep actions than normal actions.")
    print("The linearized plan is the exact same but different lexical syntax and costs less moves.")