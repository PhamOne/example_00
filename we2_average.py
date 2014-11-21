# file: we2_average.py
#
# This python script loads an EDF file and computes the average
# value for each channel of the signal.
#
# Usage:
#  python we2_average.py filename.edf
#

# import some tools that we will need to accomplish this task
#
import sys              # a system library
import edfplus          # special software to load EDF files
import numpy            # a math library

###############################################################################
#
# the main program starts here
#
###############################################################################

# get the first argument, which is the filename of your EDF file
#
inputfile = sys.argv[1]

# load the filename using the edfplus library:
#  the function edfplus.load_edf() opens an EDF file and loads its data
#  into memory. the information in the file is stored in the variables
#  on the left side of the equal sign. We are mainly interested in "signal".
#
signal, sample_rate, physical_channels, time, tmp = edfplus.load_edf(inputfile)

# loop over all the channels of interest:
#  The EPOC returns data in a multidimensional array. There are 14 channels
#  of interest (2 to 15) but other channels that contain interesting data 
#  such as gyroscope data.
#
first_channel = 2
last_channel = 15

for i in range(first_channel, last_channel + 1):

    # compute the average and standard deviation
    #
    avg = numpy.mean(signal[i])
    std = numpy.std(signal[i])

    # display the results
    #
    print i, ": channel[", physical_channels[i], "]: avg = ", avg, \
        " std = ", std

###############################################################################
#
# the main program ends here
#
###############################################################################

