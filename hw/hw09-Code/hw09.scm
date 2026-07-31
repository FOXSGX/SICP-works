;;; Homework 09: Macro

; ANSWER QUESTION wwsd

;;; Required Problems

(define (find n lst)
  (define (helper x lst)
          (if (= (car lst) n)
              x
              (helper (+ x 1) (cdr lst))))
  (helper 0 lst)
)


(define (find-nest n sym)
  (define (helper ans lst)
          (cond ((null? lst) #f)
                ((list? (car lst)) (if (helper `(car ,ans) (car lst))
                                 (helper `(car ,ans) (car lst))
                                 (helper `(cdr ,ans) (cdr lst))))
                ((= n (car lst)) `(car ,ans))
                (else (helper `(cdr ,ans) (cdr lst)))))
  (helper sym (eval sym))
)


(define-macro (my/or operands)
  (cond 
    ((null? operands) #f)
    ((null? (cdr operands)) (car operands))
    (else
      `(let ((t ,(car operands)))
         (if t
             t
             (my/or ,(cdr operands)))))
))

(define (helper1 args indices counter)
    (if (null? args)
        nil
    (if (null? indices)
        (cons (car args) (helper1 (cdr args) indices (+ counter 1)))
    (if (= counter (car indices))
        (helper1 (cdr args) (cdr indices) (+ counter 1))
    (cons (car args) (helper1 (cdr args) indices (+ counter 1)))))))

(define (helper2 args indices counter val)
    (if (null? args)
        nil
    (if (null? indices)
        (cons (car args) (helper2 (cdr args) indices (+ counter 1) val))
    (if (= counter (car indices))
        (cons (car val) (helper2 (cdr args) (cdr indices) (+ counter 1) (cdr val)))
    (cons (car args) (helper2 (cdr args) indices (+ counter 1) val))))))
(define-macro (k-curry fn args vals indices)
  `(lambda ,(helper1 args indices 0) ,(cons fn (helper2 args indices 0 vals)))
)


(define-macro (let* bindings expr)
  (if (null? bindings)
      `(let () ,expr)
      `(let (,(car bindings)) (let* ,(cdr bindings) ,expr)))
)

;;; Just For Fun Problems


; Helper Functions for you
(define (cadr lst) (car (cdr lst)))
(define (cddr lst) (cdr (cdr lst)))
(define (caddr lst) (car (cdr (cdr lst))))
(define (cdddr lst) (cdr (cdr (cdr lst))))

(define-macro (infix expr)
  'YOUR-CODE-HERE
)


; only testing if your code could expand to a valid expression 
; resulting in my/and/2 and my/or/2 not hygienic
(define (gen-sym) 'sdaf-123jasf/a123)

; in these two functions you can use gen-sym function.
; assumption:
; 1. scm> (eq? (gen-sym) (gen-sym))
;    #f
; 2. all symbol generate by (gen-sym) will not in the source code before macro expansion
(define-macro (my/and/2 operands)
  'YOUR-CODE-HERE
)

(define-macro (my/or/2 operands)
  'YOUR-CODE-HERE
)
