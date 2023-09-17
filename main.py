#All code is mine except the ButtonClass.py. Credits to TechWithTim for sharing it.
from platform import system
import pygame as pg
from math import floor
from tkinter import *
from tkinter import messagebox
from time import sleep
from ButtonClass import Button #ButtonClass is borrowed from TechWithTim YT channel
from string import ascii_lowercase
import wordguesser
import converListToString as cls

def get_OS():
    system_name = system().lower()
    seperator = ""
    if system_name == "linux":
        seperator = "/"
    elif system_name == 'lindows':
        seperator = '\\'
    return seperator

def startNewGame():
    global number_of_tries, lines_list, letters_list, letters, secret_word
    
    while True: #so that no repeated words are chosen in any of the rounds
        secret_word = wordguesser.chooseRandomWord()
        if secret_word not in prev_secret_words:
            break
    
    prev_secret_words.append(secret_word)
    number_of_tries = 0 
    lines_list = []
    for i in secret_word:#create a list of lines to draw them in the screen
        lines_list.append('_')
    letters_list = lines_list.copy()
    letters = ascii_lowercase

def drawButtons():
    count = 0 #will count the times the loop will run, needed to position letters in rows, provided a row fits 9 columns
    substractor = 0
    letter_buttons_x, letter_buttons_y = width/6, height/2
    letters_buttons_horizontal_distance = int(width/13)
    
    for i in range(0, letters_buttons_horizontal_distance*len(letters), letters_buttons_horizontal_distance):
        if count > 0 and count % 9 == 0: #to seperate in as many rows as needed
            letter_buttons_y += height/10
            substractor = i
        btn_position = letter_buttons_x+i-substractor
        btn = Button((255, 255, 255),btn_position, letter_buttons_y,50,50, text = letters[count] )
        btn.draw(window, (0,0,0))
        buttons_list.append(btn)
        count += 1 

def checkIfLost():
    if number_of_tries == 6:
        window.blit(images[number_of_tries], (width/10-15, height/8))
        screen.update()
        sleep(.2)
        messagebox.showinfo('message',f"Your lives ended. The secret word was {secret_word}.Click ok to start a new game.")
        startNewGame()

def checkForButtonPress():
    
    global number_of_tries, letters, found_letter, running
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            for item in buttons_list: #check if mouse is over any of the button objects
                if item.isOver(pg.mouse.get_pos()) and item.text != ' ':
                    for n in range(len(secret_word)):#method to  check if the pressed letter can be found in the word
                        if item.text == secret_word[n]:
                            letters_list[n] = item.text #change the line _ on letters list with the letter pressed, so when it is iterated to drow next, it will draw that letter
                            found_letter = True
                    letters = letters.replace(item.text, ' ')
                    if not found_letter:
                        number_of_tries += 1   
                        break
        
        checkIfLost()

def checkIfFoundWord():
    if cls.toString(str(letters_list)) == secret_word:        
        startNewGame()
        sleep(.2)
        messagebox.showinfo('message',"Congrats.You found the word.Click ok to start a new game.")

def drawLinesOrLetters():
    global count
    count = 0
    for i in range(len(secret_word)):
        
        line = Button((255, 255, 255),width/2.5 + int(width/18)*i, height/8,25,25, text = letters_list[i] )
        line.draw(window)
        count += 1
    screen.update()
#method by me to generate a random word
#set the screen up
fps = 60
clock = pg.time.Clock()
pg.init()
screen = pg.display
title = screen.set_caption('Hangman Game')
window = screen.set_mode((800, 650), pg.RESIZABLE)
window.fill((255,255,255))
screen.flip()
buttons_list = [] #to get the buttons drawn in every frame
prev_secret_words = []

#tutorial on how the game is played

win = Tk()
win.wm_withdraw() #to hide the main window
messagebox.showinfo('Tutorial','Welcome to the Hangman Game.You need to pick letters until you guess the right word. For one wrong letter, you lose one try. You have 7 tries in total.')

images = []
for i in range(7): #create the list of hangman images
    image = pg.image.load(f'images{get_OS()}hangman{i}.png')
    images.append(image)

#set the game up

running = True
startNewGame()
while running:#mainloop
    found_letter = False
    clock.tick(fps)
    window.fill((255,255,255))
    width, height = screen.get_surface().get_size()
    window.blit(images[number_of_tries], (width/10-15, height/8))
   
    drawButtons()
    checkForButtonPress()
    drawLinesOrLetters()
    checkIfFoundWord()
    
    screen.update()
    buttons_list = [] #clean the buttons list so that it can be refilled in the next iteration
    
