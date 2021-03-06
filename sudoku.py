import math
import cnf
from cnf import Cnf

def irange(i, j):
    return range(i, j+1)

def lit(d, i, j, polarity = True):
    """
    Creates a literal indicating whether cell (i, j) contains digit d.
    
    """
    literal = 'd{}_{}_{}'.format(d, i, j)
    if not polarity:
        literal = '!{}'.format(literal)
    return literal

class SudokuBoard:
    
    def __init__(self, matrix):
        self.matrix = matrix
        self.box_width = int(math.sqrt(len(self.matrix)))
        err = "Improper dimensions for a Sudoku board!"
        assert self.box_width == math.sqrt(len(self.matrix)), err
        
    def __str__(self):
        row_strs = [''.join([str(digit) for digit in row]) for row in self.matrix]        
        return '\n'.join(row_strs)
 
    def rows(self):
        def row_cells(i, row_length):
            return set([(i, j) for j in irange(1, row_length)])
        num_symbols = self.box_width * self.box_width
        return [row_cells(row, num_symbols) for row in irange(1, num_symbols)]
    
    def columns(self):
        def col_cells(j, col_length):
            return set([(i, j) for i in irange(1, col_length)])
        num_symbols = self.box_width * self.box_width
        return [col_cells(col, num_symbols) for col in irange(1, num_symbols)]
 
    def boxes(self):
        def box_cells(a, b, box_width):
            return set([(i+1,j+1) for i in range((a-1) * box_width, a * box_width)
                                  for j in range((b-1) * box_width, b * box_width)])
        return [box_cells(a, b, self.box_width) for a in irange(1, self.box_width)
                                                 for b in irange(1, self.box_width)]
    def zones(self):
        return self.rows() + self.columns() + self.boxes()
    
    
    def cnf(self):
        num_symbols = self.box_width * self.box_width
        clause_strs = []
        for zone in self.zones():
            for digit in irange(1, num_symbols):
                clause_strs += exactly_one_clauses(zone, digit)
        clause_strs += nonempty_clauses(self.box_width)
        clauses = [cnf.c(clause) for clause in clause_strs]
        return Cnf(list(set(clauses)))
    


def at_least_clause(cells, d):
    """
    Encodes: "The following cells have at least 1 of digit d."

    """  
    literals = [lit(d, i, j) for (i, j) in sorted(cells)]
    return ' || '.join(literals)  

def at_most_clauses(cells, d):
    """
    Encodes: "The following cells have at most 1 of digit d."

    """ 
    def all_pairs(seq):
        for a in range(len(seq)):
            for b in range(a+1, len(seq)):
                yield seq[a], seq[b]
    clauses = []         
    for cell1, cell2 in all_pairs(sorted(cells)):
        clauses.append('{} || {}'.format(lit(d, cell1[0], cell1[1], polarity=False), 
                                         lit(d, cell2[0], cell2[1], polarity=False)))        
    return clauses

def exactly_one_clauses(cells, d):
    """
    Encodes: "The following cells have exactly 1 of digit d."

    """
    return [at_least_clause(cells, d)] + at_most_clauses(cells, d)     


def nonempty_clauses(box_width):
    def non_zero_cell(i, j):
        """
        Encodes: "Cell i, j is non-zero."
    
        """ 
        literals = [lit(d, i, j) for d in irange(1, box_size)]
        return ' || '.join(literals)         
    box_size = box_width * box_width    
    clauses = [non_zero_cell(row, col)
               for row in irange(1, box_size)
               for col in irange(1, box_size)]
    return clauses
                

