from PolymerCpp.helpers import getCppSAWLC
import mpl_toolkits.mplot3d 
import matplotlib.pyplot as plt
from PolymerCpp.helpers import getCppWLC2D
import numpy as np

#############################################
## Code used to create a chain of a polymer 
## using the self avoided random walk library 
## for 3-d cases
#############################################


pathLength = 500
persisLength = 10


chain = getCppSAWLC(pathLength, persisLength, linkDiameter=0.75)
#chain = getCppWLC2D(pathLength, persisLength)
#print (chain.shape)

x = []
y = []
z = []

for i in range(len(chain)):
    x.append(chain[i][0])
    y.append(chain[i][1])
    z.append(chain[i][2])

x = np.asarray(x)
y = np.asarray(y)
z = np.asarray(z)

excl = 1.42
x_new = x*excl
y_new = y*excl
z_new = z*excl


for i in range(len(x_new)):
   print (x_new[i],y_new[i],z_new[i])



# plotting part    
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(x_new,y_new,z_new)
#plt.scatter(x,y)
plt.show()
