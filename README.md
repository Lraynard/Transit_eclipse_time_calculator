# Transit_eclipse_time_calculator
Script to predict future transit and eclipse times using known:
    period, epoch, duration

Dependencies: astropy fitsio pyplot numpy prettytable datetime

To predict transits/eclipses, edit the following lines of the get_times.py script and run:

#Object properties
period = 1.2345678      # days
epoch = 2457765.1234567     # JD/HJD/BJD
width = 1.23456         # hours

#Observing period
obs_start   = "2018-01-24T12:00:00" # UTC
obs_end     = "2018-02-07T12:00:00" # UTC
utc_offset = +2 # offset from UTC to LT in hours
