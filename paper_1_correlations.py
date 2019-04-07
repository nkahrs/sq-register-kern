# 4/4/19: rehashing "corpus_1_basic-first-questions" in terms of
# looking at many possbile correlations, for further investigations
# actually more questions too

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

# MIDI-Hz conversion
def mtof(midinote):
    abovea4 = midinote - 69 # distance from A440
    return (440 * (2.0**(abovea4/12.0)))

# experiments 1/2: MIDI and Hz
experimentnames=['Experiment 1: MIDI', 'Experiment 2: Hz']
for i in [0,1]:
    if i==0:
        thisdata = thedata
    elif i==1:
        thisdata = [[mtof(j) for j in i] for i in thedata]

    # look at only 3 and 4 note chords
    trichords = list(filter(lambda i: len(i)==3, thisdata))
    tetrachords = list(filter(lambda i: len(i)==4, thisdata))
    tritetra = trichords + tetrachords

    lowests = [i[0] for i in tritetra]
    highests = [i[-1] for i in tritetra]
    means = [statistics.mean(i) for i in tritetra]
    medians = [statistics.median(i) for i in tritetra]
    ranges = [(i[-1]-i[0]) for i in tritetra]

    # now, want median/mean note spacing.
    # first, successive interval array
    def differences(xs):
        return [t - s for s, t in zip(xs, xs[1:])]

    cints = [differences(i) for i in tritetra]
    medspacings = [statistics.median(i) for i in cints]
    meanspacings = [statistics.mean(i) for i in cints]

    print(experimentnames[i])
    thecorrs = np.corrcoef([lowests, highests, means, medians, ranges, meanspacings, medspacings])
    for i in thecorrs:
            for j in i:
                    print(round(j,2), end='\t')
            print()
    print('\n')

# Now experiment 3: intervals with MIDI/Hz

#2--4 note verticalities
relevant = list(filter(lambda i: len(i) in [2,3,4], thedata))
dyads = []
for j in relevant:
	dyads += [tuple(j[i:i+2]) for i in range(len(j)-1)]

relevantHz = [[mtof(j) for j in i] for i in relevant]
dyadsHz = []
for j in relevantHz:
	dyadsHz += [tuple(j[i:i+2]) for i in range(len(j)-1)]

experimentnames=['Experiment 3a: intervals/MIDI', 'Experiment 3b: intervals/Hz']
for i in [0,1]:
    if i==0:
        thisdata = dyads
    if i==1:
        thisdata = dyadsHz

    lowests = [i[0] for i in thisdata]
    highests = [i[-1] for i in thisdata]
    means = [statistics.mean(i) for i in thisdata]
    ranges = [(i[-1]-i[0]) for i in thisdata]
    
    print(experimentnames[i])
    thecorrs = np.corrcoef([lowests, highests, means, ranges])
    for i in thecorrs:
            for j in i:
                    print(round(j,2), end='\t')
            print()
    print('\n')

    
    

input()
