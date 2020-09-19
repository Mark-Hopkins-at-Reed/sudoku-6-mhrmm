HW: Sudoku 6
------------

Let's finish our resolution solver! 


1. In ```resolution.py``` create a function called ```resolution_closure```
   that computes the resolution closure of a set of Clauses. For instance:
   
       resolution_closure({cnf.c('!b || !c'), 
                           cnf.c('b || d')})
       
   should return a set of Clauses that is equivalent to the following:
   
       { cnf.c('!b || !c'), cnf.c('b || d'), cnf.c('!c || d') }
       
   Hint: Consider using the ClauseQueue from the previous stage of the project.
   
   Once you have a successful implementation, the following unit tests should
   succeed:
   
       python -m unittest test_part6.TestResolutionClosure

2. Augment ```resolution_closure``` to take a default Boolean parameter
   ```early_stopping``` whose default value is ```False```. When
   ```early_stopping == False```, ```resolution_closure``` should behave
   the same as described in Q1.  When ```early_stopping == True```, the
   function ```resolution_closure``` should stop as soon as it adds the
   clause ```cnf.c('FALSE')``` to the closure, and simply return the
   singleton set ```{ cnf.c('FALSE') }```.

   Once you have a successful implementation, the following unit tests should
   succeed:
   
       python -m unittest test_part6.TestEarlyStopping
       
   Also, it should be considerably faster to run early stopping in unit
   test ```test_es_6```. It should report something like:
   
       With early stopping: 0.0095s
       W/o  early stopping: 1.5312s
       
3. In ```resolution.py``` create a function called ```full_resolution```
   that computes whether a given CNF sentence is satisfiable. For
   instance:
   
       full_resolution(['a || b', 
                        '!a',
                        '!b || !c',
                        'c'])
    
   should return ```False```, whereas:
   
       full_resolution(['a || b', 
                        '!a',
                        '!b || !c'])
   
   should return ```True```. 
   
   Once you have a successful implementation, the following unit tests should
   succeed:
   
       python -m unittest test_part6.TestFullResolution
