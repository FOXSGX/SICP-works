;;; Homework 08: Scheme

;;; Required Problems

(define (square x) (* x x))

;; Problem 1: Quick Pow

(define (quick-pow base exp)
        (if (= exp 0)
            1
            (if (= exp 1)
            base
            (if (= 0 (- exp (* 2 (quotient exp 2))))
                (square (quick-pow base (quotient exp 2)))
                (* base (square (quick-pow base (quotient exp 2))))
                )))
        
)

;; Problem 2: Quicker Pow

(define (quicker-pow base exp)
  (define (helper base exp mul)
           (if (= exp 0)
            mul
            (if (= exp 1)
            (* base mul)
            (if (= 0 (- exp (* 2 (quotient exp 2))))
                (helper (square base) (/ exp 2) mul)
                (helper (square base) (quotient exp 2) (* mul base))
                ))))
  (helper base exp 1)
)

;; Problem 3: Find

(define (find predicate lst)
        (if (null? lst)
            #f
            (if (predicate (car lst))
                (car lst)
                (find predicate (cdr lst))))
)

;; Problem 4: Count Change III

(define (make-change total biggest)
    (define (list_of_one n)
            (if (= n 1)
                '(1)
            (append '(1) (list_of_one (- n 1)))))


        (if (or (= 0 total) (= 0 biggest))
            '(())
        (if (= total 1)
            '((1))
        (if (< total biggest)
            (make-change total total)
        (if (= biggest 1)
            (list (list_of_one total))
          (append (map (lambda (x) (append (list biggest) x))
                    (make-change (- total biggest) biggest)) (make-change total (- biggest 1)))
            ))))
)

;; Problem 5: Enumerate

(define (enumerate lst)
    (define (helper lst counter)
            (if (null? lst)
                '()
                (append (list (cons counter (car lst))) (helper (cdr lst) (+ 1 counter)))))

    (helper lst 0)
)

;; Problem 6: Substitute

(define (substitute bindings s)
  (define (finder lst)
        (if (null? lst)
            #f
            (if (equal? (car s) (car (car lst)))
                (cdr (car lst))
                (finder (cdr lst)))))


  (if (null? bindings)
      s
  (if (null? s)
      '()
  (if (list? (car s))
      (append (list (substitute bindings (car s))) (substitute bindings (cdr s)))
  (begin 
      (define oo (finder bindings))
      (if oo
          (append (list oo) (substitute bindings (cdr s)))
          (append (list (car s)) (substitute bindings (cdr s)))))
      )))
)

;; Problem 7: Tree in Scheme

(define (tree label branches)
  (define (make_branches b)
          (if (null? b)
              nil
              (append (list (car b)) (make_branches (cdr b))) 
              ))
        (list label (make_branches branches))
)

(define (label t)
  (car t)
)

(define (branches t)
  (car (cdr t))
)

(define (is-leaf t)
  (if (null? (branches t))
      #t
      #f)
)

; A tree for test

(define t1 (tree 1
  (list
    (tree 2
      (list
        (tree 5 nil)
        (tree 6 (list
          (tree 8 nil)))))
    (tree 3 nil)
    (tree 4
      (list
        (tree 7 nil))))))

;; Problem 8: Label Sum

(define (label-sum t)
  (define (add_b b ans)
          (if (null? b)
              ans
              (add_b (cdr b) (+ ans (label-sum (car b))))))
  
  (if (is-leaf t)
      (label t)
      (+ (label t) (add_b (branches t) 0)))
)

;;; Just For Fun Problems

;; Problem 9: Derive

(define (cadr s) (car (cdr s)))
(define (caddr s) (car (cdr (cdr s))))

; derive returns the derivative of EXPR with respect to VAR
(define (derive expr var)
  (cond ((number? expr) 0)
        ((variable? expr) (if (same-variable? expr var) 1 0))
        ((sum? expr) (derive-sum expr var))
        ((product? expr) (derive-product expr var))
        ((exp? expr) (derive-exp expr var))
        (else 'Error)))

; Variables are represented as symbols
(define (variable? x) (symbol? x))
(define (same-variable? v1 v2)
  (and (variable? v1) (variable? v2) (eq? v1 v2)))

; Numbers are compared with =
(define (=number? expr num)
  (and (number? expr) (= expr num)))

; Sums are represented as lists that start with +.
(define (make-sum a1 a2)
  (cond ((=number? a1 0) a2)
        ((=number? a2 0) a1)
        ((and (number? a1) (number? a2)) (+ a1 a2))
        (else (list '+ a1 a2))))
(define (sum? x)
  (and (list? x) (eq? (car x) '+)))
(define (first-operand s) (cadr s))
(define (second-operand s) (caddr s))

; Products are represented as lists that start with *.
(define (make-product m1 m2)
  (cond ((or (=number? m1 0) (=number? m2 0)) 0)
        ((=number? m1 1) m2)
        ((=number? m2 1) m1)
        ((and (number? m1) (number? m2)) (* m1 m2))
        (else (list '* m1 m2))))
(define (product? x)
  (and (list? x) (eq? (car x) '*)))
; You can access the operands from the expressions with
; first-operand and second-operand (already defined for sum).
; (define (first-operand p) (cadr p))
; (define (second-operand p) (caddr p))

;; Problem 9.1: Derive Sum

(define (derive-sum expr var)
  'YOUR-CODE-HERE
)

;; Problem 9.2: Derive Product

(define (derive-product expr var)
  'YOUR-CODE-HERE
)

;; Problem 9.3: Make Exp

; Exponentiations are represented as lists that start with ^.
(define (make-exp base exponent)
  'YOUR-CODE-HERE
)

(define (exp? exp)
  'YOUR-CODE-HERE
)

; Some expressions for test
(define x^2 (make-exp 'x 2))
(define x^3 (make-exp 'x 3))

;; Problem 9.4: Derive Exp

(define (derive-exp exp var)
  'YOUR-CODE-HERE
)
