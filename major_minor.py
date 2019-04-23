# I need to be able to get the prime form of a pitch-set or pitch-class set

# first, pset to pcset is easy
def pcset(pset):
    return list(set([i % 12 for i in pset]))

# you know what? I don't actually need full prime form here, and it's computationally expensive anyways.
# I can just check whether it's one of the 3 forms of 037
# assume it's already gone through the list(set(x)) stuff so it's sorted and duplicate-free

# let's separate major and minor
def zerotranspose(inputset):
    return sorted([i - min(inputset) for i in inputset]) #transpose to 0-based and ordered
    # 4/22/19 edit: sort set and use min instead of first to get rid of extensive false negatives that were massively skewing results

def ismajor(zeroed):
    return (zeroed in [[0, 4, 7], [0, 3, 8], [0, 5, 9]])

def isminor(zeroed):
    return (zeroed in [[0, 3, 7], [0, 4, 9], [0, 5, 8]])

def is037_zeroed(zeroed):
    return (ismajor(zeroed) or isminor(zeroed))

# also dominant seventh
def isdom7_zeroed(zeroed):
    return (sorted(zeroed) in [[0,4,7,10], [0,3,6,8], [0,3,5,9], [0,2,6,9]])

# end-user

def ismajor_pset(pset):
    return ismajor(zerotranspose(pcset(pset)))

def isminor_pset(pset):
    return isminor(zerotranspose(pcset(pset)))

def is037_pset(pset):
    return is037_zeroed(zerotranspose(pcset(pset)))

def isdom7_pset(pset):
    return isdom7_zeroed(zerotranspose(pcset(pset)))

# for future steps, depending on how much time I have, it could be interesting
# to have an actual prime-form calculator, so that I could tabulate prime forms
