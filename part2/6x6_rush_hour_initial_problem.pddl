;--------------------------------------------------------------------------------------------------------


;MERGED FEATURES IN PDDL (PROBLEM FILE) VER. 1: OPTIMIZING FEAT1VER1 AND FEAT2VER1'S 6X6 GRID & MULTISTEP ACTIONS
;References: https://fareskalaboud.github.io/LearnPDDL/, https://editor.planning.domains/#
;Debugging the features and changing representation/configuration using PDDL and LLM suggestions
;No runner for any configuration yet

;From here, I need to create another problem .pddl file to better represent the better, updated domain .pddl file


;--------------------------------------------------------------------------------------------------------

(define (problem rushhour-simple)
  (:domain rush-hour)
  
  (:objects
    R A B - car
    T1 T2 - truck
    C1_1 C1_2 C1_3 C1_4 C1_5 C1_6 C2_1 C2_2 C2_3 C2_4 C2_5 C2_6 C3_1 C3_2 C3_3 C3_4 C3_5 C3_6 C4_1 C4_2 C4_3 C4_4 C4_5 C4_6 C5_1 C5_2 C5_3 C5_4 C5_5 C5_6 C6_1 C6_2 C6_3 C6_4 C6_5 C6_6 - cell
  )
  
  (:init
    (at R C3_1)
    (horizontal R)    
    (at A C1_1)
    (horizontal A)
    (at B C4_3)
    (vertical B)
    (occupies T1 C3_2)
    (occupies T1 C4_2)
    (vertical T1)
    (occupies T2 C2_3)
    (occupies T2 C3_3)
    (vertical T2)
    (clear C1_2) (clear C1_3) (clear C1_4) (clear C1_5) (clear C1_6)
    (clear C2_1) (clear C2_2) (clear C2_4) (clear C2_5) (clear C2_6)
    (clear C3_4) (clear C3_5) (clear C3_6)
    (clear C4_1) (clear C4_4) (clear C4_5) (clear C4_6)
    (clear C5_1) (clear C5_2) (clear C5_3) (clear C5_4) (clear C5_5) (clear C5_6)
    (clear C6_1) (clear C6_2) (clear C6_3) (clear C6_4) (clear C6_5) (clear C6_6)
    (adjacent-right C1_1 C1_2) (adjacent-right C1_2 C1_3) (adjacent-right C1_3 C1_4) (adjacent-right C1_4 C1_5) (adjacent-right C1_5 C1_6)
    (adjacent-right C2_1 C2_2) (adjacent-right C2_2 C2_3) (adjacent-right C2_3 C2_4) (adjacent-right C2_4 C2_5) (adjacent-right C2_5 C2_6)
    (adjacent-right C3_1 C3_2) (adjacent-right C3_2 C3_3) (adjacent-right C3_3 C3_4) (adjacent-right C3_4 C3_5) (adjacent-right C3_5 C3_6)
    (adjacent-right C4_1 C4_2) (adjacent-right C4_2 C4_3) (adjacent-right C4_3 C4_4) (adjacent-right C4_4 C4_5) (adjacent-right C4_5 C4_6)
    (adjacent-right C5_1 C5_2) (adjacent-right C5_2 C5_3) (adjacent-right C5_3 C5_4) (adjacent-right C5_4 C5_5) (adjacent-right C5_5 C5_6)
    (adjacent-right C6_1 C6_2) (adjacent-right C6_2 C6_3) (adjacent-right C6_3 C6_4) (adjacent-right C6_4 C6_5) (adjacent-right C6_5 C6_6)
    (adjacent-left C1_2 C1_1) (adjacent-left C1_3 C1_2) (adjacent-left C1_4 C1_3) (adjacent-left C1_5 C1_4) (adjacent-left C1_6 C1_5)
    (adjacent-left C2_2 C2_1) (adjacent-left C2_3 C2_2) (adjacent-left C2_4 C2_3) (adjacent-left C2_5 C2_4) (adjacent-left C2_6 C2_5)
    (adjacent-left C3_2 C3_1) (adjacent-left C3_3 C3_2) (adjacent-left C3_4 C3_3) (adjacent-left C3_5 C3_4) (adjacent-left C3_6 C3_5)
    (adjacent-left C4_2 C4_1) (adjacent-left C4_3 C4_2) (adjacent-left C4_4 C4_3) (adjacent-left C4_5 C4_4) (adjacent-left C4_6 C4_5)
    (adjacent-left C5_2 C5_1) (adjacent-left C5_3 C5_2) (adjacent-left C5_4 C5_3) (adjacent-left C5_5 C5_4) (adjacent-left C5_6 C5_5)
    (adjacent-left C6_2 C6_1) (adjacent-left C6_3 C6_2) (adjacent-left C6_4 C6_3) (adjacent-left C6_5 C6_4) (adjacent-left C6_6 C6_5)
    (adjacent-down C1_1 C2_1) (adjacent-down C2_1 C3_1) (adjacent-down C3_1 C4_1) (adjacent-down C4_1 C5_1) (adjacent-down C5_1 C6_1)
    (adjacent-down C1_2 C2_2) (adjacent-down C2_2 C3_2) (adjacent-down C3_2 C4_2) (adjacent-down C4_2 C5_2) (adjacent-down C5_2 C6_2)
    (adjacent-down C1_3 C2_3) (adjacent-down C2_3 C3_3) (adjacent-down C3_3 C4_3) (adjacent-down C4_3 C5_3) (adjacent-down C5_3 C6_3)
    (adjacent-down C1_4 C2_4) (adjacent-down C2_4 C3_4) (adjacent-down C3_4 C4_4) (adjacent-down C4_4 C5_4) (adjacent-down C5_4 C6_4)
    (adjacent-down C1_5 C2_5) (adjacent-down C2_5 C3_5) (adjacent-down C3_5 C4_5) (adjacent-down C4_5 C5_5) (adjacent-down C5_5 C6_5)
    (adjacent-down C1_6 C2_6) (adjacent-down C2_6 C3_6) (adjacent-down C3_6 C4_6) (adjacent-down C4_6 C5_6) (adjacent-down C5_6 C6_6)
    (adjacent-up C2_1 C1_1) (adjacent-up C3_1 C2_1) (adjacent-up C4_1 C3_1) (adjacent-up C5_1 C4_1) (adjacent-up C6_1 C5_1)
    (adjacent-up C2_2 C1_2) (adjacent-up C3_2 C2_2) (adjacent-up C4_2 C3_2) (adjacent-up C5_2 C4_2) (adjacent-up C6_2 C5_2)
    (adjacent-up C2_3 C1_3) (adjacent-up C3_3 C2_3) (adjacent-up C4_3 C3_3) (adjacent-up C5_3 C4_3) (adjacent-up C6_3 C5_3)
    (adjacent-up C2_4 C1_4) (adjacent-up C3_4 C2_4) (adjacent-up C4_4 C3_4) (adjacent-up C5_4 C4_4) (adjacent-up C6_4 C5_4)
    (adjacent-up C2_5 C1_5) (adjacent-up C3_5 C2_5) (adjacent-up C4_5 C3_5) (adjacent-up C5_5 C4_5) (adjacent-up C6_5 C5_5)
    (adjacent-up C2_6 C1_6) (adjacent-up C3_6 C2_6) (adjacent-up C4_6 C3_6) (adjacent-up C5_6 C4_6) (adjacent-up C6_6 C5_6)
  )
  
  (:goal
    (and
      (at R C3_6)
      (occupies T1 C1_2)
      (occupies T1 C2_2)
    )
  )
)