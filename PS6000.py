# from argparse import ONE_OR_MORE
import ctypes
from datetime import date
# from tracemalloc import start
# from turtle import shearfactor
# from webbrowser import get
import numpy as np
from picosdk.ps2000a import ps2000a as ps
from picoscope import ps2000a 
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
import time
import pandas as pd
# from Tx import Tx
# from numpy.fft import fft, fftfreq, irfft
from scipy import fftpack
from scipy import signal
from time import sleep
import math

class PS6000:

    def open_ps2000a(self):

        # with ps.open_unit() as device:
        #     print('Device info: {}'.format(device.info))

        # This example opens a 2000a driver device, sets up two channels and a trigger then collects a block of data.
        # This data is then plotted as mV against time in ns.

        # Create chandle and status ready for use
        self.chandle = ctypes.c_int16()
        self.status = {}

        # Open 2000 series PicoScope
        # Returns handle to chandle for use in future API functions
        self.status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(self.chandle), None)

        try:
            assert_pico_ok(self.status["openunit"])
        except:
            # powerstate becomes the status number of openunit
            powerstate = self.status["openunit"]

            # If powerstate is the same as 282 then it will run this if statement
            if powerstate == 282:
                # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
                self.status["ChangePowerSource"] = ps.ps2000aChangePowerSource(self.chandle, 282)
            # If the powerstate is the same as 286 then it will run this if statement
            elif powerstate == 286:
                # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
                self.status["ChangePowerSource"] = ps.ps2000aChangePowerSource(self.chandle, 286)
            else:
                raise

            assert_pico_ok(self.status["ChangePowerSource"])
        assert_pico_ok(self.status["openunit"])

    # def open_ps2000a(self):

    #     print("Attempting to open Picoscope 2000A...")

    #     # Uncomment this line to use with the 2000a/2000b series
    #     self.ps = ps2000a.PS2000a()

    #     print("Found the following picoscope:")
    #     print(self.ps.getAllUnitInfo())

    def block_run(self):
        chARange = 7
        self.status["setChA"] = ps.ps2000aSetChannel(self.chandle, 0, 1, 1, chARange, 0)
        assert_pico_ok(self.status["setChA"])

        # Set up channel B
        # handle = chandle
        # channel = PS2000A_CHANNEL_B = 1
        # enabled = 1
        # coupling type = PS2000A_DC = 1
        # range = PS2000A_2V = 7
        # analogue offset = 0 V
        chBRange = 7
        self.status["setChB"] = ps.ps2000aSetChannel(self.chandle, 1, 1, 1, chBRange, 0)
        assert_pico_ok(self.status["setChB"])

        wavetype = ctypes.c_int16(0)
        sweepType = ctypes.c_int32(0)
        triggertype = ctypes.c_int32(0)
        triggerSource = ctypes.c_int32(0)

        #commented out for test
        # status["SetSigGenBuiltIn"] = ps.ps2000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 1000000, 1000000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
        # assert_pico_ok(status["SetSigGenBuiltIn"])

        # Pauses the script to show signal
        time.sleep(10)

        # Set number of pre and post trigger samples to be collected
        preTriggerSamples = 3
        postTriggerSamples = 500
        totalSamples = preTriggerSamples + postTriggerSamples

        # Get timebase information
        # WARNING: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
        # To access these Timebases, set any unused analogue channels to off.
        # handle = chandle
        # timebase = 8 = timebase
        # noSamples = totalSamples
        # pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalNs)
        # pointer to totalSamples = ctypes.byref(returnedMaxSamples)
        # segment index = 0
        timebase = 8
        timeIntervalns = ctypes.c_float()
        returnedMaxSamples = ctypes.c_int32()
        oversample = ctypes.c_int16(0)
        self.status["getTimebase2"] = ps.ps2000aGetTimebase2(self.chandle,
                                                        timebase,
                                                        totalSamples,
                                                        ctypes.byref(timeIntervalns),
                                                        oversample,
                                                        ctypes.byref(returnedMaxSamples),
                                                        0)
        assert_pico_ok(self.status["getTimebase2"])

        # Run block capture
        # handle = chandle
        # number of pre-trigger samples = preTriggerSamples
        # number of post-trigger samples = PostTriggerSamples
        # timebase = 8 = 80 ns = timebase (see Programmer's guide for mre information on timebases)
        # oversample = 0 = oversample
        # time indisposed ms = None (not needed in the example)
        # segment index = 0
        # lpReady = None (using ps2000aIsReady rather than ps2000aBlockReady)
        # pParameter = None
        self.status["runBlock"] = ps.ps2000aRunBlock(self.chandle,
                                                preTriggerSamples,
                                                postTriggerSamples,
                                                timebase,
                                                oversample,
                                                None,
                                                0,
                                                None,
                                                None)
        assert_pico_ok(self.status["runBlock"])

        # Check for data collection to finish using ps2000aIsReady
        ready = ctypes.c_int16(0)
        check = ctypes.c_int16(0)
        while ready.value == check.value:
            self.status["isReady"] = ps.ps2000aIsReady(self.chandle, ctypes.byref(ready))

        # Create buffers ready for assigning pointers for data collection
        bufferAMax = (ctypes.c_int16 * totalSamples)()
        bufferAMin = (ctypes.c_int16 * totalSamples)() # used for downsampling which isn't in the scope of this example
        bufferBMax = (ctypes.c_int16 * totalSamples)()
        bufferBMin = (ctypes.c_int16 * totalSamples)() # used for downsampling which isn't in the scope of this example

        # Set data buffer location for data collection from channel A
        # handle = chandle
        # source = PS2000A_CHANNEL_A = 0
        # pointer to buffer max = ctypes.byref(bufferDPort0Max)
        # pointer to buffer min = ctypes.byref(bufferDPort0Min)
        # buffer length = totalSamples
        # segment index = 0
        # ratio mode = PS2000A_RATIO_MODE_NONE = 0
        self.status["setDataBuffersA"] = ps.ps2000aSetDataBuffers(self.chandle,
                                                            0,
                                                            ctypes.byref(bufferAMax),
                                                            ctypes.byref(bufferAMin),
                                                            totalSamples,
                                                            0,
                                                            0)
        assert_pico_ok(self.status["setDataBuffersA"])

        # Set data buffer location for data collection from channel B
        # handle = chandle
        # source = PS2000A_CHANNEL_B = 1
        # pointer to buffer max = ctypes.byref(bufferBMax)
        # pointer to buffer min = ctypes.byref(bufferBMin)
        # buffer length = totalSamples
        # segment index = 0
        # ratio mode = PS2000A_RATIO_MODE_NONE = 0

        self.status["setDataBuffersB"] = ps.ps2000aSetDataBuffers(self.chandle,
                                                            1,
                                                            ctypes.byref(bufferBMax),
                                                            ctypes.byref(bufferBMin),
                                                            totalSamples,
                                                            0,
                                                            0)
        assert_pico_ok(self.status["setDataBuffersB"])

        # Create overflow location
        overflow = ctypes.c_int16()
        # create converted type totalSamples
        cTotalSamples = ctypes.c_int32(totalSamples)

        # Retried data from scope to buffers assigned above
        # handle = chandle
        # start index = 0
        # pointer to number of samples = ctypes.byref(cTotalSamples)
        # downsample ratio = 0
        # downsample ratio mode = PS2000A_RATIO_MODE_NONE
        # pointer to overflow = ctypes.byref(overflow))
        self.status["getValues"] = ps.ps2000aGetValues(self.chandle, 0, ctypes.byref(cTotalSamples), 0, 0, 0, ctypes.byref(overflow))
        assert_pico_ok(self.status["getValues"])


        # find maximum ADC count value
        # handle = chandle
        # pointer to value = ctypes.byref(maxADC)
        maxADC = ctypes.c_int16()
        self.status["maximumValue"] = ps.ps2000aMaximumValue(self.chandle, ctypes.byref(maxADC))
        assert_pico_ok(self.status["maximumValue"])

        # convert ADC counts data to mV
        self.adc2mVChAMax =  adc2mV(bufferAMax, chARange, maxADC)
        # self.adc2mVSigGen = adc2mV()
        # self.adc2mVChAMax_ls =[]

        # for i in self.adc2mVChAMax:
        #     i = i/1000
        #     self.adc2mVChAMax_ls.append(i)

        print("channel A (in mV) =", self.adc2mVChAMax)

        self.adc2mVChBMax =  adc2mV(bufferBMax, chBRange, maxADC)

        # self.adc2mVChBMax_ls =[]

        # for i in self.adc2mVChBMax:
        #     i = i/1000
        #     self.adc2mVChAMax_ls.append(i)

        print("channel B (in mV) =", self.adc2mVChBMax)

        # Create time data
        ed_time = np.linspace(0, ((cTotalSamples.value)-1) * timeIntervalns.value, cTotalSamples.value)

        # plot data from channel A and signalgen
        # plt.plot(self.time, self.adc2mVChAMax[:])
        plt.plot(ed_time, self.adc2mVChBMax, label ="rx")
        plt.plot(ed_time, self.adc2mVChAMax, label ="tx")
        plt.xlabel('Time (ns)')
        plt.ylabel('Voltage (mV)')
        plt.show()

        # Stop the scope
        # handle = chandle
        self.status["stop"] = ps.ps2000aStop(self.chandle)
        assert_pico_ok(self.status["stop"])

        # Close unitDisconnect the scope
        # handle = chandle
        self.status["close"] = ps.ps2000aCloseUnit(self.chandle)
        assert_pico_ok(self.status["close"])

        # display status returns
        print(self.status)

    def block_example(self):

        # # This example opens a 2000a driver device, sets up two channels and a trigger then collects a block of data.
        # # This data is then plotted as mV against time in ns.

        # # Create chandle and status ready for use
        # self.chandle = ctypes.c_int16()
        # self.status = {}

        # # Open 2000 series PicoScope
        # # Returns handle to chandle for use in future API functions
        # status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)

        # try:
        #     assert_pico_ok(self.status["openunit"])
        # except:
        #     # powerstate becomes the status number of openunit
        #     powerstate = self.status["openunit"]

        #     # If powerstate is the same as 282 then it will run this if statement
        #     if powerstate == 282:
        #         # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
        #         self.status["ChangePowerSource"] = ps.ps2000aChangePowerSource(self.chandle, 282)
        #     # If the powerstate is the same as 286 then it will run this if statement
        #     elif powerstate == 286:
        #         # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
        #         self.status["ChangePowerSource"] = ps.ps2000aChangePowerSource(self.chandle, 286)
        #     else:
        #         raise

        #     assert_pico_ok(self.status["ChangePowerSource"])
        # assert_pico_ok(self.status["openunit"])

        # Set up channel A
        # handle = chandle
        # channel = PS2000A_CHANNEL_A = 0
        # enabled = 1
        # coupling type = PS2000A_DC = 1
        # range = PS2000A_2V = 7
        # analogue offset = 0 V

        # ps_2 = ps2000a.PS2000a()

        chARange = 7
        self.status["setChA"] = ps.ps2000aSetChannel(self.chandle, 0, 1, 1, chARange, 0)
        assert_pico_ok(self.status["setChA"])

        # Set up channel B
        # handle = chandle
        # channel = PS2000A_CHANNEL_B = 1
        # enabled = 1
        # coupling type = PS2000A_DC = 1
        # range = PS2000A_2V = 7
        # analogue offset = 0 V
        chBRange = 7
        self.status["setChB"] = ps.ps2000aSetChannel(self.chandle, 1, 1, 1, chBRange, 0)
        assert_pico_ok(self.status["setChB"])

        wavetype = ctypes.c_int16(0)
        sweepType = ctypes.c_int32(0)
        triggertype = ctypes.c_int32(0)
        triggerSource = ctypes.c_int32(0)

        # Set up single trigger
        # handle = chandle
        # enabled = 1
        # source = PS2000A_CHANNEL_A = 0
        # threshold = 1024 ADC counts
        # direction = PS2000A_RISING = 2
        # delay = 0 s
        # auto Trigger = 1000 ms

        # self.status["trigger"] = ps.ps2000aSetSimpleTrigger(self.chandle, 1, 0, 1024, 2, 0, 1000)
        # assert_pico_ok(self.status["trigger"])

        # self.status["signalgen"] = ps.ps2000aSetSigGenBuiltIn(self.chandle, 20, 50, 0, 1000, 1200, 0, 20, PS2000A_UP, PS2000A_ES_OFF, 1, 0, PS2000A_SIGGEN_GATE_HIGH, PS2000A_SIGGEN_NONE, 0)
        # assert_pico_ok(self.status["signalgen"])

        # status["startsignalgen"] = ps.ps2000aSigGenSoftwareControl(chandle, 0)
        # assert_pico_ok(status["startsignalgen"])
    
        # status["stopsignalgen"] = ps.ps2000aSigGenSoftwareControl(chandle, 1)
        # assert_pico_ok(status["stopsignalgen"])

        # Output a sine wave with peak-to-peak voltage of 2 V and frequency of 10 kHz
        # handle = chandle
        # offsetVoltage = 0
        # pkToPk = 2000000
        # waveType = ctypes.c_int16(0) = PS2000A_SINE
        # startFrequency = 10 kHz
        # stopFrequency = 10 kHz
        # increment = 0
        # dwellTime = 1
        # sweepType = ctypes.c_int16(1) = PS2000A_UP
        # operation = 0
        # shots = 0
        # sweeps = 0
        # triggerType = ctypes.c_int16(0) = PS2000A_SIGGEN_RISING
        # triggerSource = ctypes.c_int16(0) = PS2000A_SIGGEN_NONE
        # extInThreshold = 1
        # wavetype = ctypes.c_int16(0)
        # sweepType = ctypes.c_int32(1)
        # triggertype = ctypes.c_int32(0)
        # triggerSource = ctypes.c_int32(0)
        # indexMode = ctypes.c_int32(0)
        # print(indexMode)
        # startDeltaPhase = 0
        # stopDeltaPhase = startDeltaPhase
        # # arbitraryWaveformSize = ps.ps2000aSigGenArbitraryMinMaxValues(self.chandle, 0, 0, 0, 0)
        # # create a custom waveform
        # awgBuffer = np.sin(np.linspace(0,2*math.pi,1024))
        # awgbufferPointer = awgBuffer.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        # arbitaryWaveform = awgbufferPointer
        # arbitraryWaveformSize = 1024

        # self.status["SetSigGenBuiltIn"] = ps.ps2000aSetSigGenBuiltIn(self.chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
        # assert_pico_ok(self.status["SetSigGenBuiltIn"])

        # t = np.linspace(0, 3, 1000, endpoint = False)
        # noise1 = 0
        # noise2 = 0.01*np.sin(2*np.pi * 0.1*t) + 0.01*np.sin(2*np.pi * 1.8*t) + 0.01*np.sin(2*np.pi * 0.4*t)

        # realSignal = 2*np.sin(2*np.pi* t)
        # sig = noise1

        # sig = np.append(sig, [realSignal, noise2, realSignal, noise1*noise2])

        # waveform = np.array(sig, dtype=np.int16)

        # phase = ctypes.c_uint32()
        # #get the start & stop DeltaPhase values for the SetSig function.
        # phase = ps.ps2000aSigGenFrequencyToPhase(self.chandle, 1650000, 0, len(waveform), ctypes.byref(phase))

        # offsetVoltage = 0
        # pkToPk = ctypes.c_uint32(int(2000000 * 1E6))
        # startDeltaPhase = phase
        # stopDeltaPhase = phase
        # deltaPhaseIncrement = ctypes.c_uint32(0) #0
        # dwellCount = ctypes.c_uint32(0) #0
        # arbitraryWaveform = waveform.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        # arbitraryWaveformSize = ctypes.c_int32(len(waveform)) #len(waveform)
        # sweepType = 0
        # operation = 0
        # indexMode = 0
        # pulses = 3
        # shots = ctypes.c_uint32(3) #ctypes.c_uint32(pulses)
        # sweeps = ctypes.c_uint32(0) #ctypes.c_uint32(1)
        # triggerType = 0
        # triggerSource = 3
        # extInThreshold = ctypes.c_int16(0) #0

        # # self.status["trigger"] = ps.ps2000aSetSimpleTrigger(self.chandle, 1, 0, 1024, 2, 0, 1000)
        # # assert_pico_ok(self.status["trigger"])

        # ret = ps.ps2000aSetSigGenArbitrary(
        #                                     self.chandle,
        #                                     offsetVoltage,
        #                                     pkToPk, 
        #                                     startDeltaPhase,
        #                                     stopDeltaPhase,
        #                                     deltaPhaseIncrement,
        #                                     dwellCount,
        #                                     arbitraryWaveform,
        #                                     arbitraryWaveformSize,
        #                                     sweepType,
        #                                     operation,
        #                                     indexMode, 
        #                                     shots, 
        #                                     sweeps,
        #                                     triggerType,
        #                                     triggerSource,
        #                                     extInThreshold)

        # self.status["startsignalgen"] = ps.ps2000aSigGenSoftwareControl(self.chandle, 1)

        # self.status["startsignalgen"] = ps.ps2000aSigGenSoftwareControl(self.chandle, 0)

        #set pulse transmit here

        # Output a sine wave with peak-to-peak voltage of 2 V and frequency of 10 kHz
        # handle = chandle
        # offsetVoltage = 0
        # pkToPk = 2000000
        # waveType = ctypes.c_int16(0) = PS2000A_SINE
        # startFrequency = 10 kHz
        # stopFrequency = 10 kHz
        # increment = 0
        # dwellTime = 1
        # sweepType = ctypes.c_int16(1) = PS2000A_UP
        # operation = 0
        # shots = 0
        # sweeps = 0
        # triggerType = ctypes.c_int16(0) = PS2000A_SIGGEN_RISING
        # triggerSource = ctypes.c_int16(0) = PS2000A_SIGGEN_NONE
        # extInThreshold = 1
        # wavetype = ctypes.c_int16(0) #square
        # sweepType = ctypes.c_int32(0)
        # triggertype = ctypes.c_int32(0)
        # triggerSource = ctypes.c_int32(0)

        # self.status["SetSigGenBuiltIn"] = ps.ps2000aSetSigGenBuiltIn(self.chandle, 0, 2000000, wavetype, 1000000, 1000000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
        # self.status["SetSigGenArb"] = ps.ps2000aSetSigGenArbitrary(self.chandle, 0,2000000,0, 0, 0,0  )
        # assert_pico_ok(self.status["SetSigGenBuiltIn"])

        # waveform_desired_duration = 1E-5 #change waveform desired duration to set the frequency of the wave
        # obs_duration = 3 * waveform_desired_duration
        # sampling_interval = obs_duration / 4096

        # (actualSamplingInterval, nSamples, maxSamples) = \
        #     ps_2.setSamplingInterval(sampling_interval, obs_duration)
        # print("Sampling interval = %f ns" % (actualSamplingInterval * 1E9))
        # print("Taking  samples = %d" % nSamples)
        # print("Maximum samples = %d" % maxSamples)

        # waveformAmplitude = 1.5
        # waveformOffset = 0
        
        # freq = 110000
        # fs = int(2*freq) # sample rate
        # t = np.linspace(0, 3, 1000, endpoint = False)

        # noise1 = 0
        # noise2 = 0.01*np.sin(2*np.pi * 0.1*t) + 0.01*np.sin(2*np.pi * 1.8*t) + 0.01*np.sin(2*np.pi * 0.4*t)

        # realSignal = 2*np.sin(2*np.pi* t)
        # sig = noise1

        # sig = np.append(sig, [realSignal, noise2, realSignal, noise1*noise2])

        # (waveform_duration, deltaPhase) = ps_2.setAWGSimple(
        # sig, waveform_desired_duration, offsetVoltage=0.0,
        # indexMode="Single", triggerSource='None')

        # Pauses the script to show signal
        time.sleep(10)

        # Set number of pre and post trigger samples to be collected
        preTriggerSamples = 3
        postTriggerSamples = 500
        totalSamples = preTriggerSamples + postTriggerSamples

        # Get timebase information
        # WARNING: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
        # To access these Timebases, set any unused analogue channels to off.
        # handle = chandle
        # timebase = 8 = timebase
        # noSamples = totalSamples
        # pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalNs)
        # pointer to totalSamples = ctypes.byref(returnedMaxSamples)
        # segment index = 0
        timebase = 8
        timeIntervalns = ctypes.c_float()
        returnedMaxSamples = ctypes.c_int32()
        oversample = ctypes.c_int16(0)
        self.status["getTimebase2"] = ps.ps2000aGetTimebase2(self.chandle,
                                                        timebase,
                                                        totalSamples,
                                                        ctypes.byref(timeIntervalns),
                                                        oversample,
                                                        ctypes.byref(returnedMaxSamples),
                                                        0)
        assert_pico_ok(self.status["getTimebase2"])

        # Run block capture
        # handle = chandle
        # number of pre-trigger samples = preTriggerSamples
        # number of post-trigger samples = PostTriggerSamples
        # timebase = 8 = 80 ns = timebase (see Programmer's guide for mre information on timebases)
        # oversample = 0 = oversample
        # time indisposed ms = None (not needed in the example)
        # segment index = 0
        # lpReady = None (using ps2000aIsReady rather than ps2000aBlockReady)
        # pParameter = None
        self.status["runBlock"] = ps.ps2000aRunBlock(self.chandle,
                                                preTriggerSamples,
                                                postTriggerSamples,
                                                timebase,
                                                oversample,
                                                None,
                                                0,
                                                None,
                                                None)
        assert_pico_ok(self.status["runBlock"])

        # Check for data collection to finish using ps2000aIsReady
        ready = ctypes.c_int16(0)
        check = ctypes.c_int16(0)
        while ready.value == check.value:
            self.status["isReady"] = ps.ps2000aIsReady(self.chandle, ctypes.byref(ready))

        # Create buffers ready for assigning pointers for data collection
        bufferAMax = (ctypes.c_int16 * totalSamples)()
        bufferAMin = (ctypes.c_int16 * totalSamples)() # used for downsampling which isn't in the scope of this example
        bufferBMax = (ctypes.c_int16 * totalSamples)()
        bufferBMin = (ctypes.c_int16 * totalSamples)() # used for downsampling which isn't in the scope of this example

        # Set data buffer location for data collection from channel A
        # handle = chandle
        # source = PS2000A_CHANNEL_A = 0
        # pointer to buffer max = ctypes.byref(bufferDPort0Max)
        # pointer to buffer min = ctypes.byref(bufferDPort0Min)
        # buffer length = totalSamples
        # segment index = 0
        # ratio mode = PS2000A_RATIO_MODE_NONE = 0
        self.status["setDataBuffersA"] = ps.ps2000aSetDataBuffers(self.chandle,
                                                            0,
                                                            ctypes.byref(bufferAMax),
                                                            ctypes.byref(bufferAMin),
                                                            totalSamples,
                                                            0,
                                                            0)
        assert_pico_ok(self.status["setDataBuffersA"])

        # Set data buffer location for data collection from channel B
        # handle = chandle
        # source = PS2000A_CHANNEL_B = 1
        # pointer to buffer max = ctypes.byref(bufferBMax)
        # pointer to buffer min = ctypes.byref(bufferBMin)
        # buffer length = totalSamples
        # segment index = 0
        # ratio mode = PS2000A_RATIO_MODE_NONE = 0

        self.status["setDataBuffersB"] = ps.ps2000aSetDataBuffers(self.chandle,
                                                            1,
                                                            ctypes.byref(bufferBMax),
                                                            ctypes.byref(bufferBMin),
                                                            totalSamples,
                                                            0,
                                                            0)
        assert_pico_ok(self.status["setDataBuffersB"])

        # Create overflow location
        overflow = ctypes.c_int16()
        # create converted type totalSamples
        cTotalSamples = ctypes.c_int32(totalSamples)

        # Retried data from scope to buffers assigned above
        # handle = chandle
        # start index = 0
        # pointer to number of samples = ctypes.byref(cTotalSamples)
        # downsample ratio = 0
        # downsample ratio mode = PS2000A_RATIO_MODE_NONE
        # pointer to overflow = ctypes.byref(overflow))
        self.status["getValues"] = ps.ps2000aGetValues(self.chandle, 0, ctypes.byref(cTotalSamples), 0, 0, 0, ctypes.byref(overflow))
        assert_pico_ok(self.status["getValues"])


        # find maximum ADC count value
        # handle = chandle
        # pointer to value = ctypes.byref(maxADC)
        maxADC = ctypes.c_int16()
        self.status["maximumValue"] = ps.ps2000aMaximumValue(self.chandle, ctypes.byref(maxADC))
        assert_pico_ok(self.status["maximumValue"])

        # convert ADC counts data to mV
        self.adc2mVChAMax =  adc2mV(bufferAMax, chARange, maxADC)
        # self.adc2mVSigGen = adc2mV()
        # self.adc2mVChAMax_ls =[]

        # for i in self.adc2mVChAMax:
        #     i = i/1000
        #     self.adc2mVChAMax_ls.append(i)

        print("channel A (in mV) =", self.adc2mVChAMax)
        
        self.adc2mVChBMax =  adc2mV(bufferBMax, chBRange, maxADC)

        # self.adc2mVChBMax_ls =[]
        
        # for i in self.adc2mVChBMax:
        #     i = i/1000
        #     self.adc2mVChAMax_ls.append(i)

        print("channel B (in mV) =", self.adc2mVChBMax)

        # Create time data
        self.time = np.linspace(0, ((cTotalSamples.value)-1) * timeIntervalns.value, cTotalSamples.value)

        # plot data from channel A and signalgen
        # plt.plot(self.time, self.adc2mVChAMax[:])
        plt.plot(self.time, self.adc2mVChBMax)
        plt.plot(self.time, self.adc2mVChAMax)
        # plt.plot(self.time, self.adc2mVChBMax_ls)
        plt.xlabel('Time (ns)')
        plt.ylabel('Voltage (mV)')
        plt.show()

        # Stop the scope
        # handle = chandle
        self.status["stop"] = ps.ps2000aStop(self.chandle)
        assert_pico_ok(self.status["stop"])

        # Close unitDisconnect the scope
        # handle = chandle
        self.status["close"] = ps.ps2000aCloseUnit(self.chandle)
        assert_pico_ok(self.status["close"])

        # display status returns
        print(self.status)

    def trigger(self):

        waveform_desired_duration = 7E-3 #change waveform desired duration to set the frequency of the wave
        obs_duration = 3 * waveform_desired_duration
        sampling_interval = obs_duration / 4096

        (actualSamplingInterval, nSamples, maxSamples) = \
            self.ps.setSamplingInterval(sampling_interval, obs_duration)
        print("Sampling interval = %f ns" % (actualSamplingInterval * 1E9))
        print("Taking  samples = %d" % nSamples)
        print("Maximum samples = %d" % maxSamples)

        waveformAmplitude = 2.0
        # x = np.linspace(-1, 1, num=ps.AWGMaxSamples, endpoint=False)

        #----commented out for NEW Tx test----
        # freq = 110000
        # fs = int(2*freq) # sample rate
        # t = np.linspace(0, 3, 1000, endpoint = False)

        # noise1 = 0
        # noise2 = 0.01*np.sin(2*np.pi * 0.1*t) + 0.01*np.sin(2*np.pi * 1.8*t) + 0.01*np.sin(2*np.pi * 0.4*t)

        # realSignal = 2*np.sin(2*np.pi* t)
        # sig = noise1

        # sig = np.append(sig, [realSignal, noise2, realSignal, noise1*noise2])
        # print("signal=", sig)

        # (waveform_duration, deltaPhase) = self.ps.setAWGSimple(
        #     sig, waveform_desired_duration, offsetVoltage=0.0,
        #     indexMode="Single", triggerSource='None')
        

        # the setChannel command will chose the next largest amplitude
        # BWLimited = 1 for 6402/6403, 2 for 6404, 0 for all
        channelARange = self.ps.setChannel('A', 'AC', waveformAmplitude, 0.0,
                                    enabled=True, BWLimited=False)
        channelBRange = self.ps.setChannel('B', 'AC', waveformAmplitude, 0.0,
                                    enabled=True, BWLimited=False)

        print("Chosen channel A range = %d" % channelARange)
        print("Chosen channel B range = %d" % channelBRange)

        self.ps.setSimpleTrigger('A', 1.0, 'Rising', delay=0, timeout_ms=100,
                            enabled=True)
        # self.ps.setSimpleTrigger('B', 1.0, 'Rising', delay=0, timeout_ms=100,
        #                     enabled=True)

        self.ps.runBlock()
        self.ps.waitReady()
        print("Waiting for awg to settle.")
        time.sleep(2.0)
        self.ps.runBlock()
        self.ps.waitReady()
        print("Done waiting for trigger")
        self.adc2mVChAMax = self.ps.getDataV('A', 200, returnOverflow=False)
        self.adc2mVChBMax = self.ps.getDataV('B', 200, returnOverflow=False)

        self.time = np.arange(200) * actualSamplingInterval

        self.ps.stop()
        self.ps.close()

        plt.plot(self.time, self.adc2mVChAMax, label="Tx")
        plt.plot(self.time,self.adc2mVChBMax, label="Rx")
        plt.title("Picoscope 2000A waveforms")
        plt.ylabel("Voltage (V)")
        plt.xlabel("Time (ms)")
        plt.legend()
        plt.show()

    # def savecsv(self, fname = 'test_1', fdest ='./CSV Files', file = "./le_test.csv", dist = 0.2):
    #     # self.channel_a = self.adc2mVChAMax[:]
    #     # self.channel_b = self.adc2mVChBMax[:]
    #     #file = '../capstone\\CSV Files\\' + str(fname) + '.csv'
    #     #write_file = open(file, 'w')
    #     #trace = pd.read_csv(file, sep='\t', skiprows=16, header=None)
    #     #trace = trace.loc[self.channel_a, self.time]
    #     # self.dict2csv = {"Voltage(mV)": self.channel_a, "Time(ns)": self.time}
    #      # trace.columns = ['voltage (mV)','time (ns)']
    #     # self.df = pd.DataFrame(self.dict2csv)
    #     # print(self.df)
    #     stiffness_val = self.swv2stiffness_csvextract(file, float(dist))
    #     stiffness_val_df = pd.DataFrame({'stiffness' : [stiffness_val]})

    #     # fdest ="add in filepath for RPi"
    #     # fname = "test" + [date]

    #     # print(stiffness_val_df)
    #     # print(fdest + '\\' + fname + '.csv')
    #     stiffness_val_df.to_csv(fdest + '\\' + fname + '.csv', sep='\t', encoding='utf-8', index = False)

    # def graph2speed(self, distance = 2.0):

    #     Tx_obj = Tx()

    #     #display both transmitting and receiving graphs
    #     plt.plot(self.time, self.adc2mVChBMax[:])
    #     plt.plot(self.time, Tx_obj.return_pwm())
    #     plt.xlabel('Time (ns)')
    #     plt.ylabel('Voltage (mV)')
    #     plt.show()

    #     #find time between both graphs
    #     #get the first voltage value > 0
    #     abovezerovals_receiving = []
    #     for i in self.adc2mVChAMax[:]:
    #         if i>0:
    #             abovezerovals_receiving.append(i)

    #     getfirstval_receiving = abovezerovals_receiving[0]

    #     #get time from the voltage 
    #     for i in range (0,5000):
    #         for j in self.df.iloc[i][0]:
    #             if j == getfirstval_receiving:
    #                 firstval_receiving_time = self.df.iloc[i][1]
    #                 break

    #     #do the same as above for transmitting circuit too
    #     abovezerovals_transmit = []
    #     for i in self.df():
    #         if i>0:
    #             abovezerovals_transmit.append(i)

    #     getfirstval_transmitting = abovezerovals_receiving[0]

    #     #get time from the voltage 
    #     for i in range (0,5000):
    #         for j in self.df.iloc[i][0]:
    #             if j == getfirstval_transmitting:
    #                 firstval_transmitting_time = self.df.iloc[i][1]
    #                 break

    #     time_diff = firstval_receiving_time - firstval_transmitting_time
    #     shear_wave_velocity = distance/time_diff
    #     return shear_wave_velocity

    def swv2stiffness(self):
        swv = self.graph2speed()
        #g/ml to kg/m^3
        stiffness = 1.07 *1000 *(swv**2)
        stiffness_inkPa = stiffness/1000
        print(str(stiffness_inkPa) + " kPa")
        return stiffness_inkPa

    def plotgraph2checkwave(self, file = "./le_test.csv"):
        #export as current waveform from picotech 
        # time_ls = []
        # voltage_ls = []
        # for i in range(1,33):
        #     if i < 10:
        #         if i == 1:
                    # file = "../Waveform\\" + "Waveform_0" + str(i) + ".csv"
        trace = pd.read_csv(file, skiprows=3)
        plt.plot(trace.iloc[:, 0].values, trace.iloc[:, 1].values)
        plt.plot(trace.iloc[:, 0].values, (trace.iloc[:, 2].values))
                    # trace = trace.loc[:,0:1]
                    # time_ls.append(trace[:, 0:1])
                    # voltage_ls.append(trace[:,1])
                    # plt.plot(time_ls, voltage_ls)
                # else:
                #     file = "../Waveform\\" + "Waveform_0" + str(i) + ".csv"
                #     trace = pd.read_csv(file, skiprows=3)
                # #     # j_ls = [start ]
                # #     # trace.iloc[0, 0]
                # #     # for k in range(0,33):
                # #     #     j = trace.iloc[0, k] + 10.003 * (i-1)
                # #     #     j_ls.append(j)
                # #     #         # plt.plot(trace.iloc[:, 0].values, trace.iloc[:, 1].values)
                # #     #     plt.plot(j_ls, trace.iloc[:, 1].values)
                # #         # print(trace)
                #     plt.plot(trace.iloc[:, 0].values, trace.iloc[:, 1].values)

            # if i >= 10:
            #     file = "../Waveform\\" + "Waveform_" + str(i) + ".csv"
            #     trace = pd.read_csv(file, skiprows=3)
            #     # trace = trace.loc[:, 0:1]
            #     # time_ls.append(trace[:, 0:1])
            #     # voltage_ls.append(trace[:,1])
            #     # plt.plot(time_ls, voltage_ls)
            #     plt.plot(trace.iloc[:, 0].values, trace.iloc[:, 1].values)
                

        # print(time_ls)
        plt.xlabel('Time (us)')
        plt.ylabel('Voltage (mV)')
        plt.show()

    def findmaxvoltageandtime_rx_run(self):
            #find maximum voltage from the graph and subsequent times for transmitting end
            # trace = pd.read_csv(file, skiprows=3)
            # trace_x = trace.iloc[:,0].values #time
            # trace_chb = trace.iloc[:,2].values #voltage from channel B
            # print(trace_x)

            # time_ls = []
            # # self.dict2csv = {"Time(ns)": trace_x, "Voltage(mV) Channel B": trace_chb}
            # self_time_ls =[]
            # for j in self.time:
            #     self_time_ls.append(j)

            # chB_ls =[]
            # for k in self.adc2mVChBMax[:]:
            #     chB_ls.append(k)
                # print(k)
            # print("chb=",chB_ls)

            filter_val = self.digital_filter()

            time_ls=[]
            self.dict2csv = {"Time(ms)": self.time, "Voltage(V) Channel B": filter_val}

            self.df = pd.DataFrame(self.dict2csv)
            # print("length=", len(self.df))
            print(self.df)
            for i in range (0,len(self.df)):
                volt = self.df.iloc[i][1]
                print(volt)
                if volt > 0.5: #change accordingly initial:0.05
                    if self.df.iloc[i][1] > self.df.iloc[i-1][1]:
                        if self.df.iloc[i][1] > self.df.iloc[i+1][1]:
                            get_time = self.df.iloc[i][0]
                            time_ls.append(get_time)
                            # print(get_time)
                    else:
                        None

            print("time_rx_ls = ", time_ls)
            time_ls = time_ls[0]
            print("time_rx_ls_new = ", time_ls)
            # time_rx_ls = []
            # print("time_ls_rx = ", time_ls)
            # time_rx_ls.append(time_ls[0])
            # for k in range(0, len(time_ls)):
            #     if (time_ls[k]-time_ls[k-1]) > 0.2:
            #         time_rx_ls.append(time_ls[k])
            # # print(time_rx_ls) 
            # return time_rx_ls   
            return time_ls

    def findmaxvoltageandtime_tx_run(self):
        
        #find maximum voltage from the graph and subsequent times for transmitting end
        # trace = pd.read_csv(file, skiprows=3)
        # trace_x = trace.iloc[:,0].values #time
        # trace_cha = trace.iloc[:,1].values #voltage from channel A

        time_ls = []
        # self.dict2csv = {"Time(ns)": trace_x, "Voltage(mV) Channel A": trace_cha}
        # self_time_ls =[]
        # for j in self.time:
        #     self_time_ls.append(j)

        # chA_ls =[]
        # for k in self.adc2mVChAMax[:]:
        #     chA_ls.append(k)
        #     # print("cha=",chA_ls)

        self.dict2csv = {"Time(ms)": self.time, "Voltage(V) Channel A": self.adc2mVChAMax[:]}
        # self.dict2csv = {"Time(ns)": self.time, "Voltage(mV) Channel A": self.adc2mVChAMax[:]}

        self.df = pd.DataFrame(self.dict2csv)
        for i in range (0,len(self.df)):
            volt = self.df.iloc[i][1]
            # print(self.df.iloc[0][1])
            if volt > 1.9: #change accordingly
                if self.df.iloc[i][1] > self.df.iloc[i-1][1]:
                    if self.df.iloc[i][1] >= self.df.iloc[i+1][1]:
                        get_time = self.df.iloc[i][0]
                        time_ls.append(get_time)
                        # print(get_time)
                else:
                    None
        print("time_tx_ls = ", time_ls)
        time_ls = time_ls[0]
        print("time_tx_ls_new = ", time_ls)
        # time_tx_ls = []
        # print("time_ls_tx = ", time_ls)
        # time_tx_ls.append(time_ls[0])
        # for k in range(0, len(time_ls)):
        #     if (time_ls[k]-time_ls[k-1]) > 0.2:
        #         time_tx_ls.append(time_ls[k])
        # # print(time_tx_ls)
        # return time_tx_ls
        return time_ls

    def findmaxvoltageandtime_rx(self, file = "./le_test.csv"):
            #find maximum voltage from the graph and subsequent times for transmitting end
            trace = pd.read_csv(file, skiprows=3)
            trace_x = trace.iloc[:,0].values #time
            trace_chb = trace.iloc[:,2].values #voltage from channel B
            # print(trace_x)

            filter_val = self.digital_filter(file)
            print("filtered")

            time_ls = []
            # self.dict2csv = {"Time(ns)": trace_x, "Voltage(mV) Channel B": trace_chb}
            self.dict2csv = {"Time(ns)": trace_x, "Voltage(mV) Channel B": filter_val}

            self.df = pd.DataFrame(self.dict2csv)
            for i in range (0,len(self.df)):
                volt = self.df.iloc[i][1]
                if volt > 360: #change accordingly
                    if self.df.iloc[i][1] > self.df.iloc[i-1][1]:
                        if self.df.iloc[i][1] > self.df.iloc[i+1][1]:
                            get_time = self.df.iloc[i][0]
                            time_ls.append(get_time)
                            # print(get_time)
                    else:
                        None

            time_rx_ls = []
            print("time_rx =",time_ls)
            time_rx_ls.append(time_ls[0])
            for k in range(0, len(time_ls)):
                if (time_ls[k]-time_ls[k-1]) > 0.2:
                    time_rx_ls.append(time_ls[k])
            print("new_time_rx_ls=", time_rx_ls) 
            return time_rx_ls   


    def findmaxvoltageandtime_tx(self, file = "./le_test.csv"):
        #find maximum voltage from the graph and subsequent times for transmitting end
        trace = pd.read_csv(file, skiprows=3)
        trace_x = trace.iloc[:,0].values #time
        trace_cha = trace.iloc[:,1].values #voltage from channel A

        time_ls = []
        self.dict2csv = {"Time(ns)": trace_x, "Voltage(mV) Channel A": trace_cha}

        self.df = pd.DataFrame(self.dict2csv)
        for i in range (0,len(self.df)):
            volt = self.df.iloc[i][1]
            if volt > 200: #change accordingly
                if self.df.iloc[i][1] > self.df.iloc[i-1][1]:
                    if self.df.iloc[i][1] > self.df.iloc[i+1][1]:
                        get_time = self.df.iloc[i][0]
                        time_ls.append(get_time)
                        # print(get_time)
                else:
                    None

        time_tx_ls = []
        print("time_tx",time_ls)
        time_tx_ls.append(time_ls[0])
        for k in range(0, len(time_ls)):
            if (time_ls[k]-time_ls[k-1]) > 0.2:
                time_tx_ls.append(time_ls[k])
        print("new_time_tx_ls=", time_tx_ls) 
        return time_tx_ls

    def getswv(self, file = "./le_test.csv", dist = 0.2):
        time_rx_ls = self.findmaxvoltageandtime_rx(file)
        time_tx_ls = self.findmaxvoltageandtime_tx(file)
        time_diff_ls = []
        sumofk = 0
        for i in time_rx_ls:
            for j in time_tx_ls:
                time_diff_ls.append(float(i-j)/1000000) 
        for k in time_diff_ls:
            sumofk = sumofk + k
        average_time_diff = sumofk/len(time_diff_ls)
        print("average time = ", average_time_diff)
        shear_wave_velocity = dist/average_time_diff
        print("shear wave velocity =" ,shear_wave_velocity)
        return shear_wave_velocity    

    def getswv_run(self, dist = 0.005):
        time_rx_ls = self.findmaxvoltageandtime_rx_run()
        time_tx_ls = self.findmaxvoltageandtime_tx_run()
        # time_diff_ls = []
        # sumofk = 0
        # for i in time_rx_ls:
        #     for j in time_tx_ls:
        #         time_diff_ls.append(float(i-j)/1000) 
        # for k in time_diff_ls:
        #     sumofk = sumofk + k
        # average_time_diff = sumofk/len(time_diff_ls)
        average_time_diff = time_rx_ls - time_tx_ls
        print("average time = ", average_time_diff)
        shear_wave_velocity = dist/average_time_diff
        print("shear wave velocity =" ,shear_wave_velocity)
        return shear_wave_velocity                 
    
    def swv2stiffness_csvextract(self, file = "./le_test.csv", dist = 0.2):
        swv_val = self.getswv(file, dist)
        #g/ml to kg/m^3
        stiffness = 1.07 *1000 *(swv_val**2)
        stiffness_inkPa = stiffness/(1000*10000000000)
        print("Stiffness:" + str(stiffness_inkPa) + " kPa")
        return stiffness_inkPa

    def getstiffness(self, dist = 0.005):
        swv_val = self.getswv_run(dist)
        #g/ml to kg/m^3
        stiffness = 1.07 *1000 *(swv_val**2)
        stiffness_inkPa = stiffness/(1000)
        print("Stiffness:" + str(stiffness_inkPa) + " kPa")
        return round(stiffness_inkPa, 1)
        #find maximum voltage from the graph and subsequent times for reciving end
        #find time difference, shear wave velocity, stiffness

    #DFT Noise Filtering - via automation you receive a single tx n receiving signal
    # def dft_filter(self, file = "./le_test.csv", threshold = 0):

    #     SAMPLE_RATE = 110000  # Hertz try to change n see also
    #     # DURATION = 1  # Seconds
    #     # N = SAMPLE_RATE * DURATION
    #     N = 12503 #try to change n see if it affects

    #     trace = pd.read_csv(file, skiprows=3)

    #     # yf = fft(trace.iloc[:, 1].values)
    #     signal = trace.iloc[:, 2].values
    #     # zf_unfiltered = fft(signal)
    #     zf = fftpack.rfft(signal)
    #     # print("yf = ", yf)
    #     xf = fftpack.fftfreq(signal.size, 1 / SAMPLE_RATE)
    #     # print("sig size =", signal.size)
    #     # xf = fftfreq(signal.size, d=20e-3/signal.size)
    #     # xf = fftfreq(N, d=0.008)

    #     zf[xf>threshold] = 0 #if Frequency less than threshold, then set all to 0 to take out noise

    #     # The maximum frequency is half the sample rate
    #     # points_per_freq = len(xf) / (SAMPLE_RATE / 2)
    #     # print(points_per_freq)

    #     # Our target frequency is 4000 Hz
    #     # target_idx = int(points_per_freq * 110000)
    #     # print(target_idx)

    #     # plt.plot(xf, np.abs(yf), label = "channel A")
    #     plt.plot(xf, np.abs(zf), label = "channel B")
    #     # plt.plot(xf, np.abs(zf_unfiltered), label = "unfiltered chb")
    #     plt.xlabel("Frequency")
    #     plt.ylabel("mV")
    #     plt.legend()
    #     plt.title("FFT")
    #     plt.show()

    #     # zf[target_idx - 1 : target_idx + 2] = 0

    #     #inverse fft
    #     # new_sig = irfft(yf)
    #     new_sig_2 = fftpack.irfft(zf)
    #     # print("sig_2=", new_sig_2)
    #     # new_sig_3 = irfft(zf_unfiltered)

    #     # plt.plot((trace.iloc[:,0].values/2)-25, new_sig_3[:N]-10, label = "Unfiltered")
    #     plt.plot(trace.iloc[:,0].values, signal, label = "Raw")
    #     # plt.plot((trace.iloc[:,0].values/2)-25, new_sig_2[:N]-10, label = "Filtered")
    #     plt.plot(trace.iloc[:,0].values, new_sig_2[:N], label = "Filtered")
    #     # plt.plot(new_sig[:1000], label = "Tx Signal")
    #     plt.xlabel("Time")
    #     plt.ylabel("mV")
    #     plt.legend()
    #     plt.title("FFT Denoising")
    #     plt.show()

    def digital_filter(self):

        fs = 11000000
        b, a = signal.iirfilter(4, Wn=500000, fs=fs, btype="low", ftype="butter")
        print(b, a, sep="\n")

        signal_raw = self.adc2mVChBMax
        # y_lfilter = signal.lfilter(b, a, signal_raw)

        # plt.figure(figsize=[6.4, 2.4])
        # plt.plot(self.time, signal_raw, label="Raw signal")
        # plt.plot(self.time, y_lfilter, alpha=0.8, lw=3, label="SciPy lfilter")
        # plt.xlabel("Time (us)")
        # plt.ylabel("Amplitude (mV)")
        # plt.legend(loc="lower center", bbox_to_anchor=[0.5, 1], ncol=2,
        #         fontsize="smaller")

        # plt.tight_layout()
        # plt.savefig("simple-lowpass-lfilter.png", dpi=100)

        # apply filter forward and backward using filtfilt
        self.y_filtfilt = signal.filtfilt(b, a, signal_raw)

        plt.figure(figsize=[6.4, 2.4])
        plt.plot(self.time, signal_raw, label="Raw signal")
        # plt.plot(self.time, y_lfilter, alpha=0.5, lw=3, label="SciPy lfilter")
        plt.plot(self.time, self.y_filtfilt, alpha=0.8, lw=3, label="SciPy filtfilt")
        plt.legend(loc="lower center", bbox_to_anchor=[0.5, 1], ncol=3,
                fontsize="smaller")
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude (V)")

        plt.tight_layout()
        # plt.savefig("lowpass-filtfilt.png", dpi=100)
        plt.show()

        return self.y_filtfilt

    def digital_filter_old(self, file):
        fs = 11000000
        b, a = signal.iirfilter(4, Wn=500000, fs=fs, btype="low", ftype="butter")
        print(b, a, sep="\n")

        trace = pd.read_csv(file, skiprows=3)
        signal_raw = trace.iloc[:, 2].values

        y_lfilter = signal.lfilter(b, a, signal_raw)

        plt.figure(figsize=[6.4, 2.4])
        plt.plot(trace.iloc[:,0].values, signal_raw, label="Raw signal")
        plt.plot(trace.iloc[:,0].values, y_lfilter, alpha=0.8, lw=3, label="SciPy lfilter")
        plt.xlabel("Time (us)")
        plt.ylabel("Amplitude (mV)")
        plt.legend(loc="lower center", bbox_to_anchor=[0.5, 1], ncol=2,
                fontsize="smaller")

        plt.tight_layout()
        # plt.savefig("simple-lowpass-lfilter.png", dpi=100)

        # apply filter forward and backward using filtfilt
        self.y_filtfilt = signal.filtfilt(b, a, signal_raw)

        plt.figure(figsize=[6.4, 2.4])
        plt.plot(trace.iloc[:,0].values, signal_raw, label="Raw signal")
        plt.plot(trace.iloc[:,0].values, y_lfilter, alpha=0.5, lw=3, label="SciPy lfilter")
        plt.plot(trace.iloc[:,0].values, self.y_filtfilt, alpha=0.8, lw=3, label="SciPy filtfilt")
        plt.legend(loc="lower center", bbox_to_anchor=[0.5, 1], ncol=3,
                fontsize="smaller")
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude (V)")

        plt.tight_layout()
        # plt.savefig("lowpass-filtfilt.png", dpi=100)
        plt.show()

        return self.y_filtfilt


    # def rapid_block_mode(self):

    #     # Create chandle and status ready for use
    #     status = {}
    #     chandle = ctypes.c_int16()

    #     # Opens the device/s
    #     status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)
    #     assert_pico_ok(status["openunit"])

    #     # Set up channel A
    #     # handle = chandle
    #     # channel = ps2000a_CHANNEL_A = 0
    #     # enabled = 1
    #     # coupling type = ps2000a_DC = 1
    #     # range = ps2000a_10V = 9
    #     # analogue offset = 0 V
    #     chARange = 9
    #     status["setChA"] = ps.ps2000aSetChannel(chandle, 0, 1, 1, chARange, 0)
    #     assert_pico_ok(status["setChA"])

    #     # Sets up single trigger
    #     # andle = chandle
    #     # Enable = 1
    #     # Source = ps2000a_channel_A = 0
    #     # Threshold = 1024 ADC counts
    #     # Direction = ps2000a_Falling = 3
    #     # Delay = 0
    #     # autoTrigger_ms = 1000
    #     status["trigger"] = ps.ps2000aSetSimpleTrigger(chandle, 1, 0, 1024, 3, 0, 1000)
    #     assert_pico_ok(status["trigger"])

    #     # Setting the number of sample to be collected
    #     preTriggerSamples = 400
    #     postTriggerSamples = 400
    #     maxsamples = preTriggerSamples + postTriggerSamples

    #     # Gets timebase innfomation
    #     # WARNING: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
    #     # To access these Timebases, set any unused analogue channels to off.
    #     # handle = chandle
    #     # Timebase = 2 = timebase
    #     # Nosample = maxsamples
    #     # TimeIntervalNanoseconds = ctypes.byref(timeIntervalns)
    #     # MaxSamples = ctypes.byref(returnedMaxSamples)
    #     # Segement index = 0
    #     timebase = 2
    #     timeIntervalns = ctypes.c_float()
    #     returnedMaxSamples = ctypes.c_int16()
    #     status["GetTimebase"] = ps.ps2000aGetTimebase2(chandle, timebase, maxsamples, ctypes.byref(timeIntervalns), 1, ctypes.byref(returnedMaxSamples), 0)
    #     assert_pico_ok(status["GetTimebase"])

    #     # Creates a overlow location for data
    #     overflow = ctypes.c_int16()
    #     # Creates converted types maxsamples
    #     cmaxSamples = ctypes.c_int32(maxsamples)

    #     # Handle = Chandle
    #     # nSegments = 10
    #     # nMaxSamples = ctypes.byref(cmaxSamples)

    #     status["MemorySegments"] = ps.ps2000aMemorySegments(chandle, 10, ctypes.byref(cmaxSamples))
    #     assert_pico_ok(status["MemorySegments"])

    #     # sets number of captures
    #     status["SetNoOfCaptures"] = ps.ps2000aSetNoOfCaptures(chandle, 10)
    #     assert_pico_ok(status["SetNoOfCaptures"])

    #     # Starts the block capture
    #     # handle = chandle
    #     # Number of prTriggerSamples
    #     # Number of postTriggerSamples
    #     # Timebase = 2 = 4ns (see Programmer's guide for more information on timebases)
    #     # time indisposed ms = None (This is not needed within the example)
    #     # Segment index = 0
    #     # LpRead = None
    #     # pParameter = None
    #     status["runblock"] = ps.ps2000aRunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, 1, None, 0, None, None)
    #     assert_pico_ok(status["runblock"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 0
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxsamples, 0, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax1 = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin1 = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 1
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax1), ctypes.byref(bufferAMin1), maxsamples, 1, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax2 = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin2 = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 2
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax2), ctypes.byref(bufferAMin2), maxsamples, 2, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax3 = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin3 = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 3
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax3), ctypes.byref(bufferAMin3), maxsamples, 3, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax4 = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin4 = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 4
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax4), ctypes.byref(bufferAMin4), maxsamples, 4, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax5 = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin5 = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 5
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax5), ctypes.byref(bufferAMin5), maxsamples, 5, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax6 = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin6 = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 6
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax6), ctypes.byref(bufferAMin6), maxsamples, 6, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax7 = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin7 = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 7
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax7), ctypes.byref(bufferAMin7), maxsamples, 7, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax8 = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin8 = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 8
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax8), ctypes.byref(bufferAMin8), maxsamples, 8, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Create buffers ready for assigning pointers for data collection
    #     bufferAMax9 = (ctypes.c_int16 * maxsamples)()
    #     bufferAMin9 = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

    #     # Setting the data buffer location for data collection from channel A
    #     # handle = chandle
    #     # source = ps2000a_channel_A = 0
    #     # Buffer max = ctypes.byref(bufferAMax)
    #     # Buffer min = ctypes.byref(bufferAMin)
    #     # Buffer length = maxsamples
    #     # Segment index = 9
    #     # Ratio mode = ps2000a_Ratio_Mode_None = 0
    #     status["SetDataBuffers"] = ps.ps2000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax9), ctypes.byref(bufferAMin9), maxsamples, 9, 0)
    #     assert_pico_ok(status["SetDataBuffers"])

    #     # Creates a overlow location for data
    #     overflow = (ctypes.c_int16 * 10)()
    #     # Creates converted types maxsamples
    #     cmaxSamples = ctypes.c_int32(maxsamples)

    #     # Checks data collection to finish the capture
    #     ready = ctypes.c_int16(0)
    #     check = ctypes.c_int16(0)
    #     while ready.value == check.value:
    #         status["isReady"] = ps.ps2000aIsReady(chandle, ctypes.byref(ready))

    #     # handle = chandle
    #     # noOfSamples = ctypes.byref(cmaxSamples)
    #     # fromSegmentIndex = 0
    #     # ToSegmentIndex = 9
    #     # DownSampleRatio = 0
    #     # DownSampleRatioMode = 0
    #     # Overflow = ctypes.byref(overflow)

    #     status["GetValuesBulk"] = ps.ps2000aGetValuesBulk(chandle, ctypes.byref(cmaxSamples), 0, 9, 0, 0, ctypes.byref(overflow))
    #     assert_pico_ok(status["GetValuesBulk"])

    #     # handle = chandle
    #     # Times = Times = (ctypes.c_int16*10)() = ctypes.byref(Times)
    #     # Timeunits = TimeUnits = ctypes.c_char() = ctypes.byref(TimeUnits)
    #     # Fromsegmentindex = 0
    #     # Tosegementindex = 9
    #     Times = (ctypes.c_int16*10)()
    #     TimeUnits = ctypes.c_char()
    #     status["GetValuesTriggerTimeOffsetBulk"] = ps.ps2000aGetValuesTriggerTimeOffsetBulk64(chandle, ctypes.byref(Times), ctypes.byref(TimeUnits), 0, 9)
    #     assert_pico_ok(status["GetValuesTriggerTimeOffsetBulk"])

    #     # Finds the max ADC count
    #     # handle = chandle
    #     # Value = ctype.byref(maxADC)
    #     maxADC = ctypes.c_int16()
    #     status["maximumValue"] = ps.ps2000aMaximumValue(chandle, ctypes.byref(maxADC))
    #     assert_pico_ok(status["maximumValue"])

    #     # Converts ADC from channel A to mV
    #     self.adc2mVChAMax = adc2mV(bufferAMax, chARange, maxADC)
    #     self.adc2mVChAMax1 = adc2mV(bufferAMax1, chARange, maxADC)
    #     self.adc2mVChAMax2 = adc2mV(bufferAMax2, chARange, maxADC)
    #     self.adc2mVChAMax3 = adc2mV(bufferAMax3, chARange, maxADC)
    #     self.adc2mVChAMax4 = adc2mV(bufferAMax4, chARange, maxADC)
    #     self.adc2mVChAMax5 = adc2mV(bufferAMax5, chARange, maxADC)
    #     self.adc2mVChAMax6 = adc2mV(bufferAMax6, chARange, maxADC)
    #     self.adc2mVChAMax7 = adc2mV(bufferAMax7, chARange, maxADC)
    #     self.adc2mVChAMax8 = adc2mV(bufferAMax8, chARange, maxADC)
    #     self.adc2mVChAMax9 = adc2mV(bufferAMax9, chARange, maxADC)

    #     # Creates the time data
    #     time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)

    #     # Plots the data from channel A onto a graph
    #     plt.plot(time, self.adc2mVChAMax[:])
    #     plt.plot(time, self.adc2mVChAMax1[:])
    #     plt.plot(time, self.adc2mVChAMax2[:])
    #     plt.plot(time, self.adc2mVChAMax3[:])
    #     plt.plot(time, self.adc2mVChAMax4[:])
    #     plt.plot(time, self.adc2mVChAMax5[:])
    #     plt.plot(time, self.adc2mVChAMax6[:])
    #     plt.plot(time, self.adc2mVChAMax7[:])
    #     plt.plot(time, self.adc2mVChAMax8[:])
    #     plt.plot(time, self.adc2mVChAMax9[:])
    #     plt.xlabel('Time (ns)')
    #     plt.ylabel('Voltage (mV)')
    #     plt.show()

    #     # Stops the scope
    #     # Handle = chandle
    #     status["stop"] = ps.ps2000aStop(chandle)
    #     assert_pico_ok(status["stop"])

    #     # Closes the unit
    #     # Handle = chandle
    #     status["close"] = ps.ps2000aCloseUnit(chandle)
    #     assert_pico_ok(status["close"])

    #     # Displays the status returns
    #     print(status)

#rapid block mode gives out waves but at different timezones; how to set all to same timezone first
    # def waveform_averaging(self):
    #     for i in range(0,9):
    #         for j in "self.adc2mVChAMax" + str(i) + "[:]":
    #             for k in "self.adc2mVChAMax" + str(i+1) + "[:]":
    #             # name = "self.adc2mVChAMax" + str(i) + "[:]"
    #             # name_2 = "self.adc2mVChAMax" + str(i+1) + "[:]"
    #                 j[:,0] += k[:,0]

# start_PS6000 = PS6000()
# start_PS6000.plotgraph2checkwave()
# start_PS6000.dft_filter()

start_PS6000 = PS6000()
filepath = "./command.txt"
start_PS6000.open_ps2000a()
# start_PS6000.block_example()
# txt_file = open(filepath,'r')
# start_PS6000.plotgraph2checkwave("C:/Users/Charis/Downloads/Waveforms/Waveforms/agar testing/pulse/Testing_agar_pulse_10mm/Testing_agar_pulse_10mm_05.csv")
# start_PS6000.dft_filter("C:/Users/Charis/Downloads/Waveforms/Waveforms/agar testing/pulse/Testing_agar_pulse_10mm/Testing_agar_pulse_10mm_05.csv",3000)
# start_PS6000.digital_filter("C:/Users/Charis/Downloads/waveform/waveform/jellllllllllyyyyyyyy_2_23.csv")
# start_PS6000.swv2stiffness_csvextract("C:/Users/Charis/Downloads/waveform/waveform/jellllllllllyyyyyyyy_2_23.csv", 0.05)
# start_PS6000.plotgraph2checkwave("C:/Users/Charis/Downloads/waveform/waveform/jellllllllllyyyyyyyy_2_23.csv")

while True:
        txt_file = open(filepath,'r')
        print("running")
        read_txt = txt_file.read()
        print("read_txt =",read_txt)
        if read_txt == "run":
            start_PS6000.block_run()
            # start_PS6000.swv2stiffness_csvextract("./le_test.csv", 0.2)
            # stiffness_val = start_PS6000.swv2stiffness_csvextract("./le_test.csv", 0.2)
            stiffness_val_run = start_PS6000.getstiffness(0.005)
            # noise_filter = start_PS6000.dft_filter()
            # start_PS600cd 0.savecsv('test_1', './', "./le_test.csv", 0.2)
            txt_file = open(filepath,'w')
            txt_file.write(str(stiffness_val_run))
            # txt_file = open(filepath,'r')
            print("txt file: run -> works")
        sleep(5)