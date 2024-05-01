import sys
import os




class Literal:
    def __init__(self, name, TP: list = [], FP: list = []):
        self.name = name
        # TP: a list of boolean values, None if not applicable
        self.TP = TP
        # FP: a list of list of transactions, None if not applicable
        self.FP = FP

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()
    
    def evaluate(self):
        '''return the evaluation of the formula'''
        '''TP = True/False'''
        '''FP = list of False Positive'''
        return self.TP, self.FP


class Formula:
    def __init__(self, left, operator=None, right=None):
        self.left = left
        if operator == "and" or operator == "&&":
            self.operator = "∧"
        elif operator == "or" or operator == "||":
            self.operator = "v"
        else:
            self.operator = operator
        self.right = right

    def __str__(self):
        if self.operator is None:
            return str(self.left)
        return f"({str(self.left)} {self.operator} {str(self.right)})"

    def __repr__(self):
        return self.__str__()
    
    def evaluate(self):
        '''return the evaluation of the formula'''
        '''TP = True/False'''
        '''FP = list of False Positive'''
        leftTP, leftFP = self.left.evaluate()
        rightTP, rightFP = self.right.evaluate()
        if isinstance(leftTP, list) and isinstance(rightTP, list) and \
            len(leftTP) != len(rightTP):
            sys.exit("Error: the number of TP is not equal")
        if isinstance(leftFP, list) and isinstance(rightFP, list) and \
            len(leftFP) != len(rightFP):
            sys.exit("Error: the number of FP is not equal")
        new_TP = []
        new_FP = []
        
        for ii in range(len(leftTP)):
            if leftTP[ii] is None and rightTP[ii] is None:
                new_TP.append(None)
                new_FP.append(None)
            elif leftTP[ii] is None and rightTP[ii] is not None:
                new_TP.append(rightTP[ii])
                new_FP.append(rightFP[ii])
            elif leftTP[ii] is not None and rightTP[ii] is None:
                new_TP.append(leftTP[ii])
                new_FP.append(leftFP[ii])
            else:
                if self.operator == "v":
                    new_TP.append( leftTP[ii] and rightTP[ii] )
                    new_FP.append( list(set(leftFP[ii]).intersection(rightFP[ii])) )

                elif self.operator == "∧":
                    new_TP.append(leftTP[ii] or rightTP[ii])
                    new_FP.append( list(set(leftFP[ii] + rightFP[ii])) )

                else:
                    print(self.operator)
                    sys.exit("Error: operator is not ∧ or v")
        return new_TP, new_FP



def generate_formulas(variables, operators, max_length):
    if max_length == 1:
        return variables
    formulas = []
    for length in range(1, max_length):
        for left in generate_formulas(variables, operators, length):
            remaining_length = max_length - length
            for right in generate_formulas(variables, operators, remaining_length):
                if isinstance(left, Literal) and isinstance(right, Literal) and \
                    left.name == right.name:
                    continue
                for operator in operators:
                    formulas.append(Formula(left, operator, right))
    return formulas




# # Define the variables and operators
# variables = [Literal("A"), Literal("B"), Literal("C"), Literal("D"), Literal("E")]
# operators = ["∧", "v"]

# # Generate and print formulas
# for length in range(1, 5):  # Lengths from 1 to 4
#     print(f"Formulas of length {length}:")
#     for formula in generate_formulas(variables, operators, length):
#         print(formula)
#         print(formula.evaluate())
#     print()
    