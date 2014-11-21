# file: we2_train.py
#
# This python script loops over a set of EDF files and trains a model.
#
# Usage:
#  python we2_train.py r_model.txt data_r.list
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

# load the filelist
#
fnames = open(sys.argv[2]).read().splitlines()

# load the first file to get the number of channels
#
signal, srate, phys_chan, time, tmp = edfplus.load_edf(fnames[0])
num_channels = len(phys_chan);

# create variables to hold accumulated values
#
num_files = 0
acc_avg = numpy.zeros(num_channels)
acc_std = numpy.zeros(num_channels)

# loop over all the input files:
#  note that the first entry in argv is the program name
#
for inputfile in fnames:

    # load the edf data
    #
    print '%s:' % inputfile
    signal, srate, phys_chan, time, tmp = edfplus.load_edf(inputfile)
    num_files += 1

    # loop over all channels in the file
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
        print '%d: channel[%s]: avg = %10.4f std = %10.4f' \
            % (i, phys_chan[i], avg, std)

        # accumulate the results
        #
        acc_avg[i] += avg
        acc_std[i] += std

    print ""

# normalize
#
acc_avg[0:num_channels] /= num_files
acc_std[0:num_channels] /= num_files

# summarize the processing status
#
print 'total number of files processed = %d' % num_files

# save the averages to a file
#
numpy.savetxt(sys.argv[1], (acc_avg, acc_std), fmt='%f')

###############################################################################
#
# the main program ends here
#
###############################################################################
