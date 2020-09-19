import queue
import cnf
from util import log

def resolve_symbol(clause1, clause2, symbol):
    if symbol in clause1 and symbol in clause2:
        if clause1[symbol] and not clause2[symbol]:
            return clause1.remove(symbol) | clause2.remove(symbol)
        if not clause1[symbol] and clause2[symbol]:
            return clause1.remove(symbol) | clause2.remove(symbol)
    return None

def resolve(clause1, clause2):
    resolvents = []
    for sym in clause1.symbols() & clause2.symbols():
       resolvent = resolve_symbol(clause1, clause2, sym)  
       if resolvent is not None:
           resolvents.append(resolvent)
    return resolvents
    

class ClauseQueue:
    def __init__(self):
        self.queue = queue.PriorityQueue()
        self.priority_function = lambda clause: len(clause)
        self.cached_clauses = set([])
        
    def push(self, clause):
        if not clause in self.cached_clauses:
            self.queue.put((self.priority_function(clause), clause))
            self.cached_clauses.add(clause)
            return True
        else:
            return False
    
    def pop(self):
        if not self.empty():
            return self.queue.get()[1]
        else:
            return None
    
    def empty(self):
        return self.queue.empty()
    
    def num_generated(self):
        return len(self.cached_clauses)

def resolution_closure(initial_unprocessed, early_stopping=False):
    processed = set([])    
    unprocessed = ClauseQueue()
    for c in initial_unprocessed:
        if early_stopping and not bool(c):
            return set([c])   
        unprocessed.push(c)
    while not unprocessed.empty():
        next_to_process = unprocessed.pop()
        for clause in processed:
            for resolvent in resolve(next_to_process, clause):
                is_new_clause = unprocessed.push(resolvent)
                if is_new_clause:
                    log("{} [BY RESOLVING {} WITH {}]"
                        .format(resolvent, next_to_process, clause))                    
                if early_stopping and not bool(resolvent):
                    log("Proved unsat after generating {} clauses."
                        .format(unprocessed.num_generated()))
                    return set([resolvent])   
        processed.add(next_to_process)
    log("Proved sat after generating {} clauses.".format(unprocessed.num_generated()))
    return processed

def full_resolution(sent):
    return cnf.c('FALSE') not in resolution_closure(sent.clauses, 
                                                    early_stopping = True)

