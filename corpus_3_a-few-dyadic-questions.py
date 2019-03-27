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
#thedata = [[mtof(j) for j in i] for i in thedata]

# get 2--4 note verticalities
relevant = list(filter(lambda i: len(i) in [2,3,4], thedata))

# and get all the dyads:
dyads = []
for j in relevant:
	dyads += [tuple(j[i:i+2]) for i in range(len(j)-1)]

# and in Hz
relevantHz = [[mtof(j) for j in i] for i in relevant]
dyadsHz = []
for j in relevantHz:
	dyadsHz += [tuple(j[i:i+2]) for i in range(len(j)-1)]

# Figure 1: lowest vs highest pitch, MIDI
plt.figure(1)
sized_scatter(dyads)
plt.xlabel('low note (MIDI)')
plt.ylabel('high note (MIDI)')

# Figure 2: same, Hz
plt.figure(2)
sized_scatter(dyadsHz)
plt.xlabel('low note (Hz)')
plt.ylabel('high note (Hz)')


# Figures 3--4: normalize y-axis by subtracting y = x
plt.figure(3)
sized_scatter([(i[0], (i[-1]-i[0])) for i in dyads])
plt.xlabel('lowest pitch (MIDI)')
plt.ylabel('size (semitones)')

plt.figure(4)
sized_scatter([(i[0], (i[-1]-i[0])) for i in dyadsHz])
plt.xlabel('lowest pitch (Hz)')
plt.ylabel('size (delta Hz)')

# Figures 5--6: by highest pitch instead
plt.figure(5)
sized_scatter([(i[1], (i[-1]-i[0])) for i in dyads])
plt.xlabel('lowest pitch (MIDI)')
plt.ylabel('size (semitones)')

plt.figure(6)
sized_scatter([(i[1], (i[-1]-i[0])) for i in dyadsHz])
plt.xlabel('lowest pitch (Hz)')
plt.ylabel('size (delta Hz)')

plt.show()
