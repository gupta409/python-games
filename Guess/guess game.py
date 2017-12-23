# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import math
import random

# initialize global variables used in your code
num=0
n=0
count=0
# define event handlers for control panel
    
def range100():
    print
    print'you are now running the 0-100 range game'
    global num,n,count
    
    n=8
    count=n
    num=random.randrange(0,100)
    print'number of chances left',n
    # button that changes range to range [0,100) and restarts

def range1000():
    print
    print'you are now running the 0-1000 range game'
    global num,n,count
    n=10
    count=n
    # button that changes range to range [0,1000) and restarts
    num=random.randrange(0,1000)
    print'number of chances left',n
def get_input(guess):
    guess=int(guess)
    print'Guess was',guess
    global num,count,n
    count=count-1
    print'number of chances left',count
    if count>0:
    
     if guess==num:
         print 'correct'
           
     elif guess>num:
         print'lower'
     else:    
         print'higher'
   
    else:
        print'Sorry you have exhusted you chances....you lose'
    # main game logic goes here	

    
# create frame
f =simplegui.create_frame("GUESS GAME",200,200)
r1=f.add_button("range 0-100",range100,200)
r2=f.add_button("range 0-1000",range1000,200)
guess=f.add_input("Enter guess",get_input,200)

# register event handlers for control elements


# start frame
f.start()

# always remember to check your completed program against the grading rubric