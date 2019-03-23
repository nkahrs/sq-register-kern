# 2/24/2019: to make sure I can scale this up the way I expect
# this file uses the whole corpus (in the "corpus" folder)
# and does some basic stats

import os, csv, collections, itertools
import matplotlib.pyplot as plt
from kern_extract import parse_kern_file

# use \\ because this runs on windoze

# initialize structure
thedata = []

# go over all files
for root, dirs, files in os.walk(".\\corpus"):  
    for filename in files:
        thisfilepath = root + '\\' + filename
        # print(thisfilepath)
        thisdata = parse_kern_file(thisfilepath, 16)
        # ignore key
        thisdata = thisdata[1]
        # add to main collection
        thedata += thisdata

# list_to_bar: make a bar plot for distribution from a list:
def list_to_bar(thelist):
    counts = collections.Counter(thelist)
    thekeys = counts.keys()
    return plt.bar(thekeys, [counts[i] for i in thekeys])

# plot sheer quantities: how many n-chords?
plt.figure(1)
fig1 = list_to_bar([len(i[1]) for i in thedata])
plt.xlabel('# notes in chord')
plt.ylabel('# occurences in corpus')

# plot sheer quantities of pitches
# make list of pitches
allpitches = list(itertools.chain.from_iterable(
    [i[1] for i in thedata]))
# make figure
plt.figure(2)
fig2 = list_to_bar(allpitches)
plt.xlabel('pitch (in MIDI value)')
plt.ylabel('# occurences in corpus')

#show
plt.show()
