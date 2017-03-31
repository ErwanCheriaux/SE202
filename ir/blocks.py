from ir.nodes import *
from frame.frame import Frame

class Block:
    """Block commencant par un label et terminant par un (c)jump"""

    def __init__(self, name, stms, cjump, jump=None, jumpTrue=None, jumpFalse=None):
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

    # debug
    display_dico(dico)

    # Réordonne les blocks du dico
    list_reorder = init_list(dico)

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

    return dico

def init_list(dico):
    list = []
    next_label = ""

    for block in dico.values():
        list = analyse(block)

    return list

def analyse(block):
    if not block.exam:
        block.exam = True
        list.append(block.stm)
        if block.cjump:
            next_label = block.jumpFalse
        else:
            next_label = block.jump
        analyse(dico[next_label])
    return list

def display_dico(dico):
    print("=== DICTIONNAIRE ===")
    for block in dico.values():
        block.display()
