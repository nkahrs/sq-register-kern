# 3/25: refactoring from corpus_0 to reuse code more comfortably

import collections, itertools
import matplotlib.pyplot as plt
import numpy as np

# list_to_bar: make a bar plot for distribution from a list:
def list_to_bar(thelist):
    counts = collections.Counter(thelist)
    thekeys = counts.keys()
    return plt.bar(thekeys, [counts[i] for i in thekeys])

# sized_scatter: given [(Num, Num)], make a scatterplot with appropriate
# dot sizes for things that reoccur
def sized_scatter(thelist, regression = True):
    thiscount = {} # make dict to count things
    for i in thelist:
        if i in thiscount.keys():
            thiscount[i] += 1
        else:
            thiscount[i] = 1

    thiskeys = thiscount.keys()
    xs = [i[0] for i in thiskeys]
    ys = [i[1] for i in thiskeys]
    sizes = [thiscount[i] for i in thiskeys]

    # unless specified otherwise, also run/plot a linear regression
    if regression:
        linear = np.polyfit(xs, ys, 1)
        # print(linear)
        # plot it, just from min to max values of xs for now
        theline = np.poly1d(linear)
        linearxs = [min(xs), max(xs)]
        plt.plot(linearxs, theline(linearxs), color='red')
        # and correlation
        correlation = np.corrcoef(xs, ys)
        print(correlation[1][0])

    return plt.scatter(xs, ys, s = sizes)

# like sized_scatter, but a bit more flexibility so we can plot multiple things at once
# too much copypasta, maybe refactor later
def sized_scatter_sub(thelist, thiscolor, thislabel, regression = True):
    thiscount = {} # make dict to count things
    for i in thelist:
        if i in thiscount.keys():
            thiscount[i] += 1
        else:
            thiscount[i] = 1

    thiskeys = thiscount.keys()
    xs = [i[0] for i in thiskeys]
    ys = [i[1] for i in thiskeys]
    sizes = [thiscount[i] for i in thiskeys]

    # unless specified otherwise, also run/plot a linear regression
    if regression:
        linear = np.polyfit(xs, ys, 1)
        # print(linear)
        # plot it, just from min to max values of xs for now
        theline = np.poly1d(linear)
        linearxs = [min(xs), max(xs)]
        plt.plot(linearxs, theline(linearxs), color=thiscolor)

    return plt.scatter(xs, ys, s = sizes, color=thiscolor, label=thislabel, alpha=0.7)
    
