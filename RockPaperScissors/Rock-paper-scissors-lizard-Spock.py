# Rock-paper-scissors-lizard-Spock template

import random
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def number_to_name(number):
    # fill in your code below
    if number==0:
     name='rock'
    elif number==1:
     name='Spock'
    elif number==2:
        name='paper'
    elif number==3:
        name='lizard'
    else:
        name='scissors'
    return name
    # convert number to a name using if/elif/else
    # don't forget to return the result!

    
def name_to_number(name):
    # fill in your code below
    if name=='rock':
     number=0
    elif name=='Spock':
     number=1
    elif name=='paper':
       number=2 
    elif name=='lizard':
        number=3
    else:
        number=4
    return number
    # convert name to number using if/elif/else
    # don't forget to return the result!


def rpsls(name): 
    # fill in your code below
    player_number=name_to_number(name)
    
    # convert name to player_number using name_to_number

    # compute random guess for comp_number using random.randrange()
    comp_number=random.randrange(0,5)
    # compute difference of player_number and comp_number modulo five
    diff=(player_number-comp_number)
    
    print
    print"Player chooses "+number_to_name(player_number)
    print"Computer chooses "+number_to_name(comp_number)
    # use if/elif/else to determine winner
    val=diff
    if player_number==comp_number:
        print"DRAW!"
    elif val==1 or val==2:
        print"Player wins!"
    else:
        print"Computer wins!" 
    # convert comp_number to name using number_to_name
    
    
    # print results

    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric

