(defun fib (x)
    (if (zero x)
        (val 1)
        (if (x == 1)
            (val 1)
            (+ (fib ((- x, 1))), (fib ((- x, 2)))))))

(print (fib (11)))

(defun circle_area (radius)
    (* 2, (* 3.14, radius)))

(print (circle_area (3)))

(let x '(5, 2, 3))

(print (first x))
(print (rest x))
(print (first (rest x)))

(defun wielomian (x)
    (+ (+ (* 2, (* x, x)), (* 5, x)), 10))

(print (wielomian (4)))

(let m 5)
(let f '(2, 3, 4, m))
(print f)

(defun length (x)
    (if (empty x)
        (val 0)
        (+ 1, (length ((rest x))))))

(print (length (f)))

(defun count_for_any (x)
    (if (empty x)
        (val '())
        (+
            '((wielomian ((first x)))),
            (count_for_any ((rest x)))
        )))

(let input '(1, 2, 3, 4, 5))
(print (count_for_any (input)))

(defexc some_error)

(try (
    (raise some_error 'asdfasdf')
) except some_error (
    (print 'works')
))

(let a '(1, 2, 3))
(let b 'asdf')

(try (
    (print (+ a, b))
) except computation_error (
    (print 'nie mozna dodac tych argumentow')
))

(try (
    (raise computation_error 'rzucanie wbudowanych wyjatkow')
) except computation_error (
    (print 'works')
))
