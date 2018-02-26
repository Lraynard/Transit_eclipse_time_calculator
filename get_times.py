import sys
sys.path.append('/home/sw/anaconda.bak/lib/python2.7/site-packages')
import numpy as np
from fitsio import FITS
from astropy.table import Table
import datetime
from astropy import time, coordinates as coord, units as u
from prettytable import *

def NGTS_orion_to_HJD(NGTS_orion_date):
    hjd_0 = 2450000.000000 # 1995-10-09 12:00:00.00 converted to JD
    return NGTS_orion_date + hjd_0

def obs_window(start, end):
    obs_times = [start, end]
    obs_window = time.Time(obs_times, format='isot', scale='utc')
    obs_window = obs_window.jd
    return obs_window

def observable_transits(period, epoch, width, obs_window, utc_offset):
    transit = epoch
    times = [transit]
    num = [1]
    kind = []
    while transit < obs_window[1]:
        num.append(num[-1] +1)
        transit += period
        times.append(transit)
    num = np.asarray(num)
    num = num[(times > obs_window[0]) & (times < obs_window[1])]
    for i in num:
        if i % 2 == 0:
            kind.append("even")
        else:
            kind.append("odd")
    times = [i for i in times if i > obs_window[0] and i < obs_window[1]]
    times = np.asarray(times) + utc_offset/24.0
    ingress = times - 0.5*width/24.0
    egress = times + 0.5*width/24.0
    times = time.Time(times, format='jd', scale='utc', out_subfmt='date_hm').iso
    ingress = time.Time(ingress, format='jd', scale='utc',
            out_subfmt='date_hm').iso
    egress = time.Time(egress, format='jd', scale='utc',
            out_subfmt='date_hm').iso
    t = PrettyTable()
    t.add_column("ingress (LT)", ingress)
    t.add_column("mid_transit (LT)", times)
    t.add_column("egress (LT)", egress)
    t.add_column("Odd/even", kind)
    return t

########################################

#Object properties
period = 1.2345678       # days
epoch = 7765.1234567     # Orion format (without 245)
width = 1.23456          # hours

#Observing period
obs_start   = "2018-01-24T12:00:00" # UTC
obs_end     = "2018-02-07T12:00:00" # UTC
utc_offset = +2 # offset from UTC to LT in hours

#########################################

#Conversions
epoch = NGTS_orion_to_HJD(epoch)

#Get observing window in JD
window = obs_window(obs_start, obs_end)

#Get transit times
try:
    times = observable_transits(period, epoch, width, window, utc_offset)
except:
    times = ''
try:
    secondary_times =  observable_transits(period, epoch+0.5*period, width, window,
        utc_offset)
except:
    secondary_times = ''

#Print times
print "period (days): %s" %period
print "epoch (HJD): %s" %epoch
print "width (hours): %s" %width
print "\nPRIMARY transit times UTC+%s hr:" %utc_offset
print times
print "\nSECONDARY transit times UTC+%s hr:" %utc_offset
print secondary_times
