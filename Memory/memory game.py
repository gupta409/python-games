# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
#tracker keeps track of the card that are of the same type and opened 
#mover keeps tracks of the cards moved yet
def init():
    global nums,exposed,state,tracker,mover,moves
    moves=0
    mover=[]
    tracker=[]
    state=0
    nums=range(0,8)
    nums.extend(range(0,8))
    random.shuffle(nums)
    exposed=[]
    for i in range(0,16):
        exposed.append(False)
    pass  
#to make the exposed function completely false
def all_false():
    global exposed,tracker
    
    for i in range(0,16):
        exposed[i]=False
        for j in tracker:
            if j==i:
                exposed[i]=True
                
                
    
    pass    
     
# define event handlers
def mouseclick(pos):
    global exposed,state,nums,moves
    print state
    index=location(pos)
    if exposed[index]==False:
        mover.append(index)

        moves=len(mover)
        ext="Moves="+str(moves)
        l.set_text(ext)
        if state==2:
            
            all_false()
        if state>0:
            if nums[mover[len(mover)-1]]==nums[mover[len(mover)-2]]:
                print nums[mover[len(mover)-1]],nums[mover[len(mover)-2]]
                tracker.append(mover[len(mover)-2])
                tracker.append(mover[len(mover)-1])
           
        if state<=2:
            
            exposed[index]=True 
            state_change()
            
        

        
    pass
#changes the global state...to keep track of the number of cards open
def state_change():
    global state
    if state == 0:
        state = 1
    elif state == 1:
        state = 2
    else:
        state =1   
    pass    
#returns the block(or the card) in which the given position is in
def location(pos):
    x=pos[0]
    for i in range(0,16):
        lower=0+(50*i)
        upper=50+(50*i)
        if x>=lower and x<=upper:
            block=i
            break
    return block        
# define function to draw box(to simplify the code)  
# cards are logically 50x100 pixels in size    
def draw_box(pos,canvas):
        
    canvas.draw_polygon(((pos[0]-25,pos[1]-50),(pos[0]+25,pos[1]-50),(pos[0]+25,pos[1]+50),(pos[0]-25,pos[1]+50)),1,"RED", "lime")
#to draw the text of the numbers by taking in the index number,canvas as inputs
def draw_text(card_number,canvas):
    global nums
    card_value=nums[card_number]
    canvas.draw_text(str(card_value),[15+(card_number*50),70],45, "black")
def draw(canvas):
    for i in range(0,16):
        if i>0:
            draw_box([25+(i*50),50],canvas)
        else:
            draw_box([25,50],canvas)
    for i in range(0,16):  
        if exposed[i]==True:
            draw_text(i,canvas)
            


    pass


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
l=frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric