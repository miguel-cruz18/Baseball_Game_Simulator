# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 2019
Created functions to use in the Baseball Game Simulator Project
@author: Miguel Cruz Robles
"""

#==============================================================================
#These script serves as a module for the main page. Contains various functions 
#created to calculate different things important for the game simulation.
#==============================================================================

from random import random
from random import randint

#Function that receives an array, specifically 
#the player stats one and establish means each value
def Player_stats(player):
    TPA = player[0]#Total Plate Appearances
    AB = player[1]#At bat
    Hits = player[2]#When player hit
    Single = player[3]#Player hit reachin first base
    Double = player[4]#Palyer hit reaching second base
    HR = player[5]#Player hit reaching Home
    AVG = player[6]#Player batting percentage, out/hits
    OBP = player[7]#Batting percentage when someone is on base
    return TPA, AB, Hits, Single, Double, HR, AVG, OBP

#One of the most important functions. Performs what will
#be the half of an inning. Receiveing team stats, batter up
#and opposing team error%, will run all the probabilities 
#and return a list of hits batted. This list then is 
#transform into runs in another function
def Half_inning(team, batter_up, opponent_error_pct):
    out = 0
    base = "empty"
    batted = []
    while out < 3:
        #Getting batter up
        player_batting = team[batter_up,:]
        
        #Getting batter stats
        TPA, AB, Hits, Single, Double, HR, AVG, OBP = Player_stats(player_batting)
        
        #Indicating the next batter
        batter_up += 1
        #Since there are 9 players, after the 9 
        #we go back to the first one.
        if batter_up == 9:
            batter_up = 0
            
        #Determine if is an At Bat or not
        prob = random()
        if prob <= (TPA-AB)/TPA:
            batted.append(1)#palyer reaching first base
            base = "occupied"#base is now occupied
        else:
            #iIf base is empty player batiing average will be AVG
            #else is occupied, OBP will be use making it
            #more probable of hitting the ball.
            if base == "empty":
                batting_average = AVG
            else:
                batting_average = OBP
            
            #Now we throw the probability of being out.
            prob = random()
            if prob <= 1 - batting_average:
                error_prob = random()
                #When out happen there might be an error
                #so we also run this prob.
                if error_prob <= opponent_error_pct:
                    batted.append(1)
                    base = "occupied"
                else:
                    out += 1#we update out to one more
            else:
                #Here the player has battet and now we determine
                #if it was a single, double, triple or HR.
                prob = randint(1, Hits)
                if prob <= Single:
                    batted.append(1)
                    base = "occupied"
                elif prob <= Single + Double:
                    batted.append(2)#reaching second base
                    base = "occupied"
                elif prob <= Single + Double + HR:
                    batted.append(4)#reachinig home with HOME RUN!
                    base = "empty"
                else:
                    batted.append(3)
                    base = "occupied"#reaching thrid base
    #Calculated runs batted in with another function that
    #will be further explained.
    runs = Runs_calc(batted)
    return runs, batter_up

#Function that receives a list containing
#the hits batted in the inning, in order to
#transform them into how many runs were batted in.
def Runs_calc(list):
    if sum(list) < 4:
        return 0#No one reached home, no runs scored.
    #The idea is to form a adding list but in descending form.
    resta = 0
    added_hits = []
    for i in list:
        added_hits.append(sum(list) - resta)
        resta = resta + i
    runs = 0
    #For every number bigger or equal than form means
    #someone reached home and scored a run.
    for j in added_hits:
        if j >= 4:
            runs = runs + 1
    return runs

#This function gives me the ascending form for 
#the runs by inning for both teams.
def Runs_adder(v_runs_list, h_runs_list):
    suma_v = 0
    suma_h = 0
    v_new_list = []
    h_new_list = []
    for k in range(len(v_runs_list)):
        suma_v = v_runs_list[k] + suma_v
        v_new_list.append(suma_v)
        suma_h = h_runs_list[k] + suma_h
        h_new_list.append(suma_h)
    return v_new_list, h_new_list
