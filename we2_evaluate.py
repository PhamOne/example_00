# file: we2_evaluate.py
#
# This python script loads two models, loops over a set of EDF files,
# and recognizes them.
#
# Usage:
#  python we2_evaluate.py r_model.txt b_model.txt data_all.list
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
fnames = open(sys.argv[3]).read().splitlines()

# load the model files
#
model_r = numpy.loadtxt(sys.argv[1])
model_b = numpy.loadtxt(sys.argv[2])

# loop over all the input files:
#  note that the first two arguments are the model files
#
errs = numpy.zeros((2, 2));

for inputfile in fnames:

    # load the edf data
    #
    signal, srate, phys_chan, time, tmp = edfplus.load_edf(inputfile)

    # reduce the signal to a vector of means and stdevs
    #
    num_channels = len(model_r[0]);
    test_avg = numpy.zeros(num_channels)
    test_std = numpy.zeros(num_channels)
    first_channel = 2
    last_channel = 15
    for i in range(first_channel, last_channel + 1):
        test_avg[i] = numpy.mean(signal[i])
        test_std[i] = numpy.std(signal[i])

    # compare to each model
    #
    error_r = numpy.linalg.norm(model_r[0] - test_avg) +\
        numpy.linalg.norm(model_r[1] - test_std);
    error_b = numpy.linalg.norm(model_b[0] - test_avg) +\
        numpy.linalg.norm(model_b[1] - test_std);


    # output the scores
    #
    print '%s: relaxed = %8.2f\tbusy = %8.2f' % (inputfile, error_r, error_b)

    # tabulate errors
    #
    if 'r_' in inputfile:
        if error_r < error_b:
            errs[0][0] += 1
            print ' --> correct choice (relaxed)'
        else:
            errs[0][1] += 1
            print ' **> incorrect choice (busy vs. relaxed)'
    elif 'b_' in inputfile:
        if error_b < error_r:
            errs[1][1] += 1
            print ' --> correct choice (busy)'
        else:
            errs[1][0] += 1
            print ' **> incorrect choice (relaxed vs. busy)'
    else:
        print ' ??> incorrect filename format'

# compute some statistics
#
p_errs = numpy.zeros((2, 2));
p_errs[0][0] = errs[0][0] / (errs[0][0] + errs[0][1]) * 100.0
p_errs[0][1] = errs[0][1] / (errs[0][0] + errs[0][1]) * 100.0
p_errs[1][0] = errs[1][0] / (errs[1][0] + errs[1][1]) * 100.0
p_errs[1][1] = errs[1][1] / (errs[1][0] + errs[1][1]) * 100.0

# print a summary
#
print ' '
print '                    GUESS:'
print 'TRUTH:      relaxed         busy'
print ' relaxed: %5.1f (%2d/%2d) %5.1f (%2d/%2d)' % \
    (p_errs[0][0], errs[0][0], errs[0][0] + errs[0][1], \
     p_errs[0][1], errs[0][1], errs[0][0] + errs[0][1])
print '    busy: %5.1f (%2d/%2d) %5.1f (%2d/%2d)' % \
    (p_errs[1][0], errs[1][0], errs[1][0] + errs[1][1], \
     p_errs[1][1], errs[1][1], errs[1][0] + errs[1][1])

###############################################################################
#
# the main program ends here
#
###############################################################################
