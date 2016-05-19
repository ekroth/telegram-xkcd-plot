import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from stopit import threading_timeoutable as timeoutable

from parse import string2func
from xkcd_plot import XKCDify

def plot(title, x_legend, y_legend, low, high, fs):
    xs = np.linspace(low, high, 100)
    ax = plt.axes()

    ax.set_title(title)
    ax.set_xlabel(x_legend)
    ax.set_ylabel(y_legend)
    plt.xlim(low, high)

    @timeoutable()
    def calc():
        for f in fs:
            fix = f + " + 0*x"
            func = string2func(fix)
            ax.plot(xs, func(xs), label=f)

        return True

    if calc(timeout=1) is None:
        raise Exception("Calculation timeout.")

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
