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
        
        

if __name__=='__main__':
    with open('haydn_test.krn', 'r') as testfile:
        print(stripbars(testfile, 1))
