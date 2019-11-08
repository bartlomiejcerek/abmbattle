# -*- coding: utf-8 -*-
import random

#Parent class actually not needed 

class RandomStrategy():
    def __init__(self):
        pass
        
    def make_move(self, field, uid, poss_actions):
        return random.choice(poss_actions)
        