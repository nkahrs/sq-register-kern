
import os, csv, statistics, random
from kern_extract import parse_kern_file, pitchclass
from graphing_utilities import *

#---------------------------------------------------------------------
# from corpus_1


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

# Figure 3: combined tri and tetrachords
tritetra = trichords + tetrachords

plt.figure(1)
sized_scatter([(i[0], i[-1]) for i in tritetra])
plt.xlabel('lowest pitch of pset (MIDI)')
plt.ylabel('highest pitch of pset (MIDI)')
plt.xlim(35, 70)
#plt.ylim(30, 100)

# Figure 4: normalize y-axis by subtracting y = x
plt.figure(2)
sized_scatter([(i[0], (i[-1]-i[0])) for i in tritetra])
plt.xlabel('lowest pitch of pset (MIDI)')
plt.ylabel('semitones from lowest to highest pitch of pset')
plt.xlim(35, 70)
#plt.ylim(0, 70)




#---------------------------------------------------------------------
# from corpus_2


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

# Figure 3: combined tri and tetrachords
tritetra = trichords + tetrachords

plt.figure(3)
sized_scatter([(i[0], i[-1]) for i in tritetra])
plt.xlabel('lowest pitch of pset (Hz)')
plt.ylabel('highest pitch of pset (Hz)')
plt.xlim(50, 400)
#plt.xlim(50, 1800)

# Figure 4: normalize y-axis by subtracting y = x
plt.figure(4)
sized_scatter([(i[0], (i[-1]-i[0])) for i in tritetra])
plt.xlabel('lowest pitch of pset (Hz)')
plt.ylabel('difference between lowest and highest pitch of pset (Hz)')
plt.xlim(50, 400)
#plt.xlim(0, 1750)


#---------------------------------------------------------------------
# from paper_3a


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

scales = ['MIDI', 'Hz']
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

    # plot figures
    plt.figure(2*(3+toggle))
    sized_scatter([(lowests[i], highests[i]) for i in range(len(lowests))])
    plt.xlabel('lowest pitch ('+scales[toggle]+')')
    plt.ylabel('highest pitch ('+scales[toggle]+')')
    if toggle==0:
        plt.xlim(35,70)
    else:
        plt.xlim(50,400)

    plt.figure(2*(3+toggle)+1)
    sized_scatter([(lowests[i], ranges[i]) for i in range(len(lowests))])
    plt.xlabel('lowest pitch ('+scales[toggle]+')')
    plt.ylabel('span ('+scales[toggle]+')')
    if toggle==0:
        plt.xlim(35,70)
    else:
        plt.xlim(50,400)

    thecorrs = np.corrcoef([lowests, highests, means, ranges])
    for i in thecorrs:
            for j in i:
                    print(round(j,2), end='\t')
            print()
    print('\n')





plt.show()
