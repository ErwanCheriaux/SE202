from ast.nodes import *
from utils.visitor import visitor

class Evaluator:
    """This contains a simple evaluator visitor which computes the value
    of a tiger expression."""

    @visitor(IntegerLiteral)
    def visit(self, int):
        return int.intValue

    @visitor(BinaryOperator)
    def visit(self, binop):
        left  = binop.left.accept(self)
        op    = binop.op

        #permets de ne pas analyser la partie droite si ce n'est pas nécessaire
        if op == '&' and left == 0:
            return 0
        elif op == '|' and left != 0:
            return 1

        right = binop.right.accept(self)

        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return int(left / right)
        elif op == '|':
            return 1 if left or right else 0
        elif op == '&':
            return 1 if left and right else 0
        elif op == '<':
            return (left < right)*1
        elif op == '>':
            return (left > right)*1
        elif op == '<=':
            return (left <= right)*1
        elif op == '>=':
            return (left >= right)*1
        elif op == '=':
            return (left == right)*1
        elif op == '<>':
            return (left != right)*1
        else:
            raise SyntaxError("unknown operator %s" % op)

    @visitor(IfThenElse)
    def visit(self, c):
        condition = c.condition.accept(self)

        if type(condition) != int:
            raise SyntaxError("wrong condition %s" % condition)
        elif condition != 0:
            return c.then_part.accept(self)
        else:
            return c.else_part.accept(self)

    @visitor(VarDecl)
    def visit(self, var):
        name = var.name.accept(self)
        return var.exp.accept(self)

    @visitor(None)
    def visit(self, node):
        raise SyntaxError("no evaluation defined for %s" % node)
