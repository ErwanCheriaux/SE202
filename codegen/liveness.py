from codegen.instr import LABEL as L, MOVE as M, OPER as O
from ir.nodes import *

def liveness_analysis(frame, instrs):
    """Annotate instructions with liveness analysis. Return the interferences
    and coalesces dictionaries as a pair.

    The interferences dictionary gives, for every temporary, the list of
    temporaries it conflicts with.

    The coalesces dictionary gives, for every temporary, the list of other
    temporaries involved in a direct MOVE operation. Those are susceptible
    of merging."""

    debug = True

    interferences = {}
    coalesces = {}

    for i in instrs:
        # At any nonmove instruction that defines a variable a, where the live-out
        # variables are b 1 , ... , b j , add interference edges
        # (a, b 1 ), ... , (a, b j ).
        if isinstance(i, O) and len(i.dsts) == 1:
            key = i.dsts[0].name
            interferences[key] = i.srcs

        # At a move instruction a ← c, where variables b 1 , ... , b j are live-out,
        # add interference edges (a, b 1 ), ... , (a, b j ) for any b i that is
        # not the same as c.
        if isinstance(i, M):
            pass

    if debug:
        print("=================== FRAME ====================")
        print(frame)

        print("=================== INSTRS ===================")
        for i in instrs:
            print(i)

        print("=============== INTERFERENCES ================")
        for key, value in interferences.items():
            print (key, value)

        print("==============================================")

    return interferences, coalesces
