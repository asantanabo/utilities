import numpy as np
import matplotlib.pyplot as plt

#####################################
# Code created to generate the coordinates
# of a dendryte configuration to be added in
# stk.polymer
#####################################
#-----------------------------------------------------------
# initial conditions
#-----------------------------------------------------------

N = 200                # Lenght of the lattice
max_iter = 500000       # Temporal iterations for the process
n_walkers = 100        # Number of random walkers

#-----------------------------------------------------------
# Creation of the lattice space
#-----------------------------------------------------------

# Template arrays for random walks
x_step = np.array([-1,0,1,0])     # first neighbours in x direction
y_step = np.array([0,-1,0,1])     # first neighbors in y direction
dx=np.array([-1,0,1,0,-1,1,1,-1])   # Template for sticking to the
dy= np.array([0,-1,0,1,-1,-1,1,1])  # corresponding neighbor


# Creating the lattice

grid=np.zeros([N+2,N+2],dtype='int')
x=np.zeros(n_walkers,dtype='int')
y=np.zeros(n_walkers,dtype='int')
status=np.ones(n_walkers,dtype='int')

# Placing random walkers on a lattice
for i in range(0,n_walkers):
    x[i]=np.random.random_integers(0,N-1)
    y[i]=np.random.random_integers(0,N-1)
    grid[x[i],y[i]]=1

# Sticky point where everything else will start to grow
grid[N//2,N//2]=2
grid[N//4,N//4]=2

# Starting the calculation
iteration,n_glued=0,0
while (n_glued < n_walkers ) and (iteration < max_iter):
    for i in range(0,n_walkers):         # loop over the random walkers
        if status[i] == 1 :                # This walker is still mobile 
          ii=np.random.choice([0,1,2,3])   # Pick a random direction
          x_new=x[i]+x_step[ii]
          y_new=y[i]+y_step[ii]
          x_new=(N+x_new) % N              # Periodic bounday conditions in x
          y_new=(N+y_new) % N              # Periodic boundary conditions in y
          grid[x_new,y_new]=1              # Update lattice
          grid[x[i],y[i]]=0
          x[i],y[i]=x_new,y_new            # Move walkers 
          if 2 in grid[x[i]+dx[:],y[i]+dy[:]]:
              grid[x[i],y[i]]=2            # Assign sticky status to walker
              status[i]=2
              n_glued+=1

#Finished of looping through all mobile walkers and all walkers
# Graphic representation of the process
    iteration+=1
    print("iteration {0}, glued walkers {1}.".format(iteration,n_glued))
plt.imshow(grid,interpolation="nearest")
plt.show()
