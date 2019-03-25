# 3/25: refactoring from corpus_0 to reuse code more comfortably

import collections, itertools
import matplotlib.pyplot as plt

# list_to_bar: make a bar plot for distribution from a list:
def list_to_bar(thelist):
    counts = collections.Counter(thelist)
    thekeys = counts.keys()
    return plt.bar(thekeys, [counts[i] for i in thekeys])

# sized_scatter: given [(Num, Num)], make a scatterplot with appropriate
# dot sizes for things that reoccur
def sized_scatter(thelist):
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

    return plt.scatter(xs, ys, s = sizes)

    
