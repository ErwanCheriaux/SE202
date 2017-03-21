from ast.nodes import *
from utils.visitor import *


class BindException(Exception):
    """Exception encountered during the binding phase."""
    pass


class Binder(Visitor):
    """The binder takes care of linking identifier uses to its declaration. If
    will also remember the depth of every declaration and every identifier,
    and mark a declaration as escaping if it is accessed from a greater depth
    than its definition.

    A new scope is pushed every time a let, function declaration or for loop is
    encountered. It is not allowed to have the same name present several
    times in the same scope.

    The depth is increased every time a function declaration is encountered,
    and restored afterwards.

    A loop node for break is pushed every time we start a for or while loop.
    Pushing None means that we are outside of break scope, which happens in the
    declarations part of a let."""

    def __init__(self):
        """Create a new binder with an initial scope for top-level
        declarations."""
        self.depth = 0
        self.scopes = []
        self.push_new_scope()
        self.break_stack = [None]

    def push_new_scope(self):
        """Push a new scope on the scopes stack."""
        self.scopes.append({})

    def pop_scope(self):
        """Pop a scope from the scopes stack."""
        del self.scopes[-1]

    def current_scope(self):
        """Return the current scope."""
        return self.scopes[-1]

    def push_new_loop(self, loop):
        """Push a new loop node on the break stack."""
        self.break_stack.append(loop)

    def pop_loop(self):
        """Pop a loop node from the break stack."""
        del self.break_stack[-1]

    def current_loop(self):
        loop = self.break_stack[-1]
        if loop is None:
            raise BindException("break called outside of loop")
        return loop

    def add_binding(self, decl):
        """Add a binding to the current scope and set the depth for
        this declaration. If the name already exists, an exception
        will be raised."""
        if decl.name in self.current_scope():
            raise BindException("name already defined in scope: %s" %
                                decl.name)
        self.current_scope()[decl.name] = decl
        decl.depth = self.depth

    def lookup(self, identifier):
        """Return the declaration associated with a identifier, looking
        into the closest scope first. If no declaration is found,
        raise an exception. If it is found, the decl and depth field
        for this identifier are set, and the escapes field of the
        declaration is updated if needed."""
        name = identifier.name
        for scope in reversed(self.scopes):
            if name in scope:
                decl = scope[name]
                identifier.decl = decl
                identifier.depth = self.depth
                decl.escapes |= self.depth > decl.depth
                return decl
        else:
            raise BindException("name not found: %s" % name)

    @visitor(None)
    def visit(self, node):
        raise Exception("unable to bind %s" % node)

    @visitor(IntegerLiteral)
    def visit(self, i):
        pass

    @visitor(BinaryOperator)
    def visit(self, binop):
        binop.left.accept(self)
        binop.right.accept(self)

    @visitor(Assignment)
    def visit(self, a):
        a.identifier.accept(self)
        a.exp.accept(self)

    @visitor(Let)
    def visit(self, let):
        self.push_new_scope()
        for decl in let.decls:
            decl.accept(self)
        for exp in let.exps:
            exp.accept(self)
        self.pop_scope()

    @visitor(Identifier)
    def visit(self, id):
        self.lookup(id)
        if type(id.decl) is not VarDecl:
            raise BindException("Is not a variable: %s" % id.name)

    @visitor(IfThenElse)
    def visit(self, c):
        c.condition.accept(self)
        c.then_part.accept(self)
        if c.else_part is not None:
            c.else_part.accept(self)

    @visitor(VarDecl)
    def visit(self, var):
        if var.exp != None:
            var.exp.accept(self)
        self.add_binding(var)

    @visitor(FunDecl)
    def visit(self, fun):
        self.add_binding(fun)
        self.push_new_scope()
        self.depth += 1
        for arg in fun.args:
            arg.accept(self)
        fun.exp.accept(self)
        self.pop_scope()
        self.depth -= 1

    @visitor(FunCall)
    def visit(self, fun):
        fun.identifier.decl = self.lookup(fun.identifier)
        if type(fun.identifier.decl) is not FunDecl:
            raise BindException("Is not a function: %s" % fun.identifier.name)
        if len(fun.identifier.decl.args) != len(fun.params):
            raise BindException("Not the right number of param for the function: %s" % fun.identifier.name)

    @visitor(SeqExp)
    def visit(self, sq):
        for exp in sq.exps:
            exp.accept(self)

    @visitor(While)
    def visit(self, w):
        w.condition.accept(self)
        w.exp.accept(self)

    @visitor(For)
    def visit(self, f):
        f.indexdecl.accept(self)
        f.low_bound.accept(self)
        f.high_bound.accept(self)
        self.push_new_loop(f)
        f.exp.accept(self)
        self.pop_loop()

    @visitor(IndexDecl)
    def visit(self, i):
        self.add_binding(i)
