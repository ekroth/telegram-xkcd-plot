import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

from parse import string2func
from xkcd_plot import XKCDify

def plot(text, a=None, b=None):
    a = a or -1.0
    b = b or 1.0

    func = string2func(text)
    x = np.linspace(a, b, 100)
    ax = plt.axes()
    ax.plot(x, func(x))
    plt.xlim(a, b)

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
