import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

from parse import string2func
from xkcd_plot import XKCDify

def plot(title, x_legend, y_legend, low, high, fs):
    xs = np.linspace(low, high, 100)
    ax = plt.axes()

    ax.set_title(title)
    ax.set_xlabel(x_legend)
    ax.set_ylabel(y_legend)
    plt.xlim(low, high)

    for f in fs:
        fix = f + " + 0*x"
        func = string2func(fix)
        ax.plot(xs, func(xs), label=f)

    ax.legend(loc='lower right')

    XKCDify(ax,
            xaxis_loc=0.0,
            yaxis_loc=0.0,
            xaxis_arrow='+-',
            yaxis_arrow='+-',
            expand_axes=True)

    plt.savefig('temp.png')
    plt.clf()
    plt.cla()

    return 'temp.png'
