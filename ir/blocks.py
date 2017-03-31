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

    #debug
    display_dico(dico)

    return seq

def init_dico(seq):

    is_block = False
    dico = {}
    list = []
    name = ""

    for stm in seq.stms:
        if isinstance(stm, LABEL):
            # Ajout d'un jump
            if is_block:
                list.append(JUMP(NAME(stm.label)))
                dico[name] = list
            # Initialisation name, list et is_block
            name = stm.label
            list = [stm]
            is_block = True
        elif isinstance(stm, JUMP):
            list.append(stm)
            dico[name] = list
            is_block = False
        elif isinstance(stm, CJUMP):
            list.append(stm)
            dico[name] = list
            is_block = False
        else:
            list.append(stm)

    return dico

def display_dico(dico):
    for cle,valeur in dico.items():
        print(cle)
        for l in valeur:
            print(l)
            if   isinstance(l, JUMP):  print(l.target.label)
            elif isinstance(l, CJUMP): print(l.ifTrue.label, l.ifFalse.label)
