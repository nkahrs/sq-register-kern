# 2/24/2019: to make sure I can scale this up the way I expect
# this file tests kern_extract on the entire Haydn Quartet Op. 9 No. 2
# and will provide basic statistics on sonority counts

import os, csv
from kern_extract import parse_kern_file

# use \\ because this runs on windoze

# initialize structure
thedata = []

# go over all files
for root, dirs, files in os.walk(".\\haydn_op9_no2_kern"):  
    for filename in files:
        thisfilepath = root + '\\' + filename
        print(thisfilepath)
        thisdata = parse_kern_file(thisfilepath, 8)
        # ignore key
        thisdata = thisdata[1]
        # reduce to (duration, num pitches)
        thisdata = [(i[0], len(i[1])) for i in thisdata]
        # add to main collection
        thedata += thisdata

# show us main data points
#print(thedata)

# send to csv for excel or something
##with open('test.csv', 'w') as thisfile:
##    thiswriter = csv.writer(thisfile)
##    thiswriter.dialectwriterows(thedata)
