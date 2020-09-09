# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 16:47:37 2020

@author: batte
"""

import numpy as np
import random

import os
from PIL import Image


def find_all(path, firstletters = ''):
    '''
    path = The path to the folder containing the files wanted
    firstletters = int or a string containing int
    
    returns a list of file's (paths and names) in a path that have names starting 
    with firstletters '''
    
    
    result = []    #will hold paths
    names = []      #will hold names of files in path
    
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.startswith(str(firstletters)):
                result.append(os.path.join(root, name))
                names.append(name)
    return result, names


class tileMap:
    '''Represents a numpy array that holds tile values'''
    
    def __init__(self, width, height, tiles):
        '''
        width = int
        height = int
        tiles = list of strings usable tiles
        
        initializes all variables needed'''
        self.width = width
        self.height = height
        self.tiles = tiles
        
        self.tileArray = np.array([['11110']*height]*width) ########<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.tileArray[1:width-1,1:height-1] = '#####'
        
    def place_tile(self, tile, x, y):
        '''
        tile = str
        x = int
        y = int
        
        attempts to place tile at x,y of the tileArray
        if succesful, tileArray[x,y] will be tile + 0,1,2,3
        returns True if succesful, False if not'''
        
        if self.tileArray[x,y] == '#####' and \
            (0 < x < self.width-1 and 0 < y < self.height-1):
            
            
            for rotation in range(4):
                rotatedTile = tile + str(rotation)
                
                canPlace = True
                for checkDirection in [(-1,0,0),(0,1,1),(1,0,2),(0,-1,3)]:  #xchange,ychange,checkSide
                    tileSides = self.tile_sides(rotatedTile, (x+checkDirection[0], y+checkDirection[1]), checkDirection[2])
                    if tileSides[0] != tileSides[1]:
                        canPlace = False
                        break
                if canPlace:
                    self.tileArray[x,y] = rotatedTile
                    return True

        return False
                
    
    def try_all_placement(self, x,y):  
        '''
        x = int
        y = int
        
        Tries to place all tiles on a coordinate'''    
        
        randomTiles = self.tiles
        random.shuffle(randomTiles)
        
        for tile in randomTiles:
            if self.place_tile(tile,x,y):
                break
            
    def fill_array(self):
        '''Fills the entire array with tiles'''
        
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                self.try_all_placement(x,y)
                
        
    
    def rotated_tile(self, tile):
        '''
        tile = string
        
        returns the tile rotated as a string'''
        
        rotation = int(tile[4])
        
        newTile = ''.join([tile[(x - rotation)%4] for x in range(4)])
        
        return newTile
    
    def tile_sides(self, tile, pos2, checkSide):
        '''
        tile = string of original tile
        pos2 = cordinate in the tileArray adjacent to pos1
        checkSide = any of 0,1,2,3 -- 0 is top 1 is right, etc.
        
        returns (value of checkSide, touching side value of pos2)
        '''
        
        tile1 = self.rotated_tile(tile)
        try:
            tile2 = self.rotated_tile(self.tileArray[pos2])
        except:
            tile2 = self.rotated_tile(tile1 + '2')
                
        return (tile1[checkSide], tile2[(checkSide+2)%4])
    
        
path = 'C:/Users/batte/OneDrive/_Parker/Python/Carcassonne/Wang_2'     


tilePaths, names = find_all(path)


tiles = [x[0:4] for x in names]    #first four charecters

width = 30
height = 30

tileArray = ['#####']
tryCount = 0
while '#####' in tileArray and tryCount < 300:
    tMap = tileMap(width,height,tiles)
    tMap.fill_array()
    
    tileArray = tMap.tileArray
    tryCount += 1



newImage = Image.new('RGB', (50*width, 50*height), color = (0,100,0))

for x in range(1,width-1):
    for y in range(1,height-1):
        tile = tileArray[y,x]
        rotation = int(tile[4]) if tile[4] != '#' else 0
        tile = tile[:4]
        paths,names = find_all(path, tile)
        chosen = random.choice(paths)
        if not (0 < x < width-1 and 0 < y < height-1):
            chosen = paths[0]
        tile = Image.open(chosen)
        tile = tile.resize((50,50))
        tile = tile.rotate(360 - 90*rotation)
        if not (0 < x < width-1 and 0 < y < height-1):
            tile = tile.rotate(360 - random.randint(0, 4)*rotation)
        newImage.paste(tile,(x*50,y*50))
        
newImage.show()
