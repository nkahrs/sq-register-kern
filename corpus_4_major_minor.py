# 3/25/2019
# this is a copy of the corpus_1_basic-first file, but translating all the MIDI notes into Hz
# things might look different, or they might not! Who knows?

import os, csv, statistics
from kern_extract import parse_kern_file
from graphing_utilities import *
from major_minor import *

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

# get major and minor 2--4 note verticalities
major = list(filter(ismajor_pset, thedata))
minor = list(filter(isminor_pset, thedata))

# Figure 1: scatterplot of lowest pitch vs highest pitch
plt.figure(1)
sized_scatter([(i[0], i[-1]) for i in (major + minor)])
plt.xlabel('lowest pitch of tetrachord (MIDI)')
plt.ylabel('highest pitch of tetrachord (MIDI)')

# Figure 2: normalized
plt.figure(2)
sized_scatter([(i[0], i[-1] - i[0]) for i in (major + minor)])
plt.xlabel('lowest pitch of tetrachord (MIDI)')
plt.ylabel('semitone span')

# Figures 3-4: separate major, minor
plt.figure(3)
sized_scatter([(i[0], i[-1] - i[0]) for i in major])
plt.xlabel('lowest pitch of tetrachord (MIDI)')
plt.ylabel('semitone span')

plt.figure(4)
sized_scatter([(i[0], i[-1] - i[0]) for i in minor])
plt.xlabel('lowest pitch of tetrachord (MIDI)')
plt.ylabel('semitone span')

plt.show()
