# template for "Stopwatch: The Game"

#import files
import simplegui
import random
# define global variables
x=0 #global vaiable keeping track of the timer
a=0
b=0
c=0
d=0
data='' #varable for final form of time
A=''	#A,B,C,D to store a,b,c,d as strings 
B=''
C=''
D=''
win=0	#win keeps track of the number of times user wins
net=0	#net keeps track of the total number of the times user tried
test=0 	#keeps track if user has pressed stop button multiple times or not
# define helper function format that converts integer
# counting tenths of seconds into formatted string A:BC.D
def format(x):
    global a,b,c,d,A,B,C,D
    a=int(x/600)
    temp=x-(a*600)
    d=temp%10
    c=int(((temp%100)-d)/10)
    b=int(((temp%1000)-(c*10)-(d))/100)
    if(c<0):
        c=0
    if(b<0):
        b=0
    if(a<0):
        a=0
    
  
    A=str(a)
    B=str(b)
    C=str(c)
    D=str(d)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_def():
    timer.start()   
    global test
    test=1
def stop_def():
    global net,win,test
    timer.stop()  
    if(test==1):
        net=net+1
        test=0
        if(((x-(a*600))%10)==0):
            win=win+1
    
def reset_def():    
    global x,win,net
    x=0
    win=0
    net=0
    timer.stop()
# define event handler for timer with 0.1 sec interval(timer handler)
def time_handle():
    global x
    x=x+1

# draw handler
def draw(STOPWATCH):
    
    
    STOPWATCH.draw_text(A+':'+B+C+'.'+D,[100,100],24,"RED")
    format(x);
    STOPWATCH.draw_text(str(win)+'/'+str(net),[250,20],15,"yellow")
# create frame
frame =simplegui.create_frame("STOPWATCH",300,200)

# register event handlers
frame.set_draw_handler(draw)
timer=simplegui.create_timer(100,time_handle)
start=frame.add_button("START",start_def)
reset=frame.add_button("STOP",stop_def)
reset=frame.add_button("RESET",reset_def)

# start timer and frame
frame.start()

#print data

# remember to review the grading rubric