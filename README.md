# SDN
SDN lab TTM4150



To run the mininet topology for assignment 1, start the controller with `./bin/ryu-manager /pathToControllerApp`
Then start your topology with `mn --custom /home/lab/test2.py  --topo singleswitchtopo --link tc --controller=remote`

We also need to force each switch to speak OpenFlow version 1.3.
This can be done with the following: `sudo ovs-vsctl set bridge s1 protocols=OpenFlow13`
Repeat for all the other switches.
