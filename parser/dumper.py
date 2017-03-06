from ast.nodes import *
from utils.visitor import *


class Dumper(Visitor):

    def __init__(self, semantics):
        """Initialize a new Dumper visitor. If semantics is True,
        additional information will be printed along with declarations
        and identifiers."""
        self.semantics = semantics

    @visitor(None)
    def visit(self, node):
        raise Exception("unable to dump %s" % node)

    @visitor(IntegerLiteral)
    def visit(self, i):
        return str(i.intValue)

    @visitor(BinaryOperator)
    def visit(self, binop):
        # Always use parentheses to reflect grouping and associativity,
        # even if they may be superfluous.
        return "(%s %s %s)" % \
               (binop.left.accept(self), binop.op, binop.right.accept(self))

    @visitor(IfThenElse)
    def visit(self, c):
        return "if %s then %s else %s" % \
                (c.condition.accept(self), c.then_part.accept(self), c.else_part.accept(self))

    @visitor(Let)
    def visit(self, let):
        d = ""
        e = ""
        for decl in let.decls:
            d += decl.accept(self)
        for exp  in let.exps:
            e += exp.accept(self)
        return "let %s in %s end" % (d, e)

    @visitor(Type)
    def visit(self, type):
        return "%s" % (type.typename)

    @visitor(VarDecl)
    def visit(self, var):
        if var.type == None:
            return "var %s := %s" % (var.name, var.exp.accept(self))
        elif var.exp == None:
            return "%s: %s" % (var.name, var.type.accept(self))
        else:
            return "var %s: %s := %s" % (var.name, var.type.accept(self), var.exp.accept(self))

    @visitor(FunDecl)
    def visit(self, fun):
        a = ""
        for arg in fun.args:
            a += arg.accept(self)
        if fun.type == None:
            return "function %s(%s) = %s" % \
                (fun.name, a, fun.exp.accept(self))
        else:
            return "function %s(%s): %s = %s" % \
                (fun.name, a, fun.type.accept(self), fun.exp.accept(self))

    @visitor(Identifier)
    def visit(self, id):
        if self.semantics:
            diff = id.depth - id.decl.depth
            scope_diff = "{%d}" % diff if diff else ''
        else:
            scope_diff = ''
        return '%s%s' % (id.name, scope_diff)
