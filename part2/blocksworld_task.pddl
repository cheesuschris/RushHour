(define (problem bw-p01)
  (:domain blocksworld)

  (:objects A B C - block)

  (:init
    (ontable A)
    (ontable B)
    (ontable C)
    (clear A)
    (clear B)
    (clear C)
    (handempty)
  )

  (:goal
    (and
      (on A B)
      (on B C))
  )
)