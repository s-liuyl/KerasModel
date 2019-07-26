import numpy as np
import matplotlib 
matplotlib.use('Agg')
import  matplotlib.pyplot as plt
X = [0.8536,0.6321,0.7373,0.4127,0.8689,0.9189,0.7854,0.8806,0.2419,0.7917,0.9596,0.5457]
Y = [0.6536,0.6368,0.7813,0.5060,0.5615,0.9291,0.8157,0.8396,0.4960,0.7500,0.9743,0.6774]
x = [0,1]
y = [0,1]
plt.cla()
plt.plot(x,y,'b')
plt.plot(X,Y, 'r.')
plt.xlabel('Clustered')
plt.ylabel('ClusterQA')
plt.savefig('/home/elaine/KerasModel/ClusteredvsClusterQA.png', format = 'png')
X = [0.8536,0.6321,0.7373,0.5934,0.8689,0.7854,0.3266,0.7879,0.9596,0.6586]
Y = [0.7107,0.6368,0.7969,0.5934,0.9467,0.8157,0.4960,0.7765,0.9743,0.6774]

plt.cla()
plt.plot(x,y,'b')
plt.plot(X,Y, 'r.')
plt.xlabel('Clustered')
plt.ylabel('ClusterQA')
plt.savefig('/home/elaine/KerasModel/ClusteredvsClusterQA5.png', format = 'png')
