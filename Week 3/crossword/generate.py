import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    # need to 'pip install Pillow' to use this function
    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            toRemove = []

            # if word does not meet unary constraint, store to a list to remove
            for word in self.domains[var]:
                if len(word) != var.length:
                    toRemove.append(word)
            
            # actual removal
            for word in toRemove:
                if word in self.domains[var]:
                    self.domains[var].remove(word) 

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # the mth letter in 'x' overlaps with the nth letter in 'y'
        m, n = self.crossword.overlaps[x, y]

        toRemove = []

        for Xword in self.domains[x]:
            corrValue = False

            for Yword in self.domains[y]:
                # if Xword has at least one corresponding value in 'y,' no need to check further
                if Xword[m] == Yword[n]:
                    corrValue = True
                    break
            
            # if Xword has no corresponding value in 'y'
            if not corrValue:
                toRemove.append(Xword)
        
        # remove all words in 'x' without possible corresponding value for 'y'
        if toRemove:
            for word in toRemove:
                self.domains[x].remove(word)

            return True

        # no words to remove from 'x'
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # begin with initial list of all arcs in the problem
        if not arcs:
            arcs = []
            for var in self.domains:
                # add all var and each of its neighbours as an arc
                for neighbour in self.crossword.neighbors(var):
                    arcs.append((var, neighbour))

        # revise each arc in the queue
        while arcs:
            x, y = arcs.pop()

            if self.revise(x, y):
                # impossible to solve problem if no values left in domain
                if len(self.domains[x]) == 0:
                    return False
            
                # add additional arcs to ensure other arcs stay consistent
                for neighbour in self.crossword.neighbors(x):
                    if neighbour != y:
                        arcs.append((neighbour, x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # if any word is not unique, assignment is inconsistent
        values = list(assignment.values())
        for v in values:
            c = values.count(v)
            if c > 1:
                return False

        # if any word has the incorrect length, inconsistent
        for var in assignment:
            if var.length != len(assignment[var]):
                return False

            # if there are conflicting characters with neighbours, inconsistent
            for neighbour in self.crossword.neighbors(var):
                # skip neighbours that are not assigned yet
                if neighbour not in assignment:
                    continue

                v, n = self.crossword.overlaps[var, neighbour]
                if assignment[var][v] != assignment[neighbour][n]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # a list of dictionaries with words and their total number of values ruled out for neighbours
        values = []
        
        for word in self.domains[var]:
            values.append({'word' : word, 'count' : 0})

            for neighbour in self.crossword.neighbors(var):
                # only count neighbours that are still unassigned
                if neighbour not in assignment:

                    v, n = self.crossword.overlaps[var, neighbour]
                    for Nword in self.domains[neighbour]:
                        # +1 for every neighbour's value ruled out
                        if word[v] != Nword[n]:
                            values[-1]['count'] += 1
        
        # order number ruled out in ascending order of values ruled out
        values.sort(key=lambda list: list['count'])

        # return the list of ordered words
        return [dic['word'] for dic in values]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables = []

        # get details of all unassigned variables
        for var in self.domains:
            if var not in assignment:

                # number of remaining values in a variable's domain
                values = len(self.domains[var])

                # number of neighbours
                degree = len(self.crossword.neighbors(var))

                variables.append((var, values, degree))

        # order accordingly and return first variable in order
        variables = sorted(variables, key=lambda list: (list[1], -list[2]))
        return variables[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # base case: assignment is completed
        if self.assignment_complete(assignment):
            return assignment
       
        # start with a variable var, loop through each of its values (in order)
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):

            # assign value to variable
            assignment[var] = value

            # if the value works, assign next value through recursion
            if self.consistent(assignment):
                assignment = self.backtrack(assignment)
                
                # assignment successful (not None), return result
                if assignment:
                    return assignment

            # remove value to backtrack if value doesn't work
            assignment.pop(var)
        
        # no assignable value
        return None
        

def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
