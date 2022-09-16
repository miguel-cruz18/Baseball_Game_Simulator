# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 2019
Baseball Game Simulator
@author: Miguel Cruz Robles
"""

#=====================================================================
#Main page for Baseball Game Simulator based on players roster batting 
#stats and opposing team fielding error probability.
#=====================================================================

import Baseball
import numpy as np
#import matplotlib.pyplot as plt

#First we gather the data from our CSV file. 
#Each file contains an array with the stats of 
#all player in the team batting order

filename_v = 'Houston_Astros.csv'
visitor_team = np.genfromtxt(filename_v, delimiter = ',', skip_header = 1)
v_error_prob = visitor_team[0,8]

filename_h = 'Boston_Red_Sox.csv'
home_team = np.genfromtxt(filename_h, delimiter = ',', skip_header = 1)
h_error_prob = home_team[0,8]


#Now we establish some baseball standards as variables 
#as every game, starts at the frist inning and 
#both team with 0 runs.
#Batter_up will be used to indicate which player
#is going to bat.

inning = 1
v_runs = 0
h_runs = 0
v_batter_up = 0
h_batter_up = 0


#This empty lists will save the runs batted in by inning 
#for both team so later on we ca plot the game results.
visitor_runs_by_inning = []
home_runs_by_inning = []


#After we have all the stats and standards, this while loop
#keeps the game happening while the game isn't in the 9 inning
#or both team runs are equal as will a real game do.

while inning <= 9 or v_runs == h_runs:
    
    #In the loop, given the stats, the information goes 
    #into the Half_inning function and returns the runs
    #batted in by the team.

    v_runs_in, v_batter_up = Baseball.Half_inning(visitor_team, v_batter_up, h_error_prob)
    visitor_runs_by_inning.append(v_runs_in)
    v_runs = sum(visitor_runs_by_inning)#update visitor runs
    
    #This statement is  based on a baseball rule that when you
    #reach the 9 inning and after visiting has batted and home team
    #is still up winning, there is no need for home to bat again
    #because after the 9 the game ends and they will still be winning 
    #batted or not.

    if inning == 9 and h_runs > v_runs:
        break
    
    #Here ocurrs exactly the same as befor in the loop but for 
    #the home team. A inning is not completed until both teams 
    #have batted, later on inning will be updated.

    h_runs_in, h_batter_up = Baseball.Half_inning(home_team, h_batter_up, v_error_prob)
    home_runs_by_inning.append(h_runs_in)
    h_runs = sum(home_runs_by_inning)#update home score
    
    #This statement helps me fix some sort of error encountered
    #when 9 innings where played but inning will still update to 
    #10 inning, giving me a false number of innings played.

    if inning >= 9 and v_runs != h_runs:
        break
    
    inning += 1 #inning increasing by 1 after each team has batted


#Based on both teams runs after the game ends, 
#the one with more runs wins the game.

if v_runs > h_runs:
    winner = 'Visitor'
else:
    winner = 'Home'

#Here we create a inning array for total innings
#played to later plot the results.

innings_played = np.arange(1, inning + 1) 

#If statement to solve a minor error that wouldn't let me 
#plot beacuse home team played one less inning and by 
#adding a 0 at the end of the list this is fix.
if len(home_runs_by_inning) != len(innings_played):
    home_runs_by_inning.append(0)

#This function converts the runs by inning into a more fluent 
#one to use in graph where runs will be added in ascending
#form while innings ascend.
v_accumulated_runs, h_accumulated_runs = Baseball.Runs_adder(visitor_runs_by_inning, home_runs_by_inning)

'''
#Code that will plot the results, nice and simple.
plt.plot(innings_played, v_accumulated_runs)
plt.plot(innings_played, h_accumulated_runs)
plt.xlabel('Innings')
plt.ylabel('Runs')
'''

#lastly for the main page script, a code that gives you the reulst
#of the game in a text file. You'll see the winner and respectives
#runs for each team.
output_file = open('Game_results.txt', 'w')
output_file.write(f'''{winner} Team wins the game! In {inning} innings played
Vistors team runs per inning were {visitor_runs_by_inning} 
for a total of {v_runs},
while Home team runs per inning were {home_runs_by_inning} 
for a total of {h_runs}.''')
output_file.close()

print(f'''\n{winner} Team wins the game! In {inning} innings played
Vistors team runs per inning were {visitor_runs_by_inning} 
for a total of {v_runs},
while Home team runs per inning were {home_runs_by_inning} 
for a total of {h_runs}.''')






