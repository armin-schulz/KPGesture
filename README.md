### OPTIONS
Default options should work fine. If needed edit: 


`DRAW_LENGTH`__int__: number of points remembered = length of line [maximal 765] \
&nbsp;&nbsp;&nbsp;&nbsp; default = 50 \
`THICKNESS` __int__ *: thickness of first line* \
&nbsp;&nbsp;&nbsp;&nbsp; default = 50 \
`JUMP_LIMIT` __int__ *: threshold of distance recognized as possible between two frames* \
&nbsp;&nbsp;&nbsp;&nbsp; default = 200 \
`SIDE` __str__: *which hand is drawn*: BOTH, LEFT, RIGHT \
&nbsp;&nbsp;&nbsp;&nbsp; default = 200 \
`COOLDOWN_AUTO` __int__ *: number of frames that have to pass between an auto snapshot and the last snapshot* \
&nbsp;&nbsp;&nbsp;&nbsp; default = 250 \
`COOLDOWN_MANUAL` __int__ *: number of frames that have to pass before a manual snapshot is possible again after a manual snapshot* 
&nbsp;&nbsp;&nbsp;&nbsp; default = 25 

__pyinstaller__ command to create .exe \
`pyinstaller --onefile --add-data="logging_config.json;." --add-data=".venv\Lib\site-packages\mediapipe\modules\hand_landmark;mediapipe\modules\hand_landmark" --add-data=".venv\Lib\site-packages\mediapipe\modules\palm_detection;mediapipe\modules\palm_detection" app.py
`

#### Modes
- exploration: live, enhanced, schematic image; paint only moving fingertips, straight fingers  
- painting: paint queue of last `DRAW_LENGTH` points
- painting_static paint all recorded points

#### Keys in painting_static
- q...quit
- f...make photo (if cooldown is zero)
- r...reset painting

