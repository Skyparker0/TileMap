# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:36:56 2020

@author: batte
"""

#THIS IS NOT TO BE USED. IT ONLY MAKES SENSE IF I EXPLAIN IT, WHICH I WILL NOT DO RIGHT NOW

from tkinter import *  
from PIL import ImageTk,Image 
import os
import random

class changingButton:
    
    def __init__(self,master, choices,row,column):
        
        self.button = Button(master, command=self.next_choice, width= 5, height = 5)
        self.button.grid(row=row, column=column)
        
        self.choices = choices
        
        self.choiceNum = 0
        
        self.update_text()
        
        
    def update_text(self):
        self.button["text"] = self.choices[self.choiceNum]
        
    def next_choice(self):
        self.choiceNum += 1
        self.choiceNum %= len(self.choices)
        self.update_text() 
        
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

def save_next():
    global startFilesIndex
    if startFilesIndex < len(startFiles):
    
        if startFilesIndex < len(startFiles)-1:
            img = ImageTk.PhotoImage(Image.open(startFiles[startFilesIndex+1]).resize((200,200)))  
            image.configure(image=img)
            image.image = img
        
        newName = ''
        
        for button in buttons: 
            newName += str(button.choiceNum)
            button.choiceNum = 0
            button.update_text()
        
        namedFiles.append(newName)
        newName += ' abcdefghijklmnopqrstuvwzyz'[namedFiles.count(newName)] + '.png'
        os.rename(startFiles[startFilesIndex], path + '/' + newName)
        print('renamed ' + newName + ' -- ' + str(startFilesIndex + 1) + ' of ' + str(len(startFiles)))
        
        startFilesIndex += 1
        #canvas.delete('all') 
    
    
    
    
    

#path = 'C:/Users/batte/OneDrive/_Parker/Python/Carcassonne/RealTilepics'

namedFiles = []
startFiles = find_all(path)[0]
for file in startFiles:
    os.rename(file, path+ '\\' + str(random.random()) + '.png')
startFiles = find_all(path)[0]

startFilesIndex = 0

root = Tk()  
root.lift()

frame = Frame(root)
frame.grid()

img = ImageTk.PhotoImage(Image.open(startFiles[startFilesIndex]).resize((200,200)))  
image = Label(frame, image = img)
image.grid(row=1, column=1)

buttons = [changingButton(frame, ['grass','city','road','river'], c[0], c[1]) for c in [(0,1), (1,2), (2,1), (1,0)]]
saveButton = Button(frame, command = save_next, text = 'Finish')
saveButton.grid(row = 3, column = 4)

root.mainloop() 


