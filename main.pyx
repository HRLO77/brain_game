# cython: language_level=3
# distutils: language=c
# cythhon: binding=False
# cython: infer_types=False
# cython: wraparound=False
# cython: boundscheck=False
# cython: cdivision=True
# cython: overflowcheck=False
# cython: nonecheck=False
# cython: initializedcheck=False
# cython: always_allow_keywords=False
# cython: c_api_binop_methods=True
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

import time
import classes
import constants
import keyboard
import numpy as np
import math
#cimport numpy as npc
from libc.stdio cimport printf, puts
#npc.import_array()
cdef bint SIDE = np.random.random() > 0.5
cdef unsigned short spaces = 0
cdef unsigned short score = 0
cpdef void func(args: keyboard._keyboard_event.KeyboardEvent):
    global spaces
    if args.name == 'space':
        spaces += 1

keyboard.on_press(func)
if SIDE:
    puts('Stay on the RIGHT!')
else:
    puts('Stay on the LEFT!')
time.sleep(3)
print("\033[0;0H\033[2J")

    
input('Press Enter to continue')


cdef bint keep_target = False
cdef bint run = False
cdef unsigned short target = 0
cdef void render(player: classes.player, left_wall: str, right_wall: str, const unsigned long long int i):
    global keep_target, run, score, target
    cdef bint lost = False
    cdef str output_string = ''
    cdef unsigned short c = 0
    if player.jumping and not run:
        target = constants.PLAY_SPACE-1
        keep_target = True
        run = True
    elif run and not player.jumping:
        keep_target = False
        target = 0
        run = False
    for l, r in zip(left_wall[i:math.floor(constants.PLAY_SPACE*1.5)+i], right_wall[i:i+math.floor(constants.PLAY_SPACE*1.5)]):

        if c==0:
            if player.side:
                output_string += (l+(' '*(constants.PLAY_SPACE-player.jump_progress-1))+constants.PLAYER+(' '*player.jump_progress)+r+'\n')
                if output_string.endswith(constants.PLAYER+' \n'):
                    lost = True
            else:
                output_string += (l+(' '*(player.jump_progress))+constants.PLAYER+(' '*(constants.PLAY_SPACE-player.jump_progress-1))+r+'\n')
                if output_string[:2] == (' '+constants.PLAYER):
                    lost = True
            # output_string += l+(' '*int(not player.side)*(constants.PLAY_SPACE-player.jump_progress-1))+(constants.PLAYER*(int(not player.side)))+(' '*int(not player.side)*(abs(player.jump_progress-constants.PLAY_SPACE)-1))+(' '*int(player.side)*(constants.PLAY_SPACE-player.jump_progress-1))+(constants.PLAYER*int(player.side))+(' '*int(player.side)*(abs(player.jump_progress-constants.PLAY_SPACE)-1))+r+'\n'
        elif c!=(constants.PLAY_SPACE) and target!=c:
            output_string += (l+(' '*constants.PLAY_SPACE)+r+'\n')
        elif c==constants.PLAY_SPACE and (not keep_target):
            # if keep_target==False:
            if not player.side:
                output_string += (l+(' '*(constants.PLAY_SPACE-1))+constants.TARGET_SQUARE+r+'\n')
            else:
                output_string += (l+constants.TARGET_SQUARE+(' '*(constants.PLAY_SPACE-1))+r+'\n')
        elif run and (target==c):
            if target==c:
                if not player.side:
                    output_string += (l+(' '*(constants.PLAY_SPACE-1))+constants.TARGET_SQUARE+r+'\n')
                else:
                    output_string += (l+constants.TARGET_SQUARE+(' '*(constants.PLAY_SPACE-1))+r+'\n')

        c+=1
    if keep_target!=False:
        target-=1
        if target==1:
           keep_target = False
           target = 0
    puts("\033[0;0H\033[2J\n")
    if SIDE:
        puts('Stay on the RIGHT!\n\n\n')
    else:
        puts('Stay on the LEFT!\n\n\n')
    print(output_string)
    if lost:
        printf('You LOST!\n')
    if not player.jumping:
        if player.side == SIDE:
            score += 1
        else:
            score -= 1
    printf('\n\nScore: %u', score)
    if lost:
        exit()

cdef void start(list left, list right):
    global spaces
    cdef str left_wall
    cdef str right_wall

    cdef unsigned short i = 0
    left_wall, right_wall = ('', '')
    for l, r in zip(left, right):
        left_wall += l.string
        right_wall += r.string
        
    player = classes.player(SIDE)
    cdef bint jumping = False
    while True:
        if spaces > 0 and not jumping:
            jumping = player.jump()
            spaces -= 1
        elif jumping:
            jumping = player.jump()
        render(player, left_wall, right_wall, i)
        time.sleep(0.135)
        i+=1
    
start([classes.wall(20, 0), *[classes.wall(np.random.randint(1, 5), 0, np.random.random() > 0.45) for i in range(1000)]],[classes.wall(20, 1), *[classes.wall(np.random.randint(1, 5), 1, np.random.random() > 0.45) for i in range(1000)]])