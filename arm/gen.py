from codegen.instr import LABEL as L, MOVE as M, OPER as O
from ir.nodes import *
from utils.visitor import *

class Gen:
    """This traverses a tree to generate instructions for a given function.

    This visitor is particular in that it returns different types for Stm
    and Sxp nodes:

        - Stm nodes return a list of Instr.
        - Sxp nodes return a pair with a list of Instr and a temporary
        containing the result.

    This way, we can define only one visitor for both kind of constructs."""

    def __init__(self, frame):
        self.frame = frame

    # Visitors are mandatory

    @visitor(None)
    def visit(self, node):
        raise AssertionError("no code generator for node {}".format(type(node)))

    # Visitors for Stm nodes

    @visitor(SEQ)
    def visit(self, seq):
        return [i for stm in seq.stms for i in stm.accept(self)]

    @visitor(JUMP)
    def visit(self, jmp):
        return [O("jmp {}".format(jmp.target.label.name), [], [], [jmp.target.label])]

    @visitor(CJUMP)
    def visit(self, cjump):
        left_stms, left_temp = cjump.left.accept(self)
        right_stms, right_temp = cjump.right.accept(self)
        if cjump.op == "=":
            op = "beq"
        elif cjump.op == "<>":
            op = "bne"
        elif cjump.op == "<":
            op = "blt"
        elif cjump.op == "<=":
            op = "ble"
        elif cjump.op == ">":
            op = "bgt"
        elif cjump.op == ">=":
            op = "bge"
        else:
            raise AssertionError("unimplemented operator {}".format(cjump.op))
        return left_stms + right_stms + [O("cmp {}, {}", srcs=[left_temp, right_temp]),
                                         O("{} {}".format(op, cjump.ifTrue.label.name),
                                           jmps=[cjump.ifTrue.label, cjump.ifFalse.label])]

    @visitor(LABEL)
    def visit(self, label):
        l = L("{}:".format(label.label), label.label)
        if label.label == self.frame.end_label:
            # The end label marks the place of the return instruction
            srcs = [self.frame.lr]
            if self.frame.returns_value:
                srcs.append(self.frame.r0)
            return [l, O("bx {}", srcs=srcs)]
        else:
            return [l]

    @visitor(MOVE)
    def visit(self, move):
        src_stms, src_temp = move.src.accept(self)
        if isinstance(move.dst, MEM):
            # If we try to move into memory, use a store
            dst_stms, dst_temp = move.dst.exp.accept(self)
            return src_stms + dst_stms + [O("str {1}, [{0}]", srcs=[src_temp, dst_temp])]
        else:
            # The only other possibility is a temporary, this is a move instruction
            return src_stms + [M("mov {}, {}", dst=move.dst.temp, src=src_temp)]

    @visitor(SXP)
    def visit(self, sxp):
        return sxp.exp.accept(self)[0]

    # Visitors for Sxp nodes

    @visitor(TEMP)
    def visit(self, temp):
        # Already in a temporary
        return [], temp.temp

    @visitor(CONST)
    def visit(self, const):
        temp = Temp.create("const")
        return [O("mov {{}}, #{}".format(const.value), dsts=[temp])], temp

    @visitor(MEM)
    def visit(self, mem):
        # Registre pour stocker le résultat
        temp = Temp.create("mem")
        # On évalue l'adresse du MEM
        adr_stms, adr_temp = mem.exp.accept(self)
        # On détermine les instructions à effectuer
        stms = adr_stms + [O("ldr {}, [{}]", dsts=[temp], srcs=[adr_temp])]
        # On retourne les instructions et le résultat
        return stms, temp

    @visitor(CALL)
    def visit(self, call):
        count = 0
        stms = []
        temp = Temp.create("call")

        # sauvegarde des registre 0 à 4 dans caller_save
        for caller_save_temp in self.frame.caller_save:
            dst_temp = Temp.create('caller_save')
            stms = stms + [M("mov {}, {}", dst=dst_temp, src=caller_save_temp)]

        # sauvegarde des arguments dans les 4 premiers reg et sur la pile
        for arg in call.args:
            args_stms, args_temp = arg.accept(self)
            if not count :
                self.frame.fp = args_temp
            elif count<=4:
                stms = stms + [M("mov {}, {}", dst=self.frame.caller_save[count-1], src=args_temp)]
            else:
                self.frame.param_regs.append(args_temp)
                stms = stms + args_stms + [O("push {}".format(args_temp), srcs=[args_temp])]
            count = count + 1

        stms = stms + [O("push {}".format(self.frame.fp), srcs=[self.frame.fp])]
        stms = stms + [O("bl {}".format(call.func.label), jmps=[call.func.label])]
        return stms, temp

    @visitor(BINOP)
    def visit(self, binop):
        temp = Temp.create("binop")
        left_stms, left_temp = binop.left.accept(self)
        right_stms, right_temp = binop.right.accept(self)
        if binop.op == "+":
            op = "add"
        elif binop.op == "-":
            op = "sub"
        elif binop.op == "*":
            op = "mul"
        elif binop.op == "/":
            op = "div"
        else:
            raise AssertionError("unimplemented operator {}".format(binop.op))
        stms = left_stms + right_stms + \
               [O("{} {}, {}, {}".format(op, temp, left_temp, right_temp),\
                    dsts=[temp], srcs=[left_temp, right_temp])]
        return stms, temp
