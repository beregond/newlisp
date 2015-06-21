Newlisp
=======

Struktura projektu
------------------

Projekt zawiera trzy pliki:

* `newlisp.py` który tworzy parser i uruchamia go na źródle podanego pliku
* `parser.py` który zawiera wszystkie definicje potrzebne `ply` do stworzenia
  parsera
* `expressions.py` który zawiera klasy używane wewnętrznie przez parser i które
  zajmują się całą logiką podczas wykonywania programu
* `exc.py` zawiera klasy związane z obsługą wyjątków

Obliczenia
----------

Wartości są obliczane za pomocą wyrażeń: `(operacja arg1 arg2)` - jest to, jak
widać, odwrotna notacja polska.

.. code-block::

    (defun wielomian (x)
        (+ (+ (* 2, (* x, x)), (* 5, x)), 10))

Dostępne wyrażenia
------------------

#. let
~~~~~~

Pozwala przypisywać wartości do zmiennych. Jeśli chcemy przypisać listę,
musimy poprzedzić wartość apostrofem.

.. code-block::

    (let m 5)
    (let x '(5, 2, 3))

#. defun
~~~~~~~~

Definiuje nową funkcję z argumentami. Zwrócona wartość to wynik ostatniego
wyrażenia w ciele funkcji. Wywołujemy ją poprzez nazwę.

.. code-block::

    (defun circle_area (radius)
        (* 2, (* 3.14, radius)))

    (print (circle_area (3)))

#. print
~~~~~~~~

Pozwala wyświetlać dowolną strukturę i wynik wyrażenia.

.. code-block::

    (print (first x))

#. val
~~~~~~

Jest wyrażeniem, które zwraca podaną wartość, szczególnie przydatne, jeśli jest
ostatnim wyrażeniem danego bloku.

.. code-block::

    (defun fib (x)
        (if (zero x)
            (val 1)
            (if (x == 1)
                (val 1)
                (+ (fib ((- x, 1))), (fib ((- x, 2)))))))

#. if
~~~~~

Wyrażenie warunkowe. W blokach instrukcji dla powodzenia i niepowodzenia testu
logicznego możemy użyć jednego lub więcej wyrażeń.

.. code-block::

    (defun count_for_any (x)
        (if (empty x)
            (val '())
            (+
                '((wielomian ((first x)))),
                (count_for_any ((rest x)))
            )))

Obsługa wyjątków
----------------

Można obsługiwać wbudowane wyjątki (w tym momencie jedynie `computation_error`)
lub definiować własne poprzez `defexc`. Łapanie wyjątków jest realizowane
poprzez konstrukcję `try except`. W wyjątkach można przekazywać jakąś wartość,
np wiadomość o szczegółach błędu.

.. code-block::

    (try (
        (print (+ a, b))
    ) except computation_error (
        (print 'nie mozna dodac tych argumentow')
    ))

    (raise computation_error 'rzucanie wbudowanych wyjatkow')

Funkcje wbudowane
-----------------

* `zero` test logiczny, czy podana wartość jest równa zero
* `first` zwraca pierwszy element tablicy
* `rest` zwraca tablicę wszystkich elementów poza pierwszym
* `empty` sprawdza, czy tablica jest pusta
