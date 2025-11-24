;--------------------------------------------------------------------------------------------------------


;MERGED FEATURES IN PDDL (DOMAIN FILE) VER. 1: OPTIMIZING FEAT1VER1 AND FEAT2VER1'S 6X6 GRID & MULTISTEP ACTIONS
;References: https://fareskalaboud.github.io/LearnPDDL/, https://editor.planning.domains/#
;Debugging the features and changing representation/configuration using PDDL and LLM suggestions
;No runner for any configuration yet

;From here, I need to minimize the search space, and create a better domain .pddl file
;Optimizations I'm going to try:
; - converting cells to row/col representation (also don't even need adjacent-left or adjacent-up)
; - removing occupies() and using at() for everything, also merging at() with the direction of the car for less facts
; - dynamically calculating the multi-step slides (or postprocessing slides if necessary) --> based on the emails
;   it sounds like the intention is for multi-step actions in the search tree rather than merging multiple steps
;   in the final action plan together to form multi-step actions. This does blow up the search tree, though, and 
;   I think the goal of the project is just to get an efficient working game? I think I'll try to implement both 
;   the multi-step actions in the search tree and in post-processing, as I can see both arguments for what I should do.


;--------------------------------------------------------------------------------------------------------

(define (domain rush-hour)
  (:requirements :typing) 
  
  (:types
    vehicle cell - object
    car truck - vehicle
  )
  
  (:predicates
    (at ?v - car ?c - cell)           
    (occupies ?t - truck ?c - cell)   
    (clear ?c - cell)                 
    (horizontal ?v - vehicle)         
    (vertical ?v - vehicle)           
    (adjacent-right ?from ?to - cell) 
    (adjacent-left ?from ?to - cell)  
    (adjacent-up ?from ?to - cell)    
    (adjacent-down ?from ?to - cell)  
  )
  
  ;Horizontal actions
  (:action car-move-right
    :parameters (?c - car ?from ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (horizontal ?c)
      (adjacent-right ?from ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-right-two
    :parameters (?c - car ?from ?between ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (horizontal ?c)
      (adjacent-right ?from ?between)
      (adjacent-right ?between ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-right-three
    :parameters (?c - car ?from ?between ?between2 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (horizontal ?c)
      (adjacent-right ?from ?between)
      (adjacent-right ?between ?between2)
      (adjacent-right ?between2 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-right-four
    :parameters (?c - car ?from ?between ?between2 ?between3 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (clear ?between3)
      (horizontal ?c)
      (adjacent-right ?from ?between)
      (adjacent-right ?between ?between2)
      (adjacent-right ?between2 ?between3)
      (adjacent-right ?between3 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-right-five
    :parameters (?c - car ?from ?between ?between2 ?between3 ?between4 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (clear ?between3)
      (clear ?between4)
      (horizontal ?c)
      (adjacent-right ?from ?between)
      (adjacent-right ?between ?between2)
      (adjacent-right ?between2 ?between3)
      (adjacent-right ?between3 ?between4)
      (adjacent-right ?between4 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-left
    :parameters (?c - car ?from ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (horizontal ?c)
      (adjacent-left ?from ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-left-two
    :parameters (?c - car ?from ?between ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (horizontal ?c)
      (adjacent-left ?from ?between)
      (adjacent-left ?between ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-left-three
    :parameters (?c - car ?from ?between ?between2 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (horizontal ?c)
      (adjacent-left ?from ?between)
      (adjacent-left ?between ?between2)
      (adjacent-left ?between2 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-left-four
    :parameters (?c - car ?from ?between ?between2 ?between3 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (clear ?between3)
      (horizontal ?c)
      (adjacent-left ?from ?between)
      (adjacent-left ?between ?between2)
      (adjacent-left ?between2 ?between3)
      (adjacent-left ?between3 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-left-five
    :parameters (?c - car ?from ?between ?between2 ?between3 ?between4 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (clear ?between3)
      (clear ?between4)
      (horizontal ?c)
      (adjacent-left ?from ?between)
      (adjacent-left ?between ?between2)
      (adjacent-left ?between2 ?between3)
      (adjacent-left ?between3 ?between4)
      (adjacent-left ?between4 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )

  (:action truck-move-right
    :parameters (?t - truck ?t-head ?t-tail ?to - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?to)
      (horizontal ?t)
      (adjacent-right ?t-tail ?t-head)
      (adjacent-right ?t-head ?to)
    )
    :effect (and
      (not (clear ?to))
      (occupies ?t ?to)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
    )
  )
  
  (:action truck-move-right-two
    :parameters (?t - truck ?t-head ?t-tail ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?to-head)
      (clear ?to-tail)
      (horizontal ?t)
      (adjacent-right ?t-tail ?t-head)
      (adjacent-right ?t-head ?to-tail)
      (adjacent-right ?to-tail ?to-head)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-right-three
    :parameters (?t - truck ?t-head ?t-tail ?between ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?between)
      (clear ?to-head)
      (clear ?to-tail)
      (horizontal ?t)
      (adjacent-right ?t-tail ?t-head)
      (adjacent-right ?t-head ?between)
      (adjacent-right ?between ?to-tail)
      (adjacent-right ?to-tail ?to-head)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-right-four
    :parameters (?t - truck ?t-head ?t-tail ?between ?between2 ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?between)
      (clear ?between2)
      (clear ?to-head)
      (clear ?to-tail)
      (horizontal ?t)
      (adjacent-right ?t-tail ?t-head)
      (adjacent-right ?t-head ?between)
      (adjacent-right ?between ?between2)
      (adjacent-right ?between2 ?to-tail)
      (adjacent-right ?to-tail ?to-head)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-left
    :parameters (?t - truck ?t-head ?t-tail ?to - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?to)
      (horizontal ?t)
      (adjacent-left ?t-head ?t-tail)
      (adjacent-left ?t-tail ?to)
    )
    :effect (and
      (not (clear ?to))
      (occupies ?t ?to)
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-left-two
    :parameters (?t - truck ?t-head ?t-tail ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?to-head)
      (clear ?to-tail)
      (horizontal ?t)
      (adjacent-left ?t-head ?t-tail)
      (adjacent-left ?t-tail ?to-head)
      (adjacent-left ?to-head ?to-tail)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-left-three
    :parameters (?t - truck ?t-head ?t-tail ?between ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?between)
      (clear ?to-head)
      (clear ?to-tail)
      (horizontal ?t)
      (adjacent-left ?t-head ?t-tail)
      (adjacent-left ?t-tail ?between)
      (adjacent-left ?between ?to-head)
      (adjacent-left ?to-head ?to-tail)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-left-four
    :parameters (?t - truck ?t-head ?t-tail ?between ?between2 ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?between)
      (clear ?between2)
      (clear ?to-head)
      (clear ?to-tail)
      (horizontal ?t)
      (adjacent-left ?t-head ?t-tail)
      (adjacent-left ?t-tail ?between)
      (adjacent-left ?between ?between2)
      (adjacent-left ?between2 ?to-head)
      (adjacent-left ?to-head ?to-tail)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )

  ;Vertical actions
  (:action car-move-up
    :parameters (?c - car ?from ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (vertical ?c)
      (adjacent-up ?from ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-up-two
    :parameters (?c - car ?from ?between ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (vertical ?c)
      (adjacent-up ?from ?between)
      (adjacent-up ?between ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-up-three
    :parameters (?c - car ?from ?between ?between2 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (vertical ?c)
      (adjacent-up ?from ?between)
      (adjacent-up ?between ?between2)
      (adjacent-up ?between2 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-up-four
    :parameters (?c - car ?from ?between ?between2 ?between3 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (clear ?between3)
      (vertical ?c)
      (adjacent-up ?from ?between)
      (adjacent-up ?between ?between2)
      (adjacent-up ?between2 ?between3)
      (adjacent-up ?between3 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-up-five
    :parameters (?c - car ?from ?between ?between2 ?between3 ?between4 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (clear ?between3)
      (clear ?between4)
      (vertical ?c)
      (adjacent-up ?from ?between)
      (adjacent-up ?between ?between2)
      (adjacent-up ?between2 ?between3)
      (adjacent-up ?between3 ?between4)
      (adjacent-up ?between4 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-down
    :parameters (?c - car ?from ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (vertical ?c)
      (adjacent-down ?from ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-down-two
    :parameters (?c - car ?from ?between ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (vertical ?c)
      (adjacent-down ?from ?between)
      (adjacent-down ?between ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-down-three
    :parameters (?c - car ?from ?between ?between2 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (vertical ?c)
      (adjacent-down ?from ?between)
      (adjacent-down ?between ?between2)
      (adjacent-down ?between2 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-down-four
    :parameters (?c - car ?from ?between ?between2 ?between3 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (clear ?between3)
      (vertical ?c)
      (adjacent-down ?from ?between)
      (adjacent-down ?between ?between2)
      (adjacent-down ?between2 ?between3)
      (adjacent-down ?between3 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action car-move-down-five
    :parameters (?c - car ?from ?between ?between2 ?between3 ?between4 ?to - cell)
    :precondition (and
      (at ?c ?from)
      (clear ?to)
      (clear ?between)
      (clear ?between2)
      (clear ?between3)
      (clear ?between4)
      (vertical ?c)
      (adjacent-down ?from ?between)
      (adjacent-down ?between ?between2)
      (adjacent-down ?between2 ?between3)
      (adjacent-down ?between3 ?between4)
      (adjacent-down ?between4 ?to)
    )
    :effect (and
      (at ?c ?to)
      (clear ?from)
      (not (at ?c ?from))
      (not (clear ?to))
    )
  )
  
  (:action truck-move-up
    :parameters (?t - truck ?t-head ?t-tail ?to - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?to)
      (vertical ?t)
      (adjacent-up ?t-head ?t-tail)
      (adjacent-up ?t-tail ?to)
    )
    :effect (and
      (occupies ?t ?t-tail)
      (not (clear ?to))
      (occupies ?t ?to)
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-up-two
    :parameters (?t - truck ?t-head ?t-tail ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?to-head)
      (clear ?to-tail)
      (vertical ?t)
      (adjacent-up ?t-head ?t-tail)
      (adjacent-up ?t-tail ?to-head)
      (adjacent-up ?to-head ?to-tail)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-up-three
    :parameters (?t - truck ?t-head ?t-tail ?between ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?between)
      (clear ?to-head)
      (clear ?to-tail)
      (vertical ?t)
      (adjacent-up ?t-head ?t-tail)
      (adjacent-up ?t-tail ?between)
      (adjacent-up ?between ?to-head)
      (adjacent-up ?to-head ?to-tail)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-up-four
    :parameters (?t - truck ?t-head ?t-tail ?between ?between2 ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?between)
      (clear ?between2)
      (clear ?to-head)
      (clear ?to-tail)
      (vertical ?t)
      (adjacent-up ?t-head ?t-tail)
      (adjacent-up ?t-tail ?between)
      (adjacent-up ?between ?between2)
      (adjacent-up ?between2 ?to-head)
      (adjacent-up ?to-head ?to-tail)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-down
    :parameters (?t - truck ?t-head ?t-tail ?to - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?to)
      (vertical ?t)
      (adjacent-down ?t-tail ?t-head)
      (adjacent-down ?t-head ?to)
    )
    :effect (and
      (occupies ?t ?t-head)
      (not (clear ?to))
      (occupies ?t ?to)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
    )
  )
  
  (:action truck-move-down-two
    :parameters (?t - truck ?t-head ?t-tail ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?to-head)
      (clear ?to-tail)
      (vertical ?t)
      (adjacent-down ?t-tail ?t-head)
      (adjacent-down ?t-head ?to-tail)
      (adjacent-down ?to-tail ?to-head)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-down-three
    :parameters (?t - truck ?t-head ?t-tail ?between ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?between)
      (clear ?to-head)
      (clear ?to-tail)
      (vertical ?t)
      (adjacent-down ?t-tail ?t-head)
      (adjacent-down ?t-head ?between)
      (adjacent-down ?between ?to-tail)
      (adjacent-down ?to-tail ?to-head)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
  
  (:action truck-move-down-four
    :parameters (?t - truck ?t-head ?t-tail ?between ?between2 ?to-head ?to-tail - cell)
    :precondition (and
      (occupies ?t ?t-head)
      (occupies ?t ?t-tail)
      (clear ?between)
      (clear ?between2)
      (clear ?to-head)
      (clear ?to-tail)
      (vertical ?t)
      (adjacent-down ?t-tail ?t-head)
      (adjacent-down ?t-head ?between)
      (adjacent-down ?between ?between2)
      (adjacent-down ?between2 ?to-tail)
      (adjacent-down ?to-tail ?to-head)
    )
    :effect (and
      (not (clear ?to-tail))
      (occupies ?t ?to-tail)
      (not (clear ?to-head))
      (occupies ?t ?to-head)
      (clear ?t-tail)
      (not (occupies ?t ?t-tail))
      (clear ?t-head)
      (not (occupies ?t ?t-head))
    )
  )
)