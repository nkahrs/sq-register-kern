# 2/24/2019: to make sure I can scale this up the way I expect
# this file uses the whole corpus (in the "corpus" folder)
# and does some basic stats

import os, csv
from kern_extract import parse_kern_file
from graphing_utilities import *

# use \\ because this runs on windoze

# initialize structure
thedata = []
# 3/29 change: also count keys
thekeys = []

# go over all files
for root, dirs, files in os.walk(".\\corpus"):  
    for filename in files:
        thisfilepath = root + '\\' + filename
        # print(thisfilepath)
        # 3/23 change: eliminated one file that had unaligned stems after 8 bars, so no longer have try/except for that
        thisdata = parse_kern_file(thisfilepath, 16)
        # add key to list of keys
        thekeys += [thisdata[0]]
        # ignore key
        thisdata = thisdata[1]
        # add to main collection
        thedata += thisdata

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

# 3/23 addition: plot numbers of major and minor for 3-voice and 4-voice triads
from major_minor import *
thiscount = {}
thesekeys = ['maj3', 'maj4', 'min3', 'min4', 'dom7']
for i in thesekeys:
    thiscount[i] = 0
# manually tabulate the 5 cases (major/minor 3/4-voice, other)
for i in thedata:
    i = i[1] # strip duration
    if len(i) == 3:
        if ismajor_pset(i):
            thiscount['maj3'] += 1
        elif isminor_pset(i):
            thiscount['min3'] += 1
    elif len(i) == 4:
        if ismajor_pset(i):
            thiscount['maj4'] += 1
        elif isminor_pset(i):
            thiscount['min4'] += 1
        elif isdom7_pset(i):
            thiscount['dom7'] += 1
plt.figure(3)
fig3 = plt.bar(thesekeys, [thiscount[i] for i in thesekeys])
plt.xlabel('type of sonority')
plt.ylabel('# occurences in corpus')
# surprisingly, we get very few actual triads

# another 3/23 addition: scatterplot with controlled dot sizes of duration vs note count
plt.figure(4)
fig4 = sized_scatter([(i[0], len(i[1])) for i in thedata]) # (duration, # notes)
plt.xlabel('duration in whole notes')
plt.ylabel('# notes in chord')

# 3/29: list of keys
plt.figure(5)
thekeys.sort()
list_to_bar(thekeys)
plt.xlabel('key')
plt.ylabel('# movements')

plt.show()
