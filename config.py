from chirality import Chirality

DRAW_LENGTH: int = 50               # --> length of drawn line; max 3 * 255
THICKNESS: int = 50                 # --> maximal thickness of drawn line and line start
JUMP_LIMIT: int = 200               # --> tolerated distance of finger position between two frames (smaller value prevents jumps between right and left)
SIDE: Chirality = Chirality.BOTH    # --> which hand's index is drawn
COOLDOWN_AUTO: int = 250            # --> number of frames that have to pass since the last made picture until an automatic picture is made
COOLDOWN_MANUAL: int = 25           # --> minimal number of frames between two manual triggered pictures

DEFAULT_MODE: str = 'painting'

