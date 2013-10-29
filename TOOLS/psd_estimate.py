# Utility for plotting power spectral density of a time series by using scipy's welch function :)

import obspy as obs
from scipy.signal import welch
import matplotlib.pyplot as plt
import numpy as np


def plot_psd(input, numwin, input2=None):
    
    if type(input)==str:
        trace1=obs.read(input)[0]
    else:
        trace1=input
    
    if input2 is not None:
        if type(input2)==str:
            trace2=obs.read(input2)[0]
        else:
            trace2=input2
        
    
    freq1, psd1=get_psd(trace1, numwin)
    
    
    if input2 is not None:
        freq2, psd2=get_psd(trace2, numwin)
        # Two subplots, the axes array is 1-d
        f, axarr = plt.subplots(2, sharex=True)
        axarr[0].loglog(freq1, np.sqrt(psd1))
        axarr[0].set_title('Power spectral densities')
        plt.xlabel('frequency [Hz]')
        plt.ylabel('Linear spectrum [V RMS]')
        axarr[1].loglog(freq2, np.sqrt(psd2))
        plt.show()
    else:
        plt.figure()
        plt.loglog(freq1, np.sqrt(psd1))
        plt.xlabel('frequency [Hz]')
        plt.ylabel('Linear spectrum [V RMS]')
        plt.show()
    
    
    

def get_psd(trace, numwin):
    trace.detrend('linear')
    trace.detrend('demean')
    fs=trace.stats.sampling_rate
    win_len=round(len(trace.data)/numwin)
    win_len=wl_adjust(win_len, fs)
    freq, psd=welch(trace.data, fs, window='hanning', nperseg=win_len, noverlap=None, nfft=None, detrend='constant', return_onesided=True, scaling='spectrum', axis=-1)
    return freq,  psd
    
    


#==================================================================================================
# Adjust window lenght to be power of 2
#==================================================================================================
"""Get the nearest power of two in terms of samples; then determine the corresponding window length in seconds. 
win_len: Integer, User-defined window length in seconds
Fs: Integer, Sampling rate """
from math import ceil,  log

def wl_adjust(win_len, Fs):
    
    #current window length
    cwl=Fs*win_len;
    nwl=int((2**ceil(log(cwl)/log(2)))/Fs)
   
    return nwl