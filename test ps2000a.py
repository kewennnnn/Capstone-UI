from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import time
# from picoscope import ps2000
from picoscope import ps2000a
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pandas as pd
from FreqMeasure import freqMeasure

if __name__ == "__main__":
    print(__doc__)

    print("Attempting to open Picoscope 2000...")

    # ps = ps2000.PS2000()
    # Uncomment this line to use with the 2000a/2000b series
    ps = ps2000a.PS2000a()

    print("Found the following picoscope:")
    print(ps.getAllUnitInfo())

    waveform_desired_duration = 1E-5 #change waveform desired duration to set the frequency of the wave
    obs_duration = 3 * waveform_desired_duration
    sampling_interval = obs_duration / 4096

    (actualSamplingInterval, nSamples, maxSamples) = \
        ps.setSamplingInterval(sampling_interval, obs_duration)
    print("Sampling interval = %f ns" % (actualSamplingInterval * 1E9))
    print("Taking  samples = %d" % nSamples)
    print("Maximum samples = %d" % maxSamples)

    waveformAmplitude = 1.5
    waveformOffset = 0
    # x = np.linspace(-1, 1, num=ps.AWGMaxSamples, endpoint=False)
    # # generate an interesting looking waveform
    # waveform = waveformOffset + (x / 2 + (x ** 2) / 2) * waveformAmplitude
    
    freq = 110000
    fs = int(2*freq) # sample rate
    t = np.linspace(0, 3, 1000, endpoint = False)

    # fm.openScope()

    # try:
    #     while 1:
    #         fm.armMeasure()
    #         fm.measure()
    # except KeyboardInterrupt:
    #     pass

    # fm.closeScope()

    # waveformAmplitude = 5
    # waveformOffset = 0
    # # x = np.sin(np.linspace(-1, 1, num=ps.AWGMaxSamples, endpoint=False, retstep=True))

    # t = np.linspace(0, 3, 1000, endpoint=False)

    # x = np.linspace(-1, 1, num=ps.AWGMaxSamples, endpoint=False)

    # pwm = signal.square(1*t, duty=0.08)

    # print ("pwm vals=",pwm)
    # print("length of pwm", len(pwm))is 1000
    # pwm = signal.square(2 * np.pi * 200 * t)
    # value = pwm*sig
    # pwm = signal.unit_impulse(100)
    # b, a = signal.butter (4,0.5)
    # response = signal.lfilter(b, a, pwm)

    # generate an interesting looking waveform
    # waveform = waveformOffset + (x / 2 + (x ** 2) / 2) * waveformAmplitude

    # waveform = waveformOffset + np.sin(20*t) * waveformAmplitude

    noise1 = 0
    noise2 = 0.01*np.sin(2*np.pi * 0.1*t) + 0.01*np.sin(2*np.pi * 1.8*t) + 0.01*np.sin(2*np.pi * 0.4*t)

    realSignal = 2*np.sin(2*np.pi* t)
    sig = noise1

    sig = np.append(sig, [realSignal, noise2, realSignal, noise1*noise2])
    print("signal=", sig)

    # sig = np.sin(2 * np.pi * t)
    # pwm = signal.square(2 * np.pi * 2 * t, duty=(sig+1)/2)

    #must be a numpy array

    #create wave from CSV file but cannot convert NaN into integer
    # save_as_csv = pd.DataFrame(waveform).to_csv("C:/Users/Charis/Downloads/waveform_test.csv")
    # waveform = np.genfromtxt("C:/Users/Charis/Downloads/waveform_test.csv", delimiter=";")

    # print("waveform vals=", waveform)
    # print(len(waveform)) is 1000
    # k_ls = np.array([], dtype = np.int16)
    # for i in waveform:
    #     print("i")
    #     for j in pwm:
    #         k = i*j
    #         print("k")
    #         k_ls = np.append(k_ls, k)
    # print("done")

    # print(k_ls) 

    # print("Waveformtype=",type(waveform))
    # waveform_arr = np.asarray(k_ls)

    (waveform_duration, deltaPhase) = ps.setAWGSimple(
        sig, waveform_desired_duration, offsetVoltage=0.0,
        indexMode="Single", triggerSource='None')

    # the setChannel command will chose the next largest amplitude
    # BWLimited = 1 for 6402/6403, 2 for 6404, 0 for all
    channelRange = ps.setChannel('A', 'DC', waveformAmplitude, 0.0,
                                 enabled=True, BWLimited=False)

    print("Chosen channel range = %d" % channelRange)

    ps.setSimpleTrigger('A', 1.0, 'Falling', delay=0, timeout_ms=100,
                        enabled=True)
    # ps.setSimpleTrigger('TriggerAux', 0.0, 'Falling', delay=0,
    #                     timeout_ms=100, enabled=True)

    ps.runBlock()
    ps.waitReady()
    print("Waiting for awg to settle.")
    time.sleep(2.0)
    ps.runBlock()
    ps.waitReady()
    print("Done waiting for trigger")
    dataA = ps.getDataV('A', nSamples, returnOverflow=False)
    dataA_1 = ps.getDataV('A', nSamples, returnOverflow=False)
    fm = freqMeasure()
    dataA_1 = dataA_1 - np.mean(dataA_1)
    freq = fm.freq_from_crossings(dataA_1)
    print("Freqency=", freq)

    dataTimeAxis = np.arange(nSamples) * actualSamplingInterval

    ps.stop()
    ps.close()

    # plt.figure()
    # plt.hold(True)
    plt.plot(dataTimeAxis, dataA, label="Clock")
    # plt.grid(True, which='major')
    plt.title("Picoscope 2000 waveforms")
    plt.ylabel("Voltage (V)")
    plt.xlabel("Time (ms)")
    plt.legend()
    plt.show()