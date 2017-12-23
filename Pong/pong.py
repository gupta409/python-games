# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
ball_radius = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
direction=random.randrange(0,2)
ball_pos=[0,0]
ball_vel=[0,0]
paddle1_pos=[HALF_PAD_WIDTH,HEIGHT/2]
paddle2_pos=[WIDTH-(HALF_PAD_WIDTH),HEIGHT/2]
paddle1_vel=0
paddle2_vel=0
edgp1=[paddle1_pos[1]-HALF_PAD_HEIGHT,paddle1_pos[1]+HALF_PAD_HEIGHT]
edgp2=[paddle2_pos[1]-HALF_PAD_HEIGHT,paddle2_pos[1]+HALF_PAD_HEIGHT]#[top most point, lower most point]
score_r=0
score_l=0

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left

def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[0,0]
    ball_vel=[0,0]
    paddle1_pos=[HALF_PAD_WIDTH,HEIGHT/2]
    paddle2_pos=[WIDTH-(HALF_PAD_WIDTH),HEIGHT/2]
    paddle1_vel=0
    paddle2_vel=0
    ball_pos=[WIDTH/2,HEIGHT/2]
    ball_vel=[random.randrange(60,180),random.randrange(120, 240)]
    ball_vel[0]=ball_vel[0]/90
    ball_vel[1]=ball_vel[1]/90
    
    
    if right==False:
        ball_vel[0]=-ball_vel[0]
        ball_vel[1]=-ball_vel[1]
    else:
        ball_vel[0]=ball_vel[0]
        ball_vel[1]=-ball_vel[1]
    
    pass

# define event handlers

def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score_r, score_l  # these are ints
    score_r=0
    score_l=0
    ball_init(direction)
    pass

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel,edgp1,edgp2,paddle1_vel,paddle2_vel,direction,score_r,score_l
    # update paddle's vertical position, keep paddle on the screen
    
    if edgp1[1]>=HEIGHT and paddle1_vel>0:
        paddle1_vel=0
    if edgp1[0]<=0 and paddle1_vel<0:
        paddle1_vel=0         
    if edgp2[1]>=HEIGHT and paddle2_vel>0:
        paddle2_vel=0
    if edgp2[0]<=0 and paddle2_vel<0:
        paddle2_vel=0     
    paddle1_pos[1]+=paddle1_vel
    paddle2_pos[1]+=paddle2_vel
    
       

    edgp1=[paddle1_pos[1]-HALF_PAD_HEIGHT,paddle1_pos[1]+HALF_PAD_HEIGHT]
    edgp2=[paddle2_pos[1]-HALF_PAD_HEIGHT,paddle2_pos[1]+HALF_PAD_HEIGHT]

        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_polygon([(paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT),(paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT),(paddle1_pos[0]-HALF_PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT),(paddle1_pos[0]-HALF_PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT)], 8, "lime")
    c.draw_polygon([(paddle2_pos[0]+HALF_PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT),(paddle2_pos[0]+HALF_PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT),(paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT),(paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT)], 8, "lime")
    # update ball
    ball_pos[0]+=ball_vel[0] 
    ball_pos[1]+=ball_vel[1] 
    #collision and reflections made by the ball and scores
    if ball_pos[1] <=ball_radius:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >=HEIGHT-ball_radius:
        ball_vel[1] = - ball_vel[1]    
    if (edgp1[0]<ball_pos[1]<edgp1[1]) and (ball_pos[0]<=(ball_radius+PAD_WIDTH)):
        ball_vel[0] = -ball_vel[0]  
        ball_vel[0]=ball_vel[0]+(0.1*ball_vel[0])
        ball_vel[1]=ball_vel[1]+(0.1*ball_vel[1])
    elif (ball_pos[0]<(ball_radius+PAD_WIDTH)):
        direction=1
        ball_init(direction)
        score_r+=1
        
    if (edgp2[0]<ball_pos[1]<edgp2[1]) and (ball_pos[0]>=WIDTH-(ball_radius+PAD_WIDTH)):
        ball_vel[0] = -ball_vel[0] 
        ball_vel[0]=ball_vel[0]+(0.1*ball_vel[0])
        ball_vel[1]=ball_vel[1]+(0.1*ball_vel[1])
    elif (ball_pos[0]>WIDTH-(ball_radius+PAD_WIDTH)):
        direction=0
        ball_init(direction)     
        score_l+=1
        
        

    # draw ball 
    c.draw_circle(ball_pos,ball_radius,1,'red','aqua')   

    c.draw_text(str(score_l),(WIDTH/6+15,HEIGHT/3),45,"lime")
    c.draw_text(str(score_r),((WIDTH*4/6)+25,HEIGHT/3),45,"lime")


def keydown(key):
    global paddle1_vel, paddle2_vel
    acc=1.5
    if key==simplegui.KEY_MAP["s"]:
            paddle1_vel+= acc

    elif key==simplegui.KEY_MAP["w"]:
            paddle1_vel-= acc

                
             
    if key==simplegui.KEY_MAP["down"]:
            paddle2_vel+= acc

    elif key==simplegui.KEY_MAP["up"]:
            paddle2_vel-= acc
               
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel=0
    paddle2_vel=0

# create frame

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)

# start frame

init()
frame.start()
