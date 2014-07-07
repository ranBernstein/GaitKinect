import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

pause = False
def simData():
    t_max = 10.0
    dt = 0.05
    x = 0.0
    t = 0.0
    while t < t_max:
        if not pause:
            x = np.sin(np.pi*t)
            t = t + dt
        yield x, t

def onClick(event):
    global pause
    pause ^= True

def simPoints(simData):
    x, t = simData[0], simData[1]
    time_text.set_text(time_template%(t))
    line.set_data(t, x)
    return line, time_text

fig = plt.figure()
ax = fig.add_subplot(111)
line, = ax.plot([], [], 'bo', ms=10) # I'm still not clear on this stucture...
ax.set_ylim(-1, 1)
ax.set_xlim(0, 10)

time_template = 'Time = %.1f s'    # prints running simulation time
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
fig.canvas.mpl_connect('button_press_event', onClick)
ani = animation.FuncAnimation(fig, simPoints, simData, blit=False, interval=10,
    repeat=True)
plt.show()