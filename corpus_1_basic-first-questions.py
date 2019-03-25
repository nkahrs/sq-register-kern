# 3/25/2019: why did I let so much time pass? Sixxen piece and grad school visits.
# This file answers the first basic questions I initially set out to look at.

import os, csv
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
for i in thedata:
    i.sort()

# note that thedata :: [[Int]], where Int stands for pitch

# extra 4- and 5-note chords
trichords = list(filter(lambda i: len(i)==3, thedata))
tetrachords = list(filter(lambda i: len(i)==4, thedata))

# Figure 1: scatterplot of lowest pitch versus highest pitch in tetrachords
plt.figure(1)
sized_scatter([(i[0], i[-1]) for i in tetrachords])
plt.xlabel('lowest pitch of tetrachord')
plt.ylabel('highest pitch of tetrachord')

# Figure 2: same thing but for trichords
plt.figure(2)
sized_scatter([(i[0], i[-1]) for i in trichords])
plt.xlabel('lowest pitch of trichord')
plt.ylabel('highest pitch of trichord')

# Figure 3: combined tri and tetrachords
plt.figure(3)
sized_scatter([(i[0], i[-1]) for i in (trichords + tetrachords)])
plt.xlabel('lowest pitch of pset')
plt.ylabel('highest pitch of pset')

plt.show()
