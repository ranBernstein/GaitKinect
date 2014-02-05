import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate(data):    
    def update_line(num, data, line):
        line.set_data(xrange(num), data[:num])
        return line,
    
    fig = plt.figure()
    line, = plt.plot([], [], 'r-')
    plt.xlim(0, len(data))
    plt.ylim(np.min(data), np.max(data))
    
    line_ani = animation.FuncAnimation(fig, update_line, len(data), fargs=(data, line), interval=50, blit=True)
    #line_ani.save('my_animation.mp4')
    
    plt.show()