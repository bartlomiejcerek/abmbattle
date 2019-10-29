# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:03:00 2019

@author: Bartek
"""

import random 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as clrs

class Engine:
    def __init__(self,field):
        self.field = field
        #For simple vizualization
    
    def makeRandomMove(self):
        '''Performs random move with each unit'''
        units = self.field.units
        uids = list(units.keys())

        for uid in uids:
            #Check if unit is not dead
            if uid not in units.keys():
                continue 
            available_acts = self.field.getAvailableActions(uid)
            action, args = random.choice(available_acts)
            # Perform Action (explicit passing of object)
            action(self.field, *args)
            
    def checkState(self):
        '''This function in futre will return info about mode, now only if over'''
        #Obtain set of teams
        teams = [self.field.units[k][0] for k in self.field.units.keys()]
        teams = set(teams)
        if len(teams) == 1:
            return True 
        else:
            return False
    
    def simpleVizualization(self):
        '''Simple vizualization method - works only for 2 teams'''
        cmap = clrs.ListedColormap(['black','white','red','blue'])

        ###HARDCODED###
        teams = np.zeros(self.field.uid_map.shape)
        for (x,y), value in np.ndenumerate(self.field.uid_map):
            if self.field.uid_map[x,y] in range (1,3):
                teams[x,y] = 1
                continue
            if self.field.uid_map[x,y] > 2:
                teams[x,y] = 2
            else:
                teams[x,y] = self.field.uid_map[x,y]
        ###HARDCODED###
        fig , ax = plt.subplots(1,1, figsize= (8,8))
        ax.set_xticks([])
        ax.set_yticks([])
        plt.imshow(teams, cmap=cmap)