import constants
import functools
import itertools

class player:
    '''Represents a player'''
    def __init__(self, side: bool) -> None:
        self.side = side
        self.jumping = False
        self.jump_progress = 0
        
    def jump(self) -> bool:
        
        self.jumping = True
        self.jump_progress += 1
        if self.jump_progress==constants.PLAY_SPACE:
            self.stop_jump()
            return False
        return True
    
    def stop_jump(self):
        self.jumping = False
        self.jump_progress = 0
        self.side = not self.side
        
class wall:
    '''Represents part of a side.'''
    def __init__(self, length: int, side: bool, solid: bool=True) -> None:
        self.length = length
        self.solid = solid
        self.side = side
        self.touched = False
        self.string = constants.SQUARE*length if solid else constants.HOLLOW_SQUARE*length

    def interact(self) -> None:
        '''Run this when this wall is touched.'''
        self.touched = True

    def __iter__(self):
        return iter(self.string)
    
    def __str__(self) -> str:
        return self.string
    
    def __repr__(self) -> str:
        return self.string
