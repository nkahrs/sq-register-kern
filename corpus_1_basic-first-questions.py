# 3/25/2019: why did I let so much time pass? Sixxen piece and grad school visits.
# This file answers the first basic questions I initially set out to look at.

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

# extra 4- and 5-note chords
trichords = list(filter(lambda i: len(i)==3, thedata))
tetrachords = list(filter(lambda i: len(i)==4, thedata))

# Figure 1: scatterplot of lowest pitch versus highest pitch in tetrachords
plt.figure(1)
sized_scatter([(i[0], i[-1]) for i in tetrachords])
plt.xlabel('lowest pitch of tetrachord')
plt.ylabel('highest pitch of tetrachord')
plt.xlim(30, 100)
plt.ylim(30, 100)

# Figure 2: same thing but for trichords
plt.figure(2)
sized_scatter([(i[0], i[-1]) for i in trichords])
plt.xlabel('lowest pitch of trichord')
plt.ylabel('highest pitch of trichord')
plt.xlim(30, 100)
plt.ylim(30, 100)

# Figure 3: combined tri and tetrachords
tritetra = trichords + tetrachords

plt.figure(3)
sized_scatter([(i[0], i[-1]) for i in tritetra])
plt.xlabel('lowest pitch of pset')
plt.ylabel('highest pitch of pset')
plt.xlim(30, 100)
plt.ylim(30, 100)

# Figure 4: normalize y-axis by subtracting y = x
plt.figure(4)
sized_scatter([(i[0], (i[-1]-i[0])) for i in tritetra])
plt.xlabel('lowest pitch of pset')
plt.ylabel('semitones from lowest to highest pitch of pset')
plt.xlim(30, 100)
plt.ylim(0, 70)

# Figure 5: also look at mean based on tri/tetra
plt.figure(5)
tri_means = [(i[0], (i[-1]-i[0])/2) for i in trichords]
tetra_means = [(i[0], (i[-1]-i[0])/3) for i in tetrachords]
sized_scatter(tri_means + tetra_means)
plt.xlabel('lowest pitch of pset')
plt.ylabel('mean spacing between pitches, in semitones')
plt.xlim(30, 100)
plt.ylim(0, 35)


# Figure 6: try by highest pitch instead
plt.figure(6)
sized_scatter([(i[-1], (i[-1]-i[0])) for i in tritetra])
plt.xlabel('highest pitch of pset')
plt.ylabel('semitones from lowest to highest pitch of pset')
plt.xlim(30, 100)
plt.ylim(0, 70)

# now, want median note spacing.

# first, successive interval array
def differences(xs):
    return [t - s for s, t in zip(xs, xs[1:])]
# median spacing
def medspacing(xs):
    return statistics.median(differences(xs))

# Figure 7: what about median note spacing?
plt.figure(7)
sized_scatter([(i[0], medspacing(i)) for i in tritetra])
plt.xlabel('lowest pitch of pset')
plt.ylabel('median distance between pitches')
plt.xlim(30, 100)
plt.ylim(0, 35)


plt.show()
