import time
import classes
import constants
import keyboard
import numpy as np
import math

SIDE = np.random.random() > 0.5
spaces = 0
score = 0
def func(args: keyboard._keyboard_event.KeyboardEvent):
    global spaces
    if args.name == 'space':
        spaces += 1

keyboard.on_press(func)
for i in range(20):
    if SIDE:
        print('Stay on the RIGHT!', )
    else:
        print('Stay on the LEFT!', )
    
    time.sleep(2/40)
    print("\033[0;0H\033[2J")
    time.sleep(2/30)
    
input('Press Enter to continue')

keep_target = False
run = False

def render(player: classes.player, left_wall: str, right_wall: str, i: int):
    global keep_target, run, score
    lost = False
    output_string = ''
    c = 0
    if player.jumping and not run:
        keep_target = constants.PLAY_SPACE-1
        run = True
    elif run and not player.jumping:
        keep_target = False
        run = False
    for l, r in zip(left_wall[i:math.floor(constants.PLAY_SPACE*1.5)+i], right_wall[i:i+math.floor(constants.PLAY_SPACE*1.5)]):

        if c==0:
            if player.side:
                output_string += l+(' '*(constants.PLAY_SPACE-player.jump_progress-1))+constants.PLAYER+(' '*player.jump_progress)+r+'\n'
                if output_string.endswith(constants.PLAYER+' \n'):
                    lost = True
            else:
                output_string += l+(' '*(player.jump_progress))+constants.PLAYER+(' '*(constants.PLAY_SPACE-player.jump_progress-1))+r+'\n'
                if output_string[:2] == ' '+constants.PLAYER:
                    lost = True
            # output_string += l+(' '*int(not player.side)*(constants.PLAY_SPACE-player.jump_progress-1))+(constants.PLAYER*(int(not player.side)))+(' '*int(not player.side)*(abs(player.jump_progress-constants.PLAY_SPACE)-1))+(' '*int(player.side)*(constants.PLAY_SPACE-player.jump_progress-1))+(constants.PLAYER*int(player.side))+(' '*int(player.side)*(abs(player.jump_progress-constants.PLAY_SPACE)-1))+r+'\n'
        elif c!=(constants.PLAY_SPACE) and keep_target!=c:
            output_string += l+(' '*constants.PLAY_SPACE)+r+'\n'
        elif c==constants.PLAY_SPACE and (keep_target==False):
            # if keep_target==False:
            if not player.side:
                output_string += l+(' '*(constants.PLAY_SPACE-1))+constants.TARGET_SQUARE+r+'\n'
            else:
                output_string += l+constants.TARGET_SQUARE+(' '*(constants.PLAY_SPACE-1))+r+'\n'
        elif run and (keep_target==c):
            if keep_target==c:
                if not player.side:
                    output_string += l+(' '*(constants.PLAY_SPACE-1))+constants.TARGET_SQUARE+r+'\n'
                else:
                    output_string += l+constants.TARGET_SQUARE+(' '*(constants.PLAY_SPACE-1))+r+'\n'

        c+=1
    if keep_target!=False:
        keep_target-=1
        if keep_target==1:
           keep_target = False
    print("\033[0;0H\033[2J")
    if SIDE:
        print('Stay on the RIGHT!\n\n')
    else:
        print('Stay on the LEFT!\n\n')
    print(output_string)
    if lost:
        print('You LOST!')
    if not player.jumping:
        if player.side == SIDE:
            score += 1
        else:
            score -= 1
    print(f'\n\nScore: {score}')
    if lost:
        exit()

def main():
    global spaces


    i = 0
    left = [classes.wall(20, 0), *[classes.wall(np.random.randint(1, 5), 0, np.random.random() > 0.45) for i in range(1000)]]
    right = [classes.wall(20, 1), *[classes.wall(np.random.randint(1, 5), 1, np.random.random() > 0.45) for i in range(1000)]]
    left_wall, right_wall = ('', '')
    for l, r in zip(left, right):
        left_wall += l.string
        right_wall += r.string
        
    player = classes.player(SIDE)
    jumping = False
    while True:
        if spaces > 0 and not jumping:
            jumping = player.jump()
            spaces -= 1
        elif jumping:
            jumping = player.jump()
        render(player, left_wall, right_wall, i)
        time.sleep(0.135)
        i+=1
    
main()