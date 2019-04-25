# 3/25/2019
# this is a copy of the corpus_1_basic-first file, but translating all the MIDI notes into Hz
# things might look different, or they might not! Who knows?

import os, csv, statistics
from kern_extract import parse_kern_file
from graphing_utilities import *

# use \\ because this runs on windoze

# initialize structure
thedata = []

# go over all files, copied from "0_stats"
for root, dirs, files in os.walk(".\\corpus"):  
    for filename in files:
        thisfilepath = root + '\\' + filename
        # print(thisfilepath)
        thisdata = parse_kern_file(thisfilepath, 16)
        # ignore key
        thisdata = thisdata[1]
        # ignore duration
        thisdata = [i[1] for i in thisdata]
        # add to main collection
        thedata += thisdata

# sort all of our chords because we're not going to hear weird register changes
# also remove duplicated pitches to avoid weirdness
thedata = [sorted(list(set(i))) for i in thedata]
# note that thedata :: [[Int]], where Int stands for pitch

# general midi->frequency conversion
def mtof(midinote):
    abovea4 = midinote - 69 # distance from A440
    return (440 * (2.0**(abovea4/12.0)))

# convert all data to frequencies
thedata = [[mtof(j) for j in i] for i in thedata]

# extra 4- and 5-note chords
trichords = list(filter(lambda i: len(i)==3, thedata))
tetrachords = list(filter(lambda i: len(i)==4, thedata))

tritetra = trichords + tetrachords


# Figure 4: normalize y-axis by subtracting y = x
##plt.figure(1)
##sized_scatter([(i[0], (i[-1]-i[0])) for i in tritetra])
##plt.xlabel('lowest pitch of pset (Hz)')
##plt.ylabel('difference between lowest and highest pitch of pset (Hz)')
##plt.xlim(50, 1800)
##plt.xlim(0, 1750)

# draft: a histogram for each bass note
bassnotes = sorted(list(set([i[0] for i in tritetra])))

##for thisbass in bassnotes:
##    plt.figure()
##    these_chords = filter(lambda i: i[0]==thisbass, tritetra)
##    list_to_bar([(i[-1]-i[0]) for i in these_chords])
##    plt.title(thisbass)
##    plt.show()

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(2)
ax = fig.add_subplot(111, projection='3d')


# want to make a list of (x, y, z), then extract each
# x = bass, y = span, z = count
bars = []
for thisbass in bassnotes:
    these_chords = [i for i in tritetra if i[0]==thisbass]
    these_spans = [(i[-1]-i[0]) for i in these_chords]
    spancounts = collections.Counter(these_spans)
    for i in spancounts.keys():
        bars.append((thisbass, i, spancounts[i], spancounts[i]/len(these_chords)))

xs = []
ys = []
zs = []

for i in bars:
    xs.append(i[0])
    ys.append(i[1])
    zs.append(i[2])

ax.bar3d(xs, ys, 0, 20, 20, zs)
ax.set_xlabel('bass note (Hz)')
ax.set_ylabel('span (Hz)')
ax.set_zlabel('count')

ax.view_init(30, 315)

# aggregate histogram
plt.figure(3)
list_to_bar([(i[-1]-i[0]) for i in tritetra])


# and then 3d chart that's normalized by bass note
fig = plt.figure(4)
ax = fig.add_subplot(111, projection='3d')

xs = []
ys = []
zs = []

for i in bars:
    xs.append(i[0])
    ys.append(i[1])
    zs.append(i[3])
    # previously, this read:
    # / len([j for j in bars if (j[0]==i[0])]))
    # however, the denominator was too small for some reason
    # workaround was to calculate the relevant stats earlier, saving an iteration

ax.bar3d(xs, ys, 0, 20, 20, zs)
ax.set_xlabel('bass note (Hz)')
ax.set_ylabel('span (Hz)')
ax.set_zlabel('probability given bass note')

ax.view_init(30, 225)

plt.show()
