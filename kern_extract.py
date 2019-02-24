# started 2/20/2019: extract basic info from Kern files into some sort of struct
# completed 2/24/2019

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
            # be mindful of newlines at end
            if line[-1] == '\n':
                line = line[0:-1]
            line = line.split() # split by tabs or spaces
            if line[0][0] == '*': # special start-of-staff lines
                if line[0][-1] == ':': #encode key
                    key = line[0][1:-1]
            elif line[0][0] == '=': # check bar numbers
                try:
                    if '-' not in line[0] and int(line[0][1:]) > howmany:
                        break
                except: # if a line has more than one ==
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
    # first, check for rest
    if name == 'r':
        return None
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

# next: need something for line ([String]) to (Int, [Int]) as in (duration, [notes])

# parse_kern_atom :: String -> (Float, Int)
# given something like "8gg", split into the two parts
# in length of measure: ie 8th note -> 0.125
# string 'gg' -> G5 -> 79
def parse_kern_atom(kern_atom):
    # first, check for null case
    if '.' in kern_atom:
        return (None, None)
    # split into beginning duration and remaining pitch
    # discard other data (ie beaming)
    thisdur = ''
    thispitch = ''
    for i in kern_atom:
        if i in '1234567890': # duration data
            thisdur += i
        elif i in 'ABCDEFGabcdefg#-r': # pitch data or rest
            thispitch += i
    thisdur = int(thisdur)
    return (1.0/thisdur, pitch(thispitch))

# parse_kern_line: [String] -> (Float, [Int])
# input: a list of strings like "8gg" as above
# output: overall duration of sonority (shortest) and list of pitches
def parse_kern_line(kern_line):
    # parse atoms
    parsed_atoms = [parse_kern_atom(i) for i in kern_line]
    # find shortest duration
    durs = [i[0] for i in parsed_atoms]
    durs = list(filter(lambda i: i != None, durs))
    if durs:
        shortestdur = min(durs)
    else:
        shortestdur = 0
    # get pitches
    pitches = [i[1] for i in parsed_atoms]
    pitches = list(filter(lambda i: type(i)==int, pitches))
    return (shortestdur, pitches)

# parse_kern_bars: above generalized to output of stripbars
# (String, [[String]]) -> (String, [(Float, [Int])])
# input: output of stripbars
# output: (key, [(duration, [Pitch])])
def parse_kern_bars(kern_bars):
    return (kern_bars[0], [parse_kern_line(i) for i in kern_bars[1]])

# parse_kern_file: generalize above to filename and number of bars
# String, Int -> (String, [(Float, [Int])])
# filepath, number of bars -> (key, [(duration, [Pitch])])
def parse_kern_file(filepath, numbars):
    with open(filepath, 'r') as thisfile:
        return parse_kern_bars(stripbars(thisfile, numbars))

# note that I've encountered a bug: if stems become non-aligned, it crashes due to trying to parse "=" as note data

if __name__=='__main__':
    with open('haydn_test.krn', 'r') as testfile:
        foo = stripbars(testfile, 3)
        print(foo)
        print(parse_kern_bars(foo))
    print('or generalized:')
    foo = parse_kern_file('haydn_test.krn', 8)
    print(foo[0])
    for i in foo[1]:
        print(i)
        
