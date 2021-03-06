# Weekly progress journal

## Instructions

In this journal you will document your progress of the project, making use of weekly milestones. In contrast to project 1, you will need to define yourself detailed milestones.

Every week you should

1. define **on Wednesday** detailed milestones for the week (according to the
   high-level milestones listed in the review issue).
   Then make a short plan of how you want to
   reach these milestones. Think about how to distribute work in the group,
   what pieces of code functionality need to be implemented.
2. write about your progress **before** the Tuesday in the next week with
   respect to the milestones. Substantiate your progress with links to code,
   pictures or test results. Reflect on the relation to your original plan.

Note that there is a break before the deadline of the first week review
issue. Hence the definition of milestones and the plan for week 1 should be
done on or before 15 April.

We will give feedback on your progress on Tuesday before the following lecture. Consult the
[grading scheme](https://computationalphysics.quantumtinkerer.tudelft.nl/proj2-grading/)
for details how the journal enters your grade.

Note that the file format of the journal is *markdown*. This is a flexible and easy method of
converting text to HTML.
Documentation of the syntax of markdown can be found
[here](https://docs.gitlab.com/ee/user/markdown.html#gfm-extends-standard-markdown).
You will find how to include [links](https://docs.gitlab.com/ee/user/markdown.html#links) and
[images](https://docs.gitlab.com/ee/user/markdown.html#images) particularly
useful.

## Week 1
(due before 21 April)

Friday 24 April (Group)
All of us had been very busy studying for exams and preparing final submissions for other courses. This is why we were not able to begin the project on time. Ludwig started with implementing the Rosenbluth algorithm. From here we need to come together and make a plan how to distribute the work for the next few weeks after which we will add milestones.


End of week report:

The Rosenbluth algorithm was implemented according to Jos' book and a report by [Mandana Tabrizi](https://yorkspace.library.yorku.ca/xmlui/bitstream/handle/10315/30743/Tabrizi_Mandana_2015_Masters.pdf?sequence=2&isAllowed=y). Two beads are initialized at positon (0,0) and (1,0). From the second bead positions of new beads are generated randomly on a circle with radius one. The variable res  gives the number of positions on the circle with equal distance of 2pi/res. Positions are stored in a vector called pos.


```
#get random positions in circular resolution of 2*pi/res
res = 6 # resolution in which angles are taken 2*pi/res
init_angle = random.uniform(0, 1)*2*pi
angles = np.zeros(res)
pos = np.zeros(shape=(res,2))
for i in range(res):
    angles[i] = (init_angle + i*(2*pi/res))%(2*pi)
    pos[i,0] = beads[1+run,0] + cos(angles[i])
    pos[i,1] = beads[1+run,1] + sin(angles[i])
```

This piece of code visualized results in six new positions that were generated randomly:

![alt text](img/week1/possible_pos.png "Generated follow up positions")

For each new coordinate the distance to the closest existing bead saved in a vector called beads is determined. This distance is used to calculate the energy (E_i) and hence the weight (w_i) of that particular position by calling the function get_weight:

```
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
```

The weights added to a vector w_i_arr and are normalized by the total weight W. This yields a vecor holding the probability of each position dependent on the energy of that position:

```
    #calculation total weight W and scaling the weights of each position with
    # W into vector pos_prob holding the probability of all positions
    w_i_arr = np.zeros(res)
    for i in range(res):
        w_i = get_weight(pos,beads,k,T,i,run)
        w_i_arr[i] = w_i
    W = np.sum(w_i_arr)
    pos_prob = w_i_arr/W
```

Some positions might be too close to an existing bead leading to a zero probability of that position due to the repulsive term in the Lennard-Jones potential. The new position is determined by the function play_roulette which asigns each probability a corresponding range in the interval [0:1]. A randomly generated number is compared to those intervals and the one which it lies in wins and serves as a new positon which is added to the vetor beads:

```
def play_roulette(pos_prob):
    roulette_list = list()
    roulette_counter = list()

    for count, r in enumerate(pos_prob):
        if r*1 == 0 or r*1 < 1e-20:
            continue
        elif r*1 > 0:# and count == 0:
            roulette_list.append(r*1)
            roulette_counter.append(count)

    for i in range(1,len(roulette_list)):
        roulette_list[i] += roulette_list[i-1]

    roulette = random.uniform(0, 1)
    idx = find_nearest(roulette_list,roulette)
    new_pos = roulette_counter[idx]
    return new_pos
```

The new bead was generated at position 2.

![alt text](img/week1/new_bead.png "New bead")

The described procedure is executed in a loop running over N new beads to add. Here is a plot presenting the self avoiding random walk (SAW) of N=50 beads:

![alt text](img/week1/50_beads.png "50 beads")


## Week 2
(due before 28 April)

Monday 4 May (Group)
Isacco vectorized the Rosenbluth algorithm and started to implement the perm algorithm. Ludwig worked on the data acquisition, results and display of Rosenbluth simulations. The vectorization led to a very significant speed up of the simulations. Here we present the squared end-to-end distance of 10000 simulations using a res = 50 and 250 beads for the the self avoiding walk. The average end-to-end distance over all simulations displayed in the plot is not taken with respect to the weights. We do calculate the weights as described in Jos' book but they become extremely large and lead to unjustifyable data. This is a matter we want to discuss with the TA's. However, the mean of the end-to-end distance and the corresponding standard deviation leads to an exponent of: 0.56 The data is presented as figure 10.3 in Jos' book.

![alt text](img/week2/end-to-end-distance.png "Beads")

The same simulation was performed without the Lennard-Jones potential which led to an exponent of: 0.5

While implementing the perm algorithm we got stuck due to conceptual understanding. We have a bunch of questions prepared for TA's.

## Week 3
(due before 5 May)

Monday 11 May (Group)
We have been trying to implement feedback received last week. In fact, our polymers do evetually cross themselves during the self avoiding random walk. This however only occurs for long polymer chain, hence a high number of beads as it was simulated and reported in week 2. To verfiy our SAW we started to simulate 10000 polymers in the range of 20 beads. The result is depicted in the following figure:

![alt text](img/week3/rosenbluth_075.png "few_Beads")

The simulation led to an exponent of: 0.754 as performed for 20 beads. The calculated exponents are fairly consistent up to a length of 25 beads per polymer. To calculate the exponents from the end-to-end distance we did not use the proposed weighted average since the calculation of the total weights W is still not entirely clear to us. This is also the reasin why the error appears to decrease with increased polymer length. This is only an artifact arising from the logarithmic scaling. The error is calculated as the standard deviation of the averaged end-to-end distances using the 10000 simulations. When trying to apply the weighted average we end up with weights W exploding to enormously high numbers. We were trying to debug the code and boiled the problem down to the following crucial points:

The following figure shows the two initial beads and a "chosen" subsequent bead along with all other possible bead positions. Here 6, since we set the resolution to res=6. The number of each position j represents its index j for the lists "Position energy" and "Bead weight w_j"

![alt text](img/week3/weights_question.png "weights_question")

Each position j gets an energy Ej assigned as a reuslt of interaction with all already existing beads. Then the positions weights are calculated by wj = exp(-Ej) where epsilon/kbT = 1. Sigma was set to 0.6 which leads to the negative position energies Ej of j=0,1,2,3,4. Only position j=5 is placed relatively close to already existing beads yielding a positive energy and hence a very low weight, in fact a weight of 0. The weights of the other positions are fairly equal except for j=0, since here attractive Lennard-Jones interaction decreases the energy, thus increases the weight. The total weight of the subsequent bead "Polymer weight W" sums up to approximately 7. For a polymer of length N we would hence expect a total weight of W=7^N. Here we wonder where we are wrong in calculating the weights. Even a random walk (epsilon=0) yields a weight of W=6 since all individual weights are wj=1. The exploding values of the weights are our main problem with the Rosenbluth algorithm.

Since the code produces the correct exponents for random walks of arbitrary polymer length as well as for SAW using short polymers, we are confident about the general implementation. Isacco managed to implement the algorithm recursively which is a corner stone for our implementation of the perm algorithm.
```
def addBead(polymer, polWeight, L):
  '''
  Recursive Rosenbluth algorithm to generate polymer in real space
  Needs eps, sigma, res, T, N global variables
  In: polymer (nparray 2 x 2): input two bead polymer
      polWeight (float): initial polymer weight (polWeight = 1)
      L (int): next bead number (L = 3)
  Out: polymer (nparray N x 2): final polymer of size N
       polWeight (float): final polymer weight
  '''
  pos, wj, W = get_weight(polymer)
  newBead = play_roulette(pos, wj, W)
  polymer = np.vstack((polymer, newBead)) #bead added
  polWeight *= W
  if L < N:
      polymer, polWeight = addBead(polymer, polWeight, L+1)
  return polymer, polWeight
```
