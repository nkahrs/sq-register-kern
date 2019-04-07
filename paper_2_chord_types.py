# 4/7/19: look at major/minor/dom7 and root scale degree

import os, csv, statistics
from kern_extract import parse_kern_file
from graphing_utilities import *
from major_minor import *

# use \\ because this runs on windoze

# initialize structure
thedata = []
# a second one for keeping the keys
keysdata = []

# go over all files
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

# look at only 3 and 4 note chords
##trichords = list(filter(lambda i: len(i)==3, thisdata))
##tetrachords = list(filter(lambda i: len(i)==4, thisdata))
##thedata = trichords + tetrachords

# note that thedata :: [[Int]], where Int stands for pitch

# MIDI-Hz conversion
def mtof(midinote):
    abovea4 = midinote - 69 # distance from A440
    return (440 * (2.0**(abovea4/12.0)))

# Experiment 4a: separate into major/minor/dom7. do lo/hi/span
print('Experiment 4a: major/minor')

# extract M/m/7
experiments = [('Major',        list(filter(ismajor_pset, thedata))),
               ('Minor',        list(filter(isminor_pset, thedata))),
               ('Dominant 7th', list(filter( isdom7_pset, thedata)))
               ]

for thisexpt in experiments:
    print(thisexpt[0])
    for j in [0,1]: # 0 = MIDI, 1 = Hz
        if j:
            print('Hz')
        else:
            print('MIDI')
        thisdata = thisexpt[1]
        if j: # conversion to Hz
            thisdata = [[mtof(j) for j in i] for i in thisdata]

        lowests = [i[0] for i in thisdata]
        highests = [i[-1] for i in thisdata]
        ranges = [(i[-1]-i[0]) for i in thisdata]

        thecorrs = np.corrcoef([lowests, highests, ranges])
        for i in thecorrs:
                for j in i:
                        print(round(j,2), end='\t')
                print()
        print('\n')

input()
