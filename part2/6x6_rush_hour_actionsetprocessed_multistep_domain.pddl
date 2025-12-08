;--------------------------------------------------------------------------------------------------------


;MERGED FEATURES IN PDDL (DOMAIN FILE) VER. 3: TAKING DOMAIN PDDL VER. 1 & OPTIMIZING & SEARCH TREE MULTI-STEP ACTIONS
;References: https://fareskalaboud.github.io/LearnPDDL/, https://editor.planning.domains/#
;Debugging the features and changing representation/configuration using PDDL and LLM suggestions: just added multi-step actions
;No runner for any configuration yet

;From here, I need to convert this optimized version (w/ multi-step actions in search tree) back to 
;mergedfeatsver3 file in python


;--------------------------------------------------------------------------------------------------------

(define (domain rush-hour)
  (:requirements :typing :equality)
  
  (:types
    vehicle row col - object
    car truck - vehicle
  )
  
  (:predicates
    (at-horizontal ?v - vehicle ?r - row ?c - col)
    (at-vertical ?v - vehicle ?r - row ?c - col)
    (clear ?r - row ?c - col)
    (next-col ?c1 - col ?c2 - col) 
    (next-row ?r1 - row ?r2 - row) 
  )

  (:action car-move-right-1
    :parameters (?c - car ?r - row ?p1 ?p2 - col)
    :precondition (and (at-horizontal ?c ?r ?p1) (next-col ?p1 ?p2) (clear ?r ?p2))
    :effect (and (not (at-horizontal ?c ?r ?p1)) (at-horizontal ?c ?r ?p2) (clear ?r ?p1) (not (clear ?r ?p2)))
  )

  (:action car-move-right-2
    :parameters (?c - car ?r - row ?p1 ?p2 ?p3 - col)
    :precondition (and (at-horizontal ?c ?r ?p1) (next-col ?p1 ?p2) (next-col ?p2 ?p3) (clear ?r ?p2) (clear ?r ?p3))
    :effect (and (not (at-horizontal ?c ?r ?p1)) (at-horizontal ?c ?r ?p3) (clear ?r ?p1) (not (clear ?r ?p3)))
  )

  (:action car-move-right-3
    :parameters (?c - car ?r - row ?p1 ?p2 ?p3 ?p4 - col)
    :precondition (and (at-horizontal ?c ?r ?p1) (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) 
                       (clear ?r ?p2) (clear ?r ?p3) (clear ?r ?p4))
    :effect (and (not (at-horizontal ?c ?r ?p1)) (at-horizontal ?c ?r ?p4) (clear ?r ?p1) (not (clear ?r ?p4)))
  )

  (:action car-move-right-4
    :parameters (?c - car ?r - row ?p1 ?p2 ?p3 ?p4 ?p5 - col)
    :precondition (and (at-horizontal ?c ?r ?p1) (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) (next-col ?p4 ?p5)
                       (clear ?r ?p2) (clear ?r ?p3) (clear ?r ?p4) (clear ?r ?p5))
    :effect (and (not (at-horizontal ?c ?r ?p1)) (at-horizontal ?c ?r ?p5) (clear ?r ?p1) (not (clear ?r ?p5)))
  )

  (:action car-move-right-5
    :parameters (?c - car ?r - row ?p1 ?p2 ?p3 ?p4 ?p5 ?p6 - col)
    :precondition (and (at-horizontal ?c ?r ?p1) (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) (next-col ?p4 ?p5) (next-col ?p5 ?p6)
                       (clear ?r ?p2) (clear ?r ?p3) (clear ?r ?p4) (clear ?r ?p5) (clear ?r ?p6))
    :effect (and (not (at-horizontal ?c ?r ?p1)) (at-horizontal ?c ?r ?p6) (clear ?r ?p1) (not (clear ?r ?p6)))
  )

  (:action car-move-left-1
    :parameters (?c - car ?r - row ?p2 ?p1 - col)
    :precondition (and (at-horizontal ?c ?r ?p2) (next-col ?p1 ?p2) (clear ?r ?p1))
    :effect (and (not (at-horizontal ?c ?r ?p2)) (at-horizontal ?c ?r ?p1) (clear ?r ?p2) (not (clear ?r ?p1)))
  )

  (:action car-move-left-2
    :parameters (?c - car ?r - row ?p3 ?p2 ?p1 - col)
    :precondition (and (at-horizontal ?c ?r ?p3) (next-col ?p1 ?p2) (next-col ?p2 ?p3) (clear ?r ?p2) (clear ?r ?p1))
    :effect (and (not (at-horizontal ?c ?r ?p3)) (at-horizontal ?c ?r ?p1) (clear ?r ?p3) (not (clear ?r ?p1)))
  )

  (:action car-move-left-3
    :parameters (?c - car ?r - row ?p4 ?p3 ?p2 ?p1 - col)
    :precondition (and (at-horizontal ?c ?r ?p4) (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) 
                       (clear ?r ?p3) (clear ?r ?p2) (clear ?r ?p1))
    :effect (and (not (at-horizontal ?c ?r ?p4)) (at-horizontal ?c ?r ?p1) (clear ?r ?p4) (not (clear ?r ?p1)))
  )

  (:action car-move-left-4
    :parameters (?c - car ?r - row ?p5 ?p4 ?p3 ?p2 ?p1 - col)
    :precondition (and (at-horizontal ?c ?r ?p5) (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) (next-col ?p4 ?p5)
                       (clear ?r ?p4) (clear ?r ?p3) (clear ?r ?p2) (clear ?r ?p1))
    :effect (and (not (at-horizontal ?c ?r ?p5)) (at-horizontal ?c ?r ?p1) (clear ?r ?p5) (not (clear ?r ?p1)))
  )

  (:action car-move-left-5
    :parameters (?c - car ?r - row ?p6 ?p5 ?p4 ?p3 ?p2 ?p1 - col)
    :precondition (and (at-horizontal ?c ?r ?p6) (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) (next-col ?p4 ?p5) (next-col ?p5 ?p6)
                       (clear ?r ?p5) (clear ?r ?p4) (clear ?r ?p3) (clear ?r ?p2) (clear ?r ?p1))
    :effect (and (not (at-horizontal ?c ?r ?p6)) (at-horizontal ?c ?r ?p1) (clear ?r ?p6) (not (clear ?r ?p1)))
  )

  (:action car-move-down-1
    :parameters (?c - car ?c_idx - col ?p1 ?p2 - row)
    :precondition (and (at-vertical ?c ?p1 ?c_idx) (next-row ?p1 ?p2) (clear ?p2 ?c_idx))
    :effect (and (not (at-vertical ?c ?p1 ?c_idx)) (at-vertical ?c ?p2 ?c_idx) (clear ?p1 ?c_idx) (not (clear ?p2 ?c_idx)))
  )

  (:action car-move-down-2
    :parameters (?c - car ?c_idx - col ?p1 ?p2 ?p3 - row)
    :precondition (and (at-vertical ?c ?p1 ?c_idx) (next-row ?p1 ?p2) (next-row ?p2 ?p3) (clear ?p2 ?c_idx) (clear ?p3 ?c_idx))
    :effect (and (not (at-vertical ?c ?p1 ?c_idx)) (at-vertical ?c ?p3 ?c_idx) (clear ?p1 ?c_idx) (not (clear ?p3 ?c_idx)))
  )

  (:action car-move-down-3
    :parameters (?c - car ?c_idx - col ?p1 ?p2 ?p3 ?p4 - row)
    :precondition (and (at-vertical ?c ?p1 ?c_idx) (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4)
                       (clear ?p2 ?c_idx) (clear ?p3 ?c_idx) (clear ?p4 ?c_idx))
    :effect (and (not (at-vertical ?c ?p1 ?c_idx)) (at-vertical ?c ?p4 ?c_idx) (clear ?p1 ?c_idx) (not (clear ?p4 ?c_idx)))
  )

  (:action car-move-down-4
    :parameters (?c - car ?c_idx - col ?p1 ?p2 ?p3 ?p4 ?p5 - row)
    :precondition (and (at-vertical ?c ?p1 ?c_idx) (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4) (next-row ?p4 ?p5)
                       (clear ?p2 ?c_idx) (clear ?p3 ?c_idx) (clear ?p4 ?c_idx) (clear ?p5 ?c_idx))
    :effect (and (not (at-vertical ?c ?p1 ?c_idx)) (at-vertical ?c ?p5 ?c_idx) (clear ?p1 ?c_idx) (not (clear ?p5 ?c_idx)))
  )

  (:action car-move-down-5
    :parameters (?c - car ?c_idx - col ?p1 ?p2 ?p3 ?p4 ?p5 ?p6 - row)
    :precondition (and (at-vertical ?c ?p1 ?c_idx) (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4) (next-row ?p4 ?p5) (next-row ?p5 ?p6)
                       (clear ?p2 ?c_idx) (clear ?p3 ?c_idx) (clear ?p4 ?c_idx) (clear ?p5 ?c_idx) (clear ?p6 ?c_idx))
    :effect (and (not (at-vertical ?c ?p1 ?c_idx)) (at-vertical ?c ?p6 ?c_idx) (clear ?p1 ?c_idx) (not (clear ?p6 ?c_idx)))
  )

  (:action car-move-up-1
    :parameters (?c - car ?c_idx - col ?p2 ?p1 - row)
    :precondition (and (at-vertical ?c ?p2 ?c_idx) (next-row ?p1 ?p2) (clear ?p1 ?c_idx))
    :effect (and (not (at-vertical ?c ?p2 ?c_idx)) (at-vertical ?c ?p1 ?c_idx) (clear ?p2 ?c_idx) (not (clear ?p1 ?c_idx)))
  )

  (:action car-move-up-2
    :parameters (?c - car ?c_idx - col ?p3 ?p2 ?p1 - row)
    :precondition (and (at-vertical ?c ?p3 ?c_idx) (next-row ?p1 ?p2) (next-row ?p2 ?p3) (clear ?p2 ?c_idx) (clear ?p1 ?c_idx))
    :effect (and (not (at-vertical ?c ?p3 ?c_idx)) (at-vertical ?c ?p1 ?c_idx) (clear ?p3 ?c_idx) (not (clear ?p1 ?c_idx)))
  )

  (:action car-move-up-3
    :parameters (?c - car ?c_idx - col ?p4 ?p3 ?p2 ?p1 - row)
    :precondition (and (at-vertical ?c ?p4 ?c_idx) (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4)
                       (clear ?p3 ?c_idx) (clear ?p2 ?c_idx) (clear ?p1 ?c_idx))
    :effect (and (not (at-vertical ?c ?p4 ?c_idx)) (at-vertical ?c ?p1 ?c_idx) (clear ?p4 ?c_idx) (not (clear ?p1 ?c_idx)))
  )

  (:action car-move-up-4
    :parameters (?c - car ?c_idx - col ?p5 ?p4 ?p3 ?p2 ?p1 - row)
    :precondition (and (at-vertical ?c ?p5 ?c_idx) (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4) (next-row ?p4 ?p5)
                       (clear ?p4 ?c_idx) (clear ?p3 ?c_idx) (clear ?p2 ?c_idx) (clear ?p1 ?c_idx))
    :effect (and (not (at-vertical ?c ?p5 ?c_idx)) (at-vertical ?c ?p1 ?c_idx) (clear ?p5 ?c_idx) (not (clear ?p1 ?c_idx)))
  )

  (:action car-move-up-5
    :parameters (?c - car ?c_idx - col ?p6 ?p5 ?p4 ?p3 ?p2 ?p1 - row)
    :precondition (and (at-vertical ?c ?p6 ?c_idx) (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4) (next-row ?p4 ?p5) (next-row ?p5 ?p6)
                       (clear ?p5 ?c_idx) (clear ?p4 ?c_idx) (clear ?p3 ?c_idx) (clear ?p2 ?c_idx) (clear ?p1 ?c_idx))
    :effect (and (not (at-vertical ?c ?p6 ?c_idx)) (at-vertical ?c ?p1 ?c_idx) (clear ?p6 ?c_idx) (not (clear ?p1 ?c_idx)))
  )

  (:action truck-move-right-1
    :parameters (?t - truck ?r - row ?p1 ?p2 ?p3 - col)
    :precondition (and (at-horizontal ?t ?r ?p1) (at-horizontal ?t ?r ?p2)
                       (next-col ?p1 ?p2) (next-col ?p2 ?p3)
                       (clear ?r ?p3))
    :effect (and (not (at-horizontal ?t ?r ?p1)) (at-horizontal ?t ?r ?p3) 
                 (clear ?r ?p1) (not (clear ?r ?p3)))
  )

  (:action truck-move-right-2
    :parameters (?t - truck ?r - row ?p1 ?p2 ?p3 ?p4 - col)
    :precondition (and (at-horizontal ?t ?r ?p1) (at-horizontal ?t ?r ?p2)
                       (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4)
                       (clear ?r ?p3) (clear ?r ?p4))
    :effect (and (not (at-horizontal ?t ?r ?p1)) (not (at-horizontal ?t ?r ?p2))
                 (at-horizontal ?t ?r ?p3) (at-horizontal ?t ?r ?p4)
                 (clear ?r ?p1) (clear ?r ?p2)
                 (not (clear ?r ?p3)) (not (clear ?r ?p4)))
  )

  (:action truck-move-right-3
    :parameters (?t - truck ?r - row ?p1 ?p2 ?p3 ?p4 ?p5 - col)
    :precondition (and (at-horizontal ?t ?r ?p1) (at-horizontal ?t ?r ?p2)
                       (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) (next-col ?p4 ?p5)
                       (clear ?r ?p3) (clear ?r ?p4) (clear ?r ?p5))
    :effect (and (not (at-horizontal ?t ?r ?p1)) (not (at-horizontal ?t ?r ?p2))
                 (at-horizontal ?t ?r ?p4) (at-horizontal ?t ?r ?p5)
                 (clear ?r ?p1) (clear ?r ?p2)
                 (not (clear ?r ?p4)) (not (clear ?r ?p5)))
  )

  (:action truck-move-right-4
    :parameters (?t - truck ?r - row ?p1 ?p2 ?p3 ?p4 ?p5 ?p6 - col)
    :precondition (and (at-horizontal ?t ?r ?p1) (at-horizontal ?t ?r ?p2)
                       (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) (next-col ?p4 ?p5) (next-col ?p5 ?p6)
                       (clear ?r ?p3) (clear ?r ?p4) (clear ?r ?p5) (clear ?r ?p6))
    :effect (and (not (at-horizontal ?t ?r ?p1)) (not (at-horizontal ?t ?r ?p2))
                 (at-horizontal ?t ?r ?p5) (at-horizontal ?t ?r ?p6)
                 (clear ?r ?p1) (clear ?r ?p2)
                 (not (clear ?r ?p5)) (not (clear ?r ?p6)))
  )

  (:action truck-move-left-1
    :parameters (?t - truck ?r - row ?p1 ?p2 ?p3 - col)
    :precondition (and (at-horizontal ?t ?r ?p2) (at-horizontal ?t ?r ?p3)
                       (next-col ?p1 ?p2) (next-col ?p2 ?p3)
                       (clear ?r ?p1))
    :effect (and (not (at-horizontal ?t ?r ?p3)) (at-horizontal ?t ?r ?p1) 
                 (clear ?r ?p3) (not (clear ?r ?p1)))
  )

  (:action truck-move-left-2
    :parameters (?t - truck ?r - row ?p1 ?p2 ?p3 ?p4 - col)
    :precondition (and (at-horizontal ?t ?r ?p3) (at-horizontal ?t ?r ?p4)
                       (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4)
                       (clear ?r ?p1) (clear ?r ?p2))
    :effect (and (not (at-horizontal ?t ?r ?p3)) (not (at-horizontal ?t ?r ?p4))
                 (at-horizontal ?t ?r ?p1) (at-horizontal ?t ?r ?p2)
                 (clear ?r ?p3) (clear ?r ?p4)
                 (not (clear ?r ?p1)) (not (clear ?r ?p2)))
  )

  (:action truck-move-left-3
    :parameters (?t - truck ?r - row ?p1 ?p2 ?p3 ?p4 ?p5 - col)
    :precondition (and (at-horizontal ?t ?r ?p4) (at-horizontal ?t ?r ?p5)
                       (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) (next-col ?p4 ?p5)
                       (clear ?r ?p1) (clear ?r ?p2) (clear ?r ?p3))
    :effect (and (not (at-horizontal ?t ?r ?p4)) (not (at-horizontal ?t ?r ?p5))
                 (at-horizontal ?t ?r ?p1) (at-horizontal ?t ?r ?p2)
                 (clear ?r ?p4) (clear ?r ?p5)
                 (not (clear ?r ?p1)) (not (clear ?r ?p2)))
  )

  (:action truck-move-left-4
    :parameters (?t - truck ?r - row ?p1 ?p2 ?p3 ?p4 ?p5 ?p6 - col)
    :precondition (and (at-horizontal ?t ?r ?p5) (at-horizontal ?t ?r ?p6)
                       (next-col ?p1 ?p2) (next-col ?p2 ?p3) (next-col ?p3 ?p4) (next-col ?p4 ?p5) (next-col ?p5 ?p6)
                       (clear ?r ?p1) (clear ?r ?p2) (clear ?r ?p3) (clear ?r ?p4))
    :effect (and (not (at-horizontal ?t ?r ?p5)) (not (at-horizontal ?t ?r ?p6))
                 (at-horizontal ?t ?r ?p1) (at-horizontal ?t ?r ?p2)
                 (clear ?r ?p5) (clear ?r ?p6)
                 (not (clear ?r ?p1)) (not (clear ?r ?p2)))
  )

  (:action truck-move-down-1
    :parameters (?t - truck ?c_idx - col ?p1 ?p2 ?p3 - row)
    :precondition (and (at-vertical ?t ?p1 ?c_idx) (at-vertical ?t ?p2 ?c_idx)
                       (next-row ?p1 ?p2) (next-row ?p2 ?p3)
                       (clear ?p3 ?c_idx))
    :effect (and (not (at-vertical ?t ?p1 ?c_idx)) (at-vertical ?t ?p3 ?c_idx)
                 (clear ?p1 ?c_idx) (not (clear ?p3 ?c_idx)))
  )

  (:action truck-move-down-2
    :parameters (?t - truck ?c_idx - col ?p1 ?p2 ?p3 ?p4 - row)
    :precondition (and (at-vertical ?t ?p1 ?c_idx) (at-vertical ?t ?p2 ?c_idx)
                       (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4)
                       (clear ?p3 ?c_idx) (clear ?p4 ?c_idx))
    :effect (and (not (at-vertical ?t ?p1 ?c_idx)) (not (at-vertical ?t ?p2 ?c_idx))
                 (at-vertical ?t ?p3 ?c_idx) (at-vertical ?t ?p4 ?c_idx)
                 (clear ?p1 ?c_idx) (clear ?p2 ?c_idx)
                 (not (clear ?p3 ?c_idx)) (not (clear ?p4 ?c_idx)))
  )

  (:action truck-move-down-3
    :parameters (?t - truck ?c_idx - col ?p1 ?p2 ?p3 ?p4 ?p5 - row)
    :precondition (and (at-vertical ?t ?p1 ?c_idx) (at-vertical ?t ?p2 ?c_idx)
                       (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4) (next-row ?p4 ?p5)
                       (clear ?p3 ?c_idx) (clear ?p4 ?c_idx) (clear ?p5 ?c_idx))
    :effect (and (not (at-vertical ?t ?p1 ?c_idx)) (not (at-vertical ?t ?p2 ?c_idx))
                 (at-vertical ?t ?p4 ?c_idx) (at-vertical ?t ?p5 ?c_idx)
                 (clear ?p1 ?c_idx) (clear ?p2 ?c_idx)
                 (not (clear ?p4 ?c_idx)) (not (clear ?p5 ?c_idx)))
  )

  (:action truck-move-down-4
    :parameters (?t - truck ?c_idx - col ?p1 ?p2 ?p3 ?p4 ?p5 ?p6 - row)
    :precondition (and (at-vertical ?t ?p1 ?c_idx) (at-vertical ?t ?p2 ?c_idx)
                       (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4) (next-row ?p4 ?p5) (next-row ?p5 ?p6)
                       (clear ?p3 ?c_idx) (clear ?p4 ?c_idx) (clear ?p5 ?c_idx) (clear ?p6 ?c_idx))
    :effect (and (not (at-vertical ?t ?p1 ?c_idx)) (not (at-vertical ?t ?p2 ?c_idx))
                 (at-vertical ?t ?p5 ?c_idx) (at-vertical ?t ?p6 ?c_idx)
                 (clear ?p1 ?c_idx) (clear ?p2 ?c_idx)
                 (not (clear ?p5 ?c_idx)) (not (clear ?p6 ?c_idx)))
  )

  (:action truck-move-up-1
    :parameters (?t - truck ?c_idx - col ?p1 ?p2 ?p3 - row)
    :precondition (and (at-vertical ?t ?p2 ?c_idx) (at-vertical ?t ?p3 ?c_idx)
                       (next-row ?p1 ?p2) (next-row ?p2 ?p3)
                       (clear ?p1 ?c_idx))
    :effect (and (not (at-vertical ?t ?p3 ?c_idx)) (at-vertical ?t ?p1 ?c_idx)
                 (clear ?p3 ?c_idx) (not (clear ?p1 ?c_idx)))
  )

  (:action truck-move-up-2
    :parameters (?t - truck ?c_idx - col ?p1 ?p2 ?p3 ?p4 - row)
    :precondition (and (at-vertical ?t ?p3 ?c_idx) (at-vertical ?t ?p4 ?c_idx)
                       (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4)
                       (clear ?p1 ?c_idx) (clear ?p2 ?c_idx))
    :effect (and (not (at-vertical ?t ?p3 ?c_idx)) (not (at-vertical ?t ?p4 ?c_idx))
                 (at-vertical ?t ?p1 ?c_idx) (at-vertical ?t ?p2 ?c_idx)
                 (clear ?p3 ?c_idx) (clear ?p4 ?c_idx)
                 (not (clear ?p1 ?c_idx)) (not (clear ?p2 ?c_idx)))
  )

  (:action truck-move-up-3
    :parameters (?t - truck ?c_idx - col ?p1 ?p2 ?p3 ?p4 ?p5 - row)
    :precondition (and (at-vertical ?t ?p4 ?c_idx) (at-vertical ?t ?p5 ?c_idx)
                       (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4) (next-row ?p4 ?p5)
                       (clear ?p1 ?c_idx) (clear ?p2 ?c_idx) (clear ?p3 ?c_idx))
    :effect (and (not (at-vertical ?t ?p4 ?c_idx)) (not (at-vertical ?t ?p5 ?c_idx))
                 (at-vertical ?t ?p1 ?c_idx) (at-vertical ?t ?p2 ?c_idx)
                 (clear ?p4 ?c_idx) (clear ?p5 ?c_idx)
                 (not (clear ?p1 ?c_idx)) (not (clear ?p2 ?c_idx)))
  )

  (:action truck-move-up-4
    :parameters (?t - truck ?c_idx - col ?p1 ?p2 ?p3 ?p4 ?p5 ?p6 - row)
    :precondition (and (at-vertical ?t ?p5 ?c_idx) (at-vertical ?t ?p6 ?c_idx)
                       (next-row ?p1 ?p2) (next-row ?p2 ?p3) (next-row ?p3 ?p4) (next-row ?p4 ?p5) (next-row ?p5 ?p6)
                       (clear ?p1 ?c_idx) (clear ?p2 ?c_idx) (clear ?p3 ?c_idx) (clear ?p4 ?c_idx))
    :effect (and (not (at-vertical ?t ?p5 ?c_idx)) (not (at-vertical ?t ?p6 ?c_idx))
                 (at-vertical ?t ?p1 ?c_idx) (at-vertical ?t ?p2 ?c_idx)
                 (clear ?p5 ?c_idx) (clear ?p6 ?c_idx)
                 (not (clear ?p1 ?c_idx)) (not (clear ?p2 ?c_idx)))
  )
)