Uni: cjd2186
Author: Christopher Demirjian

Python Files: rip.py, pd_7_router_net.py

JSON files: 
'u_link_weights.json'
'v_link_weights.json'
'x_link_weights.json'
'w_link_weights.json'
'y_link_weights.json'
'z_link_weights.json'


LOGIC:
I modified the pd_7_router_net.py file
  to have the network topology that was given in figure 5.3 of the James Kurose
    eighth edition textbook.
    RIP contains two mew functions to assign linkweights and implement poison reverse,
     ableit these functions are not used, but they display my thought process.



RIP Modifications:
I created two new functions called "getLinkWeights" and "poisonReverse",
  the latter of which only consists of pseudocode.

getLinkWeights reads from the json files created that each store the 
  link weights of a the links to a node's adjacent neighbtors.
These values are stored into a dictionary, where each value is another link weights
  for the link named key.

The poisonReverse function is written in pseudocode, to communicate how 
  poisonReverse would work if it were used: 
  
  [without poison Reverse:
  (as in it would ensure that there is not a case as in 5.7 where the loop 
   will persist for 44 iterations (message exchanges between y and z)—until z 
   eventually computes the cost ofits path via y to be greater than 50)]. 
   
   With poisonReverse:
    y’s distance table will indicicate Dz(x) = ∞. 
    The cost of the (x, y) link changes from 4 to 60 at time t=0, y
     updates its table and continues to route directly to x, (to 60), 
     and will tell z of its new cost to x, that is, Dy(x) = 60. 
    After receiving the update at t=1, z will shift its route to x to be
     via the direct (z, x) with link cost50. Since this is a new least-cost 
     path to x, and since the path no longer passes through y, z now tells y 
     that Dz(x) = 50 at t=2. 
    After receiving the update from z, y updates its distance table with 
     Dy(x) = 51. Also, since z is now on y’s leastcost path to x, y poisons 
     the reverse path from z to x by informing z at time t=3 that Dy(x) = ∞ 
     (even though y knows that Dy(x) = 51 in truth)

TOOLS:
mininet was used to test the network topology and to ensure RIP.py worked in its 
untouched form as downloaded from the lab assignment.
