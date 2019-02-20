# started 2/20/2019: extract basic info from Kern files into some sort of struct

# we'll use "kern" as a variable name for a kern file
# we'll assume the type is [String], ie a list of separate lines
# this way we can just say "for line in open()," etc.

# first, just get key and first n bars
# assumes all staves have same key signature
# :: [String], Int -> (String, [[String]])
# :: Kern, how many bars -> (key, [bar]) where bar is [notes]
def stripbars(kern, howmany):
    toreturn = []
    key = ''
    for line in kern:
        if line[0] == "!": # ignore comments
            continue
        else:
            line = line.split('\t') # split by tabs
            if line[0][0] == '*': # special start-of-staff lines
                if line[0][-1] == ':': #encode key
                    key = line[0][1:-1]
            elif line[0][0] == '=': # check bar numbers
                if '-' not in line[0] and int(line[0][1:]) > howmany:
                    break
            else: # otherwise just tack on the line
                toreturn.append(line)
    return (key, toreturn)


# now, we have to actually get useful data from this format

# define pitch class -> integer reference
pitchclassreference = {'c': 0, 'c-': 11, 'c#': 1, 'd': 2, 'd-': 1, 'd#': 3,
                       'e': 4, 'e-': 3, 'e#': 5, 'f': 5, 'f-': 4, 'f#': 6,
                       'g': 7, 'g-': 6, 'g#': 8, 'a': 9, 'a-': 8, 'a#': 10,
                       'b': 11, 'b-': 10, 'b#': 0}
# pitchclass: String -> Int (integer notation, C = 0)
def pitchclass(name):
    try:
        return pitchclassreference[name.lower()]
    except:
        raise ValueError('pitchclass: invalid note name')

# pitch: String -> Int (MIDI notation, C4 = 60)
def pitch(name):
    # check for accidentals, standardize name
    finalshift = 0
    if name[-1] == '-':
        name = name[0:-1]
        finalshift = -1
    elif name[-1] == '#':
        name = name[0:-1]
        finalshift = 1

    # calculate octave
    if name.isupper():
        octave = 4 - len(name)
    elif name.islower():
        octave = 3 + len(name)
    else:
        raise ValueError('pitch: invalid note name')

    pc = pitchclass(name[0])+finalshift
    return pc + (12*(octave+1))
        
        

if __name__=='__main__':
    with open('haydn_test.krn', 'r') as testfile:
        print(stripbars(testfile, 1))
