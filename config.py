MAX_QUEUE_LENGTH: int = 30  # --> length of drawn line; max 3 * 255
DRAW_THICKNESS = 50         # --> maximal thickness of drawn line and line start
MAX_FRAME_DISTANCE = 200    # --> tolerated distance of finger position between two frames (smaller value prevents jumps between right and left)
AUTO_COOLDOWN = 250         # --> number of frames that have to pass since the last made picture until an automatic picture is made
MANUAL_COOLDOWN = 25        # --> minimal number of frames between two manual triggered pictures

DEFAULT_MODE: str = 'painting'
###
MODE: str = 'painting'
