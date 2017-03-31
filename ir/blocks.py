from ir.nodes import *
from frame.frame import Frame


def reorder_blocks(seq, frame):
    """Reorder blocks in seq so that the negative branch of a CJUMP always
    follows the CJUMP itself. frame is the frame of the corresponding
    function."""
    assert(isinstance(seq, SEQ))
    assert(isinstance(frame, Frame))

    dico = {}
    list = []
    name = ""

    for stm in seq.stms:
        if isinstance(stm, LABEL):
            print("xxxxxx")
            print (stm.label)
            name = stm.label
            list = [stm]
        elif isinstance(stm, JUMP) or isinstance(stm, CJUMP):
            print (stm)
            list.append(stm)
            dico[name] = list
        else:
            print (stm)
            list.append(stm)

    print("DICO START")

    for cle,valeur in dico.items():
        print (cle)
        for l in valeur:
            print (l)

    print("DICO END")

    return seq
