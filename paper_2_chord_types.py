# 4/7/19: look at major/minor/dom7 and root scale degree

import os, csv, statistics
from kern_extract import parse_kern_file, pitchclass
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
        # ignore duration
        thisdata = (thisdata[0], [i[1] for i in thisdata[1]])
        thisdata = (thisdata[0], list(filter(lambda i: len(i) in [3,4], thisdata[1])))
        # add to main collection, ignoring key
        thedata += thisdata[1]
        # add to separate collection with key
        keysdata.append(thisdata)

# sort all of our chords because we're not going to hear weird register changes
# also remove duplicated pitches to avoid weirdness
thedata = [sorted(list(set(i))) for i in thedata]

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


# isolate the "run this in semitones and then again in Hertz and print the data"
# part because I do it a lot in different contexts
def run_this_pair(thisdata):
    print("N =", len(thisdata))
    for j in [0,1]: # 0 = MIDI, 1 = Hz
        if j:
            print('Hz')
        else:
            print('MIDI')
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
    return

for thisexpt in experiments:
    print(thisexpt[0])
    thisdata = thisexpt[1]
    run_this_pair(thisdata)


# Experiment 4b: lo/hi/span for each root scale degree
print('Experiment 4b: scale degrees')

# for each scaledegree, what height above key?
heightsizes = [[0],    #^1
               [1, 2], #^2
               [3, 4], #^3
               [5, 6], #^4
               [7],    #^5
               [8, 9], #^6
               [10, 11] #^7
               ]

for degree in range(7):
    print("Scale Degree", degree+1, '\n')

    # start structure
    thisdata = []
    
    # keep only those chords whose lowest pc is the right scaledegree, and is size 3/4.
    # I could do this more concisely...
    for i in keysdata:
        # i[0] is key as string, i[1] is list of chords
        tonic = pitchclass(i[0])
        for j in i[1]:
            if (len(j) in [3,4]) and (((j[0] - tonic) % 12) in heightsizes[degree]):
                thisdata.append(j)
    run_this_pair(thisdata)
    
# 4c: by key
print('Experiment 4c: global keys')

databykey = {}
for i in keysdata:
    if not (i[0] in databykey.keys()):
        databykey[i[0]] = []
    databykey[i[0]] += i[1]

for key in databykey.keys():
    thisdata = databykey[key]
    print(key)
    run_this_pair(thisdata)

input()
