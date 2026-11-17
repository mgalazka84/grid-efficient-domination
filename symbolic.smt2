; SMT-LIB 2. Counterexample searches for the strip equation and window cuts.
; Run: z3 symbolic.smt2
; Expected: unsat, unsat. All dimensions and coordinates below are unbounded integers.
(set-logic QF_LIA)
(declare-const p Int)
(assert (>= p 1))
(define-fun m () Int (* 2 p))
(define-fun L () Int (+ m 1))
(declare-const i Int)
(assert (and (<= 1 i) (<= i m)))
(define-fun even ((x Int)) Bool (= (mod x 2) 0))
(define-fun d ((row Int)) Int (ite (even row) row (- L row)))
(define-fun seed ((A Bool) (x Int)) Bool
  (let ((phase (mod x 4)))
    (ite A (or (= phase 1) (= phase 2)) (or (= phase 0) (= phase 1)))))
(define-fun block ((A Bool) (row Int) (t Int)) Bool
  (and (<= 1 row) (<= row m)
    (ite (even t)
      (and (> (d row) (- L t))
           (seed A (ite (even row) (- (+ row t) 1) (- t row 1))))
      (and (> (d row) t) (seed A (- (+ row t) 1))))))
; All uses of t lie between -1 and L. A crossing reflects the row.
(define-fun cell ((A Bool) (row Int) (t Int)) Bool
  (ite (< t 0) (block A (- L row) (+ t L))
    (ite (>= t L) (block A (- L row) (- t L)) (block A row t))))
(define-fun bit ((x Bool)) Int (ite x 1 0))

; Does a cell have an open-neighbour sum different from one?
(push)
(declare-const A Bool)
(declare-const t Int)
(assert (and (<= 0 t) (< t L)))
(assert (distinct 1
  (+ (bit (cell A (- i 1) t)) (bit (cell A (+ i 1) t))
     (bit (cell A i (- t 1))) (bit (cell A i (+ t 1))))))
(check-sat)
(pop)

; Is there a row witnessing the failure of either inclusion for any residue?
(declare-const r Int)
(assert (and (<= 0 r) (< r L)))
(define-fun max2 ((x Int) (y Int)) Int (ite (>= x y) x y))
(define-fun h () Int (ite (even p) p (+ p 1)))
(define-fun u () Int (ite (even p) (+ p 1) p))
(define-fun useA () Bool (even r))
(define-fun leftCut () Int
  (ite useA (max2 0 (- h r))
       (ite (= r 1) 0 (max2 (+ 1 (- L r)) u))))
(define-fun rightCut () Int
  (let ((end (+ leftCut r))) (ite (>= end L) (- end L) end)))
(assert (or
  (and (cell useA i leftCut) (not (cell useA i (+ leftCut 1))))
  (and (cell useA i (+ rightCut 1)) (not (cell useA i rightCut)))))
(check-sat)
