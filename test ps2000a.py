from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import time
from picoscope import ps2000a
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pandas as pd

class Trigger:

    def trigger_tx(self):

        print("Attempting to open Picoscope 2000A...")

        # Uncomment this line to use with the 2000a/2000b series
        ps = ps2000a.PS2000a()

        print("Found the following picoscope:")
        print(ps.getAllUnitInfo())

        waveform_desired_duration = 7E-3 #change waveform desired duration to set the frequency of the wave
        obs_duration = 3 * waveform_desired_duration
        sampling_interval = obs_duration / 4096

        (actualSamplingInterval, nSamples, maxSamples) = \
            ps.setSamplingInterval(sampling_interval, obs_duration)
        print("Sampling interval = %f ns" % (actualSamplingInterval * 1E9))
        print("Taking  samples = %d" % nSamples)
        print("Maximum samples = %d" % maxSamples)

        waveformAmplitude = 2.0
        waveformOffset = 0
        # x = np.linspace(-1, 1, num=ps.AWGMaxSamples, endpoint=False)

        freq = 110000
        fs = int(2*freq) # sample rate
        t = np.linspace(0, 3, 1000, endpoint = False)

        # waveformAmplitude = 5
        # waveformOffset = 0
        # # x = np.sin(np.linspace(-1, 1, num=ps.AWGMaxSamples, endpoint=False, retstep=True))

        noise1 = 0
        noise2 = 0.01*np.sin(2*np.pi * 0.1*t) + 0.01*np.sin(2*np.pi * 1.8*t) + 0.01*np.sin(2*np.pi * 0.4*t)

        realSignal = 2*np.sin(2*np.pi* t)
        sig = noise1

        sig = np.append(sig, [realSignal, noise2, realSignal, noise1*noise2])
        print("signal=", sig)

        (waveform_duration, deltaPhase) = ps.setAWGSimple(
            sig, waveform_desired_duration, offsetVoltage=0.0,
            indexMode="Single", triggerSource='None')

        # the setChannel command will chose the next largest amplitude
        # BWLimited = 1 for 6402/6403, 2 for 6404, 0 for all
        channelARange = ps.setChannel('A', 'DC', waveformAmplitude, 0.0,
                                    enabled=True, BWLimited=False)
        channelBRange = ps.setChannel('B', 'DC', waveformAmplitude, 0.0,
                                    enabled=True, BWLimited=False)

        print("Chosen channel range = %d" % channelARange)

        ps.setSimpleTrigger('A', 1.0, 'Falling', delay=0, timeout_ms=100,
                            enabled=True)
        # ps.setSimpleTrigger('B', 1.0, 'Falling', delay=0, timeout_ms=100,
        #                     enabled=True)

        ps.runBlock()
        ps.waitReady()
        print("Waiting for awg to settle.")
        time.sleep(2.0)
        ps.runBlock()
        ps.waitReady()
        print("Done waiting for trigger")
        self.adc2mVChAMax = ps.getDataV('A', nSamples, returnOverflow=False)
        self.adc2mVChBMax = ps.getDataV('B', nSamples, returnOverflow=False)

        self.time = np.arange(nSamples) * actualSamplingInterval

        ps.stop()
        ps.close()

        plt.plot(self.time, self.adc2mVChAMax, label="Tx")
        plt.plot(self.time,self.adc2mVChBMax, label="Rx")
        plt.title("Picoscope 2000A waveforms")
        plt.ylabel("Voltage (V)")
        plt.xlabel("Time (ms)")
        plt.legend()
        plt.show()

    def find_freq(self):
        # print("ChA=",self.adc2mVChAMax)
        # print("ChB=",self.adc2mVChBMax)
        # print(type(self.adc2mVChAMax))

        self.dict2csv = {"Time(ms)": self.time, "Voltage(V) Channel A": self.adc2mVChAMax}

        self.df = pd.DataFrame(self.dict2csv)

        time_ls =[]
        for i in range (0,len(self.df)):
            volt = self.df.iloc[i][1]
            print(volt)
            if volt > 1.9: #change accordingly
                if self.df.iloc[i][1] > self.df.iloc[i-1][1]:
                    if self.df.iloc[i][1] >= self.df.iloc[i+1][1]:
                        get_time = self.df.iloc[i][0]
                        time_ls.append(get_time)
                else:
                    None

        print(time_ls)
        # if (time_ls[1] - time_ls[0])<0.01:
        freq = 1/((time_ls[1] - time_ls[0])*1E-3)
        # else:
        #     freq = 1/((time_ls[2] - time_ls[1])*1E-3)
        print ("Frequency(MHz)=", freq/1E6)

trigger = Trigger()
trigger.trigger_tx()
trigger.find_freq()
