import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg') # Need to use in order to run on mac
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

"""
Reqiered:
    data: [number of frames][number of joints]
Optional:
    showTrajectory, showSticks, rotate: bool
    time: list
    hirarchy: list of tuples
"""
def renderSkeleton(data, **kwargs):
    time = kwargs.pop('time', None)
    if time is None:
        time = range(len(data))
    showTrajectory = kwargs.pop('showTrajectory', False)
    showSticks = kwargs.pop('showSticks', False)
    rotate = kwargs.pop('rotate', False)
    hirarchy = kwargs.pop('rotate', [])
    jointsNum = len(data[0])
    
    
    # Set up figure & 3D axis for animation
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('on')
    
    # choose a different color for each trajectory
    colors = plt.cm.jet(np.linspace(0, 1, jointsNum))
    # set up trajectory lines
    lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
    # set up points
    pts = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])
    
    stick_lines = [ax.plot([], [], [], 'k-')[0] for _ in hirarchy]
    dic={}
    dataByJoints = np.zeros(shape=(jointsNum,len(data),3))
    for j in range(jointsNum):
        for l in range(len(data)):
            dataByJoints[j, l, :] = data[l][j]
            #np.array([data[l][3*j], data[l][3*j+1],data[l][3*j+2]])
    
    # prepare the axes limits
    maxes =np.zeros((3,1))
    mins=np.zeros((3,1))
    for d in range(3):
        maxes[d] = np.max(dataByJoints[:,:,d])
        maxes[d] = maxes[d]*1.3 if maxes[d]>0 else maxes[d]*0.7
        mins[d] = np.min(dataByJoints[:,:,d])
        mins[d] = mins[d]*1.3 if mins[d]<0 else mins[d]*0.7
    #maxes=maxes[[0, 2, 1]]  
    #mins=mins[[0, 2, 1]]  
    print maxes
    print mins
    ax.set_xlim((mins[0], maxes[0]))
    ax.set_ylim((mins[2], maxes[2])) # note usage of z coordinate
    ax.set_zlim((mins[1], maxes[1])) # note usage of y coordinate
    
    # set point-of-view: specified by (altitude degrees, azimuth degrees)
    ax.view_init(30, 0)
    
    # initialization function: plot the background of each frame
    def init():
        for line, pt in zip(lines, pts):
            # trajectory lines
            line.set_data([], [])
            line.set_3d_properties([])
            # points
            pt.set_data([], [])
            pt.set_3d_properties([])
        return lines + pts + stick_lines
    
    showTrajectory = True
    showSticks = False
    rotate= False
    # animation function.  This will be called sequentially with the frame number
    #x_t= np.array(data)
    x_t = dataByJoints
    x_t = x_t[:, :, [0, 2, 1]]
    print x_t[0][0] 
    def animate(i):
        # we'll step two time-steps per frame.  This leads to nice results.
        i = (5 * i) % x_t.shape[1]
    
        for line, pt, xi in zip(lines, pts, x_t):
            x, y, z = xi[:i].T # note ordering of points to line up with true exogenous registration (x,z,y)
            pt.set_data(x[-1:], y[-1:])
            pt.set_3d_properties(z[-1:])
            
            # trajectory lines
            if showTrajectory:
                line.set_data(x,y)
                line.set_3d_properties(z)
                
        if showSticks:
            for stick_line, (sp, ep) in zip(stick_lines, hirarchy):
                stick_line._verts3d = x_t[[sp,ep], i, :].T.tolist()
    
        if rotate:
            ax.view_init(30, 0.3 * i)
        fig.canvas.draw()
        return lines + pts + stick_lines
    
    # instantiate the animator.
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=500, interval=30, blit=True)
    plt.show()
    return fig
"""
stick_defines = [
    (0, 1),
    (1, 2),
    (3, 4),
    (4, 5),
    (6, 7),
    (7, 8),
    (9, 10),
    (10, 11)
]
t_start = 1917 # start frame
t_end = 2130 # end frame

data = pd.read_csv('../inputs/Smart-first_phase_NaN-zeros.csv') # only coordinate data
df = data.loc[t_start:t_end,'Shoulder_left_x':'Ankle_right_z']
data = df.values.tolist()

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
        
newData = []
for line in data:
    newData.append(chunks(line, 3))
renderSkeleton(newData)
"""











