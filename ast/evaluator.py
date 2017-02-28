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
        left, right = binop.left.accept(self), binop.right.accept(self)
        op = binop.op
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '|':
            return left | right
        elif op == '&':
            return left & right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '=':
            return left == right
        elif op == '<>':
            return left != right
        else:
            raise SyntaxError("unknown operator %s" % op)

@visitor(IfThenElse)
def visit(self, c):
    condition = c.condition.accept(self)
    then_part = c.then_part.accept(self)
    else_part = c.else_part.accept(self)
    children  = c.children
    if condition == True:
        return then_part
    elif condition == False:
        return else_part
    else:
        raise SyntaxError("unknown cond %s" % condition)

    @visitor(None)
    def visit(self, node):
        raise SyntaxError("no evaluation defined for %s" % node)
