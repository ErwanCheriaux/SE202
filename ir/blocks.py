from ir.nodes import *
from frame.frame import Frame


def reorder_blocks(seq, frame):
    """Reorder blocks in seq so that the negative branch of a CJUMP always
    follows the CJUMP itself. frame is the frame of the corresponding
    function."""
    assert(isinstance(seq, SEQ))
    assert(isinstance(frame, Frame))

    # Ajout des jumps a la fin de chaque block n'en possedant pas
    # Rempli le dictionnaire contenant les blocks commancant par un label
    # et finnissant par un (c)jump
    dico = init_dico(seq)

    return seq

def init_dico(seq):

    is_block = False
    dico = {}
    list = []
    name = ""

    for stm in seq.stms:
        if isinstance(stm, LABEL):
            print("xxxxxx")
            print (stm.label)
            name = stm.label
            # Ajout d'un jump
            if is_block:
                list.append(JUMP(NAME(name)))
                dico[name] = list
            list = [stm]
            is_block = True
        elif isinstance(stm, JUMP):
            print (stm)
            list.append(stm)
            dico[name] = list
            is_block = False
        elif isinstance(stm, CJUMP):
            print (stm)
            print (stm.ifTrue.label)
            print (stm.ifFalse.label)
            list.append(stm)
            dico[name] = list
            is_block = False
        else:
            print (stm)
            list.append(stm)

    print("DICO START")

    for cle,valeur in dico.items():
        print (cle)
        for l in valeur:
            print (l)

    print("DICO END")

    return dico
