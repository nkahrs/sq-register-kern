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

### Figure 1: scatterplot of lowest pitch versus highest pitch in tetrachords
##plt.figure(1)
##sized_scatter([(i[0], i[-1]) for i in tetrachords])
##plt.xlabel('lowest pitch of tetrachord (Hz)')
##plt.ylabel('highest pitch of tetrachord (Hz)')
##plt.xlim(50, 600)
##plt.ylim(50, 1800)
##
### Figure 2: same thing but for trichords
##plt.figure(2)
##sized_scatter([(i[0], i[-1]) for i in trichords])
##plt.xlabel('lowest pitch of trichord (Hz)')
##plt.ylabel('highest pitch of trichord (Hz)')
##plt.xlim(50, 600)
##plt.ylim(50, 1800)

# Figure 3: combined tri and tetrachords
tritetra = trichords + tetrachords

plt.figure(3)
sized_scatter([(i[0], i[-1]) for i in tritetra])
plt.xlabel('lowest pitch of pset (Hz)')
plt.ylabel('highest pitch of pset (Hz)')
plt.xlim(50, 800)
#plt.xlim(50, 1800)

# Figure 4: normalize y-axis by subtracting y = x
plt.figure(4)
sized_scatter([(i[0], (i[-1]-i[0])) for i in tritetra])
plt.xlabel('lowest pitch of pset (Hz)')
plt.ylabel('difference between lowest and highest pitch of pset (Hz)')
plt.xlim(50, 800)
#plt.xlim(0, 1750)

# Figure 5: also look at mean based on tri/tetra
plt.figure(5)
tri_means = [(i[0], (i[-1]-i[0])/2) for i in trichords]
tetra_means = [(i[0], (i[-1]-i[0])/3) for i in tetrachords]
sized_scatter(tri_means + tetra_means)
plt.xlabel('lowest pitch of pset (Hz)')
plt.ylabel('mean spacing between pitches (delta Hz)')
plt.xlim(50, 1800)
plt.xlim(0, 900)


# Figure 6: try by highest pitch instead
plt.figure(6)
sized_scatter([(i[-1], (i[-1]-i[0])) for i in tritetra])
plt.xlabel('highest pitch of pset (Hz)')
plt.ylabel('delta Hz from lowest to highest pitch of pset')
plt.xlim(50, 1800)
plt.xlim(0, 1750)

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
plt.xlabel('lowest pitch of pset (Hz)')
plt.ylabel('median distance between pitches (delta Hz)')
plt.xlim(50, 1800)
plt.xlim(0, 900)


plt.show()
