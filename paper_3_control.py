# 4/10/19: compare to "chance"

import os, csv, statistics, random
from kern_extract import parse_kern_file, pitchclass
from graphing_utilities import *
from major_minor import *

# use \\ because this runs on windoze

# initialize structure
thedata = []

# go over all files
for root, dirs, files in os.walk(".\\corpus"):  
    for filename in files:
        thisfilepath = root + '\\' + filename
        # print(thisfilepath)
        thisdata = parse_kern_file(thisfilepath, 16)
        # ignore duration and turn key into pc number
        thisdata = (pitchclass(thisdata[0]), [i[1] for i in thisdata[1]])
        # add to main collection, ignoring key
        thedata += thisdata[1]

# sort all of our chords because we're not going to hear weird register changes
# also remove duplicated pitches to avoid weirdness
thedata = [sorted(list(set(i))) for i in thedata]

# look at only 4-note chords
tetrachords = list(filter(lambda i: len(i)==4, thedata))

# note that thedata :: [[Int]], where Int stands for pitch

# MIDI-Hz conversion
def mtof(midinote):
    abovea4 = midinote - 69 # distance from A440
    return (440 * (2.0**(abovea4/12.0)))

### Experiment 4a: separate into major/minor/dom7. do lo/hi/span
print('Experiment 5: control data')

voices = [[], [], [], []] # vc, vla, vln2, vln1

for i in tetrachords:
    if len(i) != 4:
        continue
    for j in range(4):
        voices[j].append(i[j])

# I now have the probability in each tetrachord voice, though not for the instruments in the whole corpus...

newtetras = []
for i in range(20000):
    thistetra = [0,0,0,0]
    for i in range(4):
        thistetra[i] = random.choice(voices[i])
    newtetras.append(sorted(thistetra))

for toggle in [0,1]:
    if toggle==0:
        print('MIDI')
        thisdata = newtetras
    else:
        print('Hz')
        thisdata = [[mtof(j) for j in i] for i in newtetras]
    # lo/hi/span
    lowests = [i[0] for i in thisdata]
    highests = [i[-1] for i in thisdata]
    means = [statistics.mean(i) for i in thisdata]
    ranges = [(i[-1]-i[0]) for i in thisdata]

    thecorrs = np.corrcoef([lowests, highests, means, ranges])
    for i in thecorrs:
            for j in i:
                    print(round(j,2), end='\t')
            print()
    print('\n')


# scatterplot for fun
#sized_scatter([(lowests[i], ranges[i]) for i in range(len(lowests))])


# intervals too
#2--4 note verticalities
relevant = newtetras
dyads = []
for j in relevant:
	dyads += [tuple(j[i:i+2]) for i in range(len(j)-1)]

relevantHz = [[mtof(j) for j in i] for i in relevant]
dyadsHz = []
for j in relevantHz:
	dyadsHz += [tuple(j[i:i+2]) for i in range(len(j)-1)]

print('N =', len(dyads))

experimentnames=['Experiment 5c: intervals/MIDI', 'Experiment 5d: intervals/Hz']
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
