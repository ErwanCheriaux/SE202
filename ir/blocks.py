from ir.nodes import *
from frame.frame import Frame


class Block:
    """Block commencant par un label et terminant par un (c)jump"""

    def __init__(self, name, stms, cjump=None, jump=None, jumpTrue=None, jumpFalse=None):
        assert isinstance(name, Label), "name must be a Label"
        assert isinstance(stms, list), "stms must be a list of Stm"
        self.name      = name
        self.stms      = stms
        self.cjump     = cjump
        self.jump      = jump
        self.jumpTrue  = jumpTrue
        self.jumpFalse = jumpFalse
        self.exam      = False

    def display(self):
        print(self.name)

        for stm in self.stms:
            print(stm)

        if self.cjump: print(self.jumpTrue,self.jumpFalse)
        else:          print(self.jump)


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

    # Réordonne les blocks du dico
    list_reorder = init_list(dico)

    # Suppression des jump inutile
    list_reorder = linearisation(list_reorder)

    # Cette concaténation deviens le nouveau corps du nœud SEQ
    seq.stms = list_reorder
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
                dico[name] = Block(name=name, stms=list, cjump=False, jump=stm.label)
            # Initialisation name, list et is_block
            name = stm.label
            list = [stm]
            is_block = True
        elif isinstance(stm, JUMP):
            list.append(stm)
            dico[name] = Block(name=name, stms=list, cjump=False, jump=stm.target.label)
            is_block = False
        elif isinstance(stm, CJUMP):
            list.append(stm)
            dico[name] = Block(name=name, stms=list, cjump=True, jumpTrue=stm.ifTrue.label, jumpFalse=stm.ifFalse.label)
            is_block = False
        else:
            list.append(stm)
    # ajout du label end sans jump
    dico[name] = Block(name=name, stms=list)
    return dico


def init_list(dico):

    list = []

    for block in dico.values():
        for stm in analyse(block, dico):
            list.append(stm)
    return list


def analyse(block, dico):

    list = []
    next_label = ""

    if not block.exam:
        block.exam = True
        for stm in block.stms:
            list.append(stm)
        if block.cjump:
            # saut conditionnel
            next_label = block.jumpFalse
            if dico[next_label].exam:
                next_label = block.jumpTrue
                if dico[next_label].exam:
                    #jump vers un label fictif
                    next_label = "fictif"
                else:
                    #inversion de la condition et des labels vrai faux
                    dico[next_label].stms[-1].op = oppo(dico[next_label].stms[-1].op)
                    dico[next_label].stms[-1].ifTrue, dico[next_label].stms[-1].ifFalse = \
                        dico[next_label].stms[-1].ifFalse, dico[next_label].stms[-1].ifTrue
        else:
            # saut inconditionnel
            next_label = block.jump
        if next_label in dico:
            for stm in analyse(dico[next_label], dico):
                list.append(stm)
    return list

def oppo(str):
    if str == "<":    return ">="
    elif str == "<=": return ">"
    elif str == ">":  return "<="
    elif str == ">=": return "<"
    elif str == "==": return "!="
    elif str == "!=": return "=="
    elif str == "&":  return "|"
    elif str == "|":  return "&"
    else: raise AssertionError("Opperande doesn't manage %s" % str)

def linearisation(list):
    i = 0
    for l in list:
        if isinstance(l, LABEL):
            if isinstance(list[i-1], JUMP) and list[i-1].target.label == l.label:
                list.pop(i-1)
        i = i+1
    return list

def display_dico(dico):
    print("=== DICTIONNAIRE ===")
    for block in dico.values():
        block.display()
    print()


def display_list(list):
    print("=== LISTE ===")
    for stm in list:
        print(stm)
        if   isinstance(stm, LABEL): print(stm.label)
        elif isinstance(stm, JUMP):  print(stm.target.label)
        elif isinstance(stm, CJUMP): print(stm.ifTrue.label, stm.ifFalse.label)
    print()
