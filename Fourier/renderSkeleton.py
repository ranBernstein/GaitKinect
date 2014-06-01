"""
Full animation of a walking event (note: a lot of missing data) 
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg') # Need to use in order to run on mac
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

#=============================================================================================

t_start = 1917 # start frame
t_end = 2130 # end frame

data = pd.read_csv('inputs/Smart-first_phase_NaN-zeros.csv') # only coordinate data
df = data.loc[t_start:t_end,'Shoulder_left_x':'Ankle_right_z']

# Find max and min values for animation ranges
df_minmax = pd.DataFrame(index=list('xyz'),columns=range(2))
for i in list('xyz'):
    c_max = df.filter(regex='_{}'.format(i)).max().max()
    c_min = df.filter(regex='_{}'.format(i)).min().min()
    df_minmax.ix[i] = np.array([c_min,c_max])

df_minmax = 1.3*df_minmax # increase by 30% to make animation look better

df.columns  = np.repeat(range(12),3) # store cols like this for simplicity
N_tag = df.shape[1]/3 # nr of tags used (all)

N_trajectories = N_tag

t = np.linspace(0,data.Time[t_end],df.shape[0]) # pseudo time-vector for first walking activity
x_t = np.zeros(shape=(N_tag,df.shape[0],3)) # empty animation array (3D)

for tag in range(12):
    # store data in numpy 3D array: (tag,time-stamp,xyz-coordinates)
    x_t[tag,:,:] = df[tag]


#===STICK-LINES========================================================================================
#xx = [x_t[1,:,0],x_t[2,:,0]]
#yy = [x_t[1,:,1],x_t[2,:,1]]
#zz = [x_t[1,:,2],x_t[2,:,2]] 
#======================================================================================================

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('on')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))
# set up trajectory lines
lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
# set up points
pts = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])
# set up lines which create the stick figures
stick_lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])

# prepare the axes limits
ax.set_xlim(df_minmax.ix['x'].values)
ax.set_ylim(df_minmax.ix['z'].values) # note usage of z coordinate
ax.set_zlim(df_minmax.ix['y'].values) # note usage of y coordinate

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt, stick_line in zip(lines, pts, stick_lines):
        # trajectory lines
        line.set_data([], [])
        line.set_3d_properties([])
        # points
        pt.set_data([], [])
        pt.set_3d_properties([])
        # stick lines
        stick_line.set_data([], [])
        stick_line.set_3d_properties([])
    return lines + pts + stick_lines

# animation function.  This will be called sequentially with the frame number
def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    i = (5 * i) % x_t.shape[1]

    for line, pt, stick_line, xi in zip(lines, pts, stick_lines, x_t):
        x, z, y = xi[:i].T # note ordering of points to line up with true exogenous registration (x,z,y)
        # trajectory lines
        line.set_data(x,y)
        line.set_3d_properties(z)
        # points
        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])
        # stick lines
        #stick_line.set_data(xx,zz)
        #stick_line.set_3d_properties(yy)
    #ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return lines + pts + stick_lines

# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=500, interval=30, blit=True)

# Save as mp4. This requires mplayer or ffmpeg to be installed
#anim.save('lorentz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

plt.show()