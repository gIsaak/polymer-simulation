import numpy as np
import random
from math import pi, sin, cos
import matplotlib.pyplot as plt


def find_nearest(array, value):
    array = np.asarray(array)
    idx = None
    for i in range(len(array)):
        if value < array[i]:
            idx = i
            break
    return idx

# distances to nearest neighbors
# number of possible positions is res
# need to calculate the distance to the nearest neighbor of each position to plus into lennard jones
def get_weight(pos,beads,k,T,i,run):    
    #distance to all existant beads for new pos i
    dist_list = list()
    for j in range(len(beads[:2+run,1])):
        bead_dist = abs(np.sqrt((beads[j,0]-pos[i,0])**2 + (beads[j,1]-pos[i,1])**2))
        dist_list.append(bead_dist)
        
    # gives index of bead with minimal distance to position i
    min_position = dist_list.index(min(dist_list))
    min_distance = dist_list[min_position]
#    print(min_distance)
# with those calculate the energy they have and therefore weight w_i
    E_i = (0.8/min_distance)**12 - (0.8/min_distance)**6
    #    print('\nE_i ={}\n'.format(E_i))
    w_i = np.exp(-E_i/(k*T))
        
    print('Position: {}\nMin Dist to existing bead: {}\nCorresponding E(r):{}\nCorresponding w_i:{}\n'.format(i,min_distance,E_i,w_i))
    return w_i

def play_roulette(pos_prob):
    # play roulette with gives weight distribution
    roulette_list = list()
    roulette_counter = list()
    
    for count, r in enumerate(pos_prob):
        if r*1 == 0 or r*1 < 1e-20:
            continue
        elif r*1 > 0:# and count == 0:
            roulette_list.append(r*1)
            roulette_counter.append(count)

#    print('raw prob\n',pos_prob)       
#    print('before shit happens\n',roulette_list,'\n')
    for i in range(1,len(roulette_list)):
        roulette_list[i] += roulette_list[i-1] 
        
    roulette = random.uniform(0, 1)
    idx = find_nearest(roulette_list,roulette)
#    print(roulette_list)
    
    new_pos = roulette_counter[idx]
#    print('\nReslt section\nRoulette number: {}\ncorr. index: {}'.format(roulette,idx))
    return new_pos

T = 300
k = 1

N = 50
beads = np.zeros(shape=(2+N,2))
beads[1,0] = 1
scatterPoints = []

# set up scatter plot for displaying beads SAW
fig = plt.figure()
ax = fig.add_subplot(111)
for run in range(N):
    #get random positions in circular resolution of 2*pi/res
    res = 6 # resolution in which angles are taken 2*pi/res
    init_angle = random.uniform(0, 1)*2*pi
    angles = np.zeros(res)
    pos = np.zeros(shape=(res,2))
    for i in range(res):
        angles[i] = (init_angle + i*(2*pi/res))%(2*pi)
        pos[i,0] = beads[1+run,0] + cos(angles[i])
        pos[i,1] = beads[1+run,1] + sin(angles[i])
 
###=======================================================================###       
### plots the initial positions for possible new bead positions for debugging ###
#        plt.scatter(pos[i,0],pos[i,1],color='g')
#        if i < len(beads[:2+run,0]):
#            plt.scatter(beads[i,0],beads[i,1],color='r')
#        plt.text(pos[i,0],pos[i,1], '{}'.format((str(i)), size=20, zorder=1, color='k'))  
###=======================================================================###

    #calculation total weight W and scaling the weights of each position with 
    # W into vector pos_prob holding the probability of all positions
    w_i_arr = np.zeros(res)
    for i in range(res):
        w_i = get_weight(pos,beads,k,T,i,run)
        w_i_arr[i] = w_i
    W = np.sum(w_i_arr)
    pos_prob = w_i_arr/W
    
    # function to get the new position according to their prob. distribution
    new_pos = play_roulette(pos_prob)
    
    # adding the new bead
    beads[2+run,0] = pos[new_pos,0]
    beads[2+run,1] = pos[new_pos,1]
    
#    # plotting the beads
#    scatterPoints.append(ax.scatter(beads[:,0],beads[:,1],color='r'))
#    plt.plot(beads[:,0],beads[:,1],color='b')
    
    plt.scatter(beads[:,0],beads[:,1],color='r')
#    plt.plot(beads[:,0],beads[:,1],color='b')

    plt.pause(0.05)

plt.plot(beads[:,0],beads[:,1],color='b')
       
