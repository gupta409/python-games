# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0
constant_angvel=0.05
constant_vel=1
friction=0.5
missile_constant=6
started = False
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    

    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)
#helper function to take care of collisions
def group_collide(group,other_object):
    global g_group
    count=0
    for obj in list(group):
        if obj.collide(other_object):
            group.remove(obj)
            count+=1
    g_group=group
    return count        
# helper function that draws each object one by one
def process_sprite_group(group,canvas):
    
    for obj in list(group):
        
        if obj.update():
            obj.draw(canvas)    
        else:
            group.remove(obj)
# helper function keeping track of collisions between two groups
def group_group_collide(group1,group2):
    global g_group
    g_group=group1
    count=0
    for obj1 in group2:
        count+=group_collide(group1,obj1)
    group1=g_group
    return count    
# helper function terminates the game and makes it ready for restart
def game_over():
    global lives,count,missile_group,rock_group,my_ship,started
    started=False
    lives=3
    count=0
    my_ship = Ship([width / 2, height / 2], [0,0], 0, ship_image, ship_info)
    rock_group =set([])
    missile_group =set([]) 

    
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0],self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def thrust_switch(self,val):
        if val:
            self.thrust=True
            ship_thrust_sound.play()
        else:
            self.thrust=False
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
    
    def update(self):
        self.angle += self.angle_vel
        acc = angle_to_vector(self.angle)
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99
        
        if (self.pos[0]-(0.5*self.image_size[0]))<=0:
            self.pos[0]=width-self.image_size[0]
        if (self.pos[0]+(0.5*self.image_size[0]))>=width:
            self.pos[0]=self.image_size[0]    
        if (self.pos[1]-(0.5*self.image_size[1]))<=0:
            self.pos[1]=height-self.image_size[1]
        if (self.pos[1]+(0.5*self.image_size[1]))>=height:
            self.pos[1]=self.image_size[1]        
        pass
    
    def shoot(self):
        
        forward=angle_to_vector(self.angle)
        missile_pos=[(self.pos[0]+(self.radius*forward[0])),self.pos[1]+(self.radius*forward[1])]       
        missile_vel=[self.vel[0]+(missile_constant*forward[0]),self.vel[1]+(missile_constant*forward[1])]
        missile_group.add(Sprite(missile_pos, missile_vel,0, 0, missile_image, missile_info, missile_sound))
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # keeps the body form going round the canvas
        if (self.pos[0]-(0.5*self.image_size[0]))<=0:
            self.pos[0]=width-self.image_size[0]
        if (self.pos[0]+(0.5*self.image_size[0]))>=width:
            self.pos[0]=self.image_size[0]    
        if (self.pos[1]-(0.5*self.image_size[1]))<=0:
            self.pos[1]=height-self.image_size[1]
        if (self.pos[1]+(0.5*self.image_size[1]))>=height:
            self.pos[1]=self.image_size[1]        
        # keeping track of the lifetime and age of the object
        self.age+=1
        if self.age>=self.lifespan:
            return False
        else:
            return True
        pass        
    def collide(self,other_object):
        if dist(self.pos,other_object.pos)>self.radius+other_object.radius:
            return False
        else:
            return True 

# draw handler           
def draw(canvas):
    global time,started,rock_group,lives,missile_group,score
    
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])
    canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [2*wtime, size[1]], 
                                [1.25*wtime, height/2], [2.5*wtime, height])
    canvas.draw_text("LIVES",[width*0.08,height*0.05],30,"Red")
    canvas.draw_text(str(lives),[width*0.1,height*0.1],30,"Red")
    canvas.draw_text("SCORE",[width-width*0.15,height*0.05],30,"Red")
    canvas.draw_text(str(score),[width-width*0.1,height*0.1],30,"Red")
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    
    # makes the multiple rocks
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group,canvas)
    # drawing collisions
    score+=group_group_collide(rock_group,missile_group)
    lives-=group_collide(rock_group,my_ship)
    if lives==0:
        game_over()
    # update ship and sprites
    my_ship.update()
    
    
    
    # draw splash screen if not started *draws the initial screen you see *
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [width/2, height/2], 
                          splash_info.get_size())        

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
     
    rock_pos = [random.randrange(0, width), random.randrange(0, height)]
    while dist(rock_pos,my_ship.pos)<(my_ship.radius+asteroid_info.get_radius())+8:
        rock_pos = [random.randrange(0, width), random.randrange(0, height)]
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_avel = random.random() * .2 - .1
    if len(list(rock_group))<13:
        rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))
    pass
# key handlers 
def keydown(key):
    
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust_switch(True)
        forward_vector=angle_to_vector(my_ship.angle)
        my_ship.vel[0]+=constant_vel*forward_vector[0]
        my_ship.vel[1]+=constant_vel*forward_vector[1]
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel+=constant_angvel
    elif key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel-=constant_angvel
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        missile_sound.play()
def keyup(key):
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust_switch(False)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel=0
    elif key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel=0    
    elif key == simplegui.KEY_MAP['space']:
        missile_sound.pause()
        missile_sound.rewind()
# initialize frame
frame = simplegui.create_frame("Asteroids", width, height)
# click handlers for the starting
def click(pos):
    global started
    center = [width / 2, height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
# initialize ship and two sprites
my_ship = Ship([width / 2, height / 2], [0,0], 0, ship_image, ship_info)
rock_group =set([])
missile_group =set([]) 

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)
frame.set_mouseclick_handler(click)

# get things rolling
timer.start()
frame.start()