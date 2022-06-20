# from argparse import ONE_OR_MORE
import ctypes
from datetime import date
# from turtle import shearfactor
# from webbrowser import get
import numpy as np
from picosdk.ps2000a import ps2000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
import time
import pandas as pd
# from Tx import Tx
from scipy.fft import fft, fftfreq, irfft
from time import sleep

#generate signal or receive a signal
#print the signal n convert into csv

class PS6000:

    def open_ps2000a(self):

        with ps.open_unit() as device:
            print('Device info: {}'.format(device.info))

    def open_ps6(self):
        return None

    def block_example(self):
        # This example opens a 2000a driver device, sets up two channels and a trigger then collects a block of data.
        # This data is then plotted as mV against time in ns.

        # Create chandle and status ready for use
        chandle = ctypes.c_int16()
        status = {}

        # Open 2000 series PicoScope
        # Returns handle to chandle for use in future API functions
        status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)

        try:
            assert_pico_ok(status["openunit"])
        except:
            # powerstate becomes the status number of openunit
            powerstate = status["openunit"]

            # If powerstate is the same as 282 then it will run this if statement
            if powerstate == 282:
                # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
                status["ChangePowerSource"] = ps.ps2000aChangePowerSource(chandle, 282)
            # If the powerstate is the same as 286 then it will run this if statement
            elif powerstate == 286:
                # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
                status["ChangePowerSource"] = ps.ps2000aChangePowerSource(chandle, 286)
            else:
                raise

            assert_pico_ok(status["ChangePowerSource"])
        assert_pico_ok(status["openunit"])

        # Set up channel A
        # handle = chandle
        # channel = PS2000A_CHANNEL_A = 0
        # enabled = 1
        # coupling type = PS2000A_DC = 1
        # range = PS2000A_2V = 7
        # analogue offset = 0 V
        chARange = 7
        status["setChA"] = ps.ps2000aSetChannel(chandle, 0, 1, 1, chARange, 0)
        assert_pico_ok(status["setChA"])

        # Set up channel B
        # handle = chandle
        # channel = PS2000A_CHANNEL_B = 1
        # enabled = 1
        # coupling type = PS2000A_DC = 1
        # range = PS2000A_2V = 7
        # analogue offset = 0 V
        chBRange = 7
        status["setChB"] = ps.ps2000aSetChannel(chandle, 1, 1, 1, chBRange, 0)
        assert_pico_ok(status["setChB"])

        # Set up single trigger
        # handle = chandle
        # enabled = 1
        # source = PS2000A_CHANNEL_A = 0
        # threshold = 1024 ADC counts
        # direction = PS2000A_RISING = 2
        # delay = 0 s
        # auto Trigger = 1000 ms

        # status["trigger"] = ps.ps2000aSetSimpleTrigger(chandle, 1, 0, 1024, 2, 0, 1000)
        # assert_pico_ok(status["trigger"])

        # status["signalgen"] = ps.ps2000aSetSigGenBuiltIn(chandle, 20, 50, 0, 1000, 1200, 0, 20, PS2000A_UP, PS2000A_ES_OFF, 1, 0, PS2000A_SIGGEN_GATE_HIGH, PS2000A_SIGGEN_NONE, 0)
        # assert_pico_ok(status["signalgen"])

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
        wavetype = ctypes.c_int16(0)
        sweepType = ctypes.c_int32(0)
        triggertype = ctypes.c_int32(0)
        triggerSource = ctypes.c_int32(0)

        status["SetSigGenBuiltIn"] = ps.ps2000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 110000, 110000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
        assert_pico_ok(status["SetSigGenBuiltIn"])

        # Pauses the script to show signal
        time.sleep(10)
        
        # status["changesiggen"] = ps.ps2000aSetSigGenPropertiesArbitary(chandle, 20, 40, 20, 20, )

        # Set number of pre and post trigger samples to be collected
        preTriggerSamples = 3
        postTriggerSamples = 3
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
        status["getTimebase2"] = ps.ps2000aGetTimebase2(chandle,
                                                        timebase,
                                                        totalSamples,
                                                        ctypes.byref(timeIntervalns),
                                                        oversample,
                                                        ctypes.byref(returnedMaxSamples),
                                                        0)
        assert_pico_ok(status["getTimebase2"])

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
        status["runBlock"] = ps.ps2000aRunBlock(chandle,
                                                preTriggerSamples,
                                                postTriggerSamples,
                                                timebase,
                                                oversample,
                                                None,
                                                0,
                                                None,
                                                None)
        assert_pico_ok(status["runBlock"])

        # Check for data collection to finish using ps2000aIsReady
        ready = ctypes.c_int16(0)
        check = ctypes.c_int16(0)
        while ready.value == check.value:
            status["isReady"] = ps.ps2000aIsReady(chandle, ctypes.byref(ready))

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
        status["setDataBuffersA"] = ps.ps2000aSetDataBuffers(chandle,
                                                            0,
                                                            ctypes.byref(bufferAMax),
                                                            ctypes.byref(bufferAMin),
                                                            totalSamples,
                                                            0,
                                                            0)
        assert_pico_ok(status["setDataBuffersA"])

        # Set data buffer location for data collection from channel B
        # handle = chandle
        # source = PS2000A_CHANNEL_B = 1
        # pointer to buffer max = ctypes.byref(bufferBMax)
        # pointer to buffer min = ctypes.byref(bufferBMin)
        # buffer length = totalSamples
        # segment index = 0
        # ratio mode = PS2000A_RATIO_MODE_NONE = 0

        status["setDataBuffersB"] = ps.ps2000aSetDataBuffers(chandle,
                                                            1,
                                                            ctypes.byref(bufferBMax),
                                                            ctypes.byref(bufferBMin),
                                                            totalSamples,
                                                            0,
                                                            0)
        assert_pico_ok(status["setDataBuffersB"])

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
        status["getValues"] = ps.ps2000aGetValues(chandle, 0, ctypes.byref(cTotalSamples), 0, 0, 0, ctypes.byref(overflow))
        assert_pico_ok(status["getValues"])


        # find maximum ADC count value
        # handle = chandle
        # pointer to value = ctypes.byref(maxADC)
        maxADC = ctypes.c_int16()
        status["maximumValue"] = ps.ps2000aMaximumValue(chandle, ctypes.byref(maxADC))
        assert_pico_ok(status["maximumValue"])

        # convert ADC counts data to mV
        self.adc2mVChAMax =  adc2mV(bufferAMax, chARange, maxADC)
        # self.adc2mVSigGen = adc2mV()
        # self.adc2mVChAMax_ls =[]

        # for i in self.adc2mVChAMax:
        #     i = i/1000
        #     self.adc2mVChAMax_ls.append(i)

        print("channel A (in mV) =", self.adc2mVChAMax[:])
        
        self.adc2mVChBMax =  adc2mV(bufferBMax, chBRange, maxADC)

        # self.adc2mVChBMax_ls =[]
        
        # for i in self.adc2mVChBMax:
        #     i = i/1000
        #     self.adc2mVChAMax_ls.append(i)

        print("channel B (in mV) =", self.adc2mVChBMax[:])

        # Create time data
        self.time = np.linspace(0, ((cTotalSamples.value)-1) * timeIntervalns.value, cTotalSamples.value)

        # plot data from channel A and signalgen
        plt.plot(self.time, self.adc2mVChAMax[:])
        plt.plot(self.time, self.adc2mVChBMax[:])
        # plt.plot(self.time, self.adc2mVChAMax_ls)
        # plt.plot(self.time, self.adc2mVChBMax_ls)
        plt.xlabel('Time (ns)')
        plt.ylabel('Voltage (mV)')
        plt.show()

        # Stop the scope
        # handle = chandle
        status["stop"] = ps.ps2000aStop(chandle)
        assert_pico_ok(status["stop"])

        # Close unitDisconnect the scope
        # handle = chandle
        status["close"] = ps.ps2000aCloseUnit(chandle)
        assert_pico_ok(status["close"])

        # display status returns
        print(status)

    def savecsv(self, fname = 'test_1', fdest ='./CSV Files', file = "./le_test.csv", dist = 0.2):
        # self.channel_a = self.adc2mVChAMax[:]
        # self.channel_b = self.adc2mVChBMax[:]
        #file = '../capstone\\CSV Files\\' + str(fname) + '.csv'
        #write_file = open(file, 'w')
        #trace = pd.read_csv(file, sep='\t', skiprows=16, header=None)
        #trace = trace.loc[self.channel_a, self.time]
        # self.dict2csv = {"Voltage(mV)": self.channel_a, "Time(ns)": self.time}
         # trace.columns = ['voltage (mV)','time (ns)']
        # self.df = pd.DataFrame(self.dict2csv)
        # print(self.df)
        stiffness_val = self.swv2stiffness_csvextract(file, float(dist))
        stiffness_val_df = pd.DataFrame({'stiffness' : [stiffness_val]})

        # fdest ="add in filepath for RPi"
        # fname = "test" + [date]

        # print(stiffness_val_df)
        # print(fdest + '\\' + fname + '.csv')
        stiffness_val_df.to_csv(fdest + '\\' + fname + '.csv', sep='\t', encoding='utf-8', index = False)

    def graph2speed(self, distance = 2.0):

        Tx_obj = Tx()

        #display both transmitting and receiving graphs
        plt.plot(self.time, self.adc2mVChBMax[:])
        plt.plot(self.time, Tx_obj.return_pwm())
        plt.xlabel('Time (ns)')
        plt.ylabel('Voltage (mV)')
        plt.show()

        #find time between both graphs
        #get the first voltage value > 0
        abovezerovals_receiving = []
        for i in self.adc2mVChAMax[:]:
            if i>0:
                abovezerovals_receiving.append(i)

        getfirstval_receiving = abovezerovals_receiving[0]

        #get time from the voltage 
        for i in range (0,5000):
            for j in self.df.iloc[i][0]:
                if j == getfirstval_receiving:
                    firstval_receiving_time = self.df.iloc[i][1]
                    break

        #do the same as above for transmitting circuit too
        abovezerovals_transmit = []
        for i in self.df():
            if i>0:
                abovezerovals_transmit.append(i)

        getfirstval_transmitting = abovezerovals_receiving[0]

        #get time from the voltage 
        for i in range (0,5000):
            for j in self.df.iloc[i][0]:
                if j == getfirstval_transmitting:
                    firstval_transmitting_time = self.df.iloc[i][1]
                    break

        time_diff = firstval_receiving_time - firstval_transmitting_time
        shear_wave_velocity = distance/time_diff
        return shear_wave_velocity

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
        plt.plot(trace.iloc[:, 0].values, (trace.iloc[:, 2].values/1000))
                    # trace = trace.loc[:,0:1]
                    # time_ls.append(trace[:, 0:1])
                    # voltage_ls.append(trace[:,1])
                    # plt.plot(time_ls, voltage_ls)
                # else:
                #     file = "../Waveform\\" + "Waveform_0" + str(i) + ".csv"
                #     trace = pd.read_csv(file, skiprows=3)
                # #     # j_ls = []
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
        plt.ylabel('Voltage (V)')
        plt.show()

    def findmaxvoltageandtime_tx(self, file = "./le_test.csv"):
            #find maximum voltage from the graph and subsequent times for transmitting end
            # trace = pd.read_csv(file, skiprows=3)
            # trace_x = trace.iloc[:,0].values #time
            # trace_cha = trace.iloc[:,1].values #voltage from channel A

            time_ls = []
            # self.dict2csv = {"Time(ns)": trace_x, "Voltage(mV) Channel A": trace_cha}
            self.dict2csv = {"Time(ns)": self.time, "Voltage(mV) Channel A": self.adc2mVChAMax[:]}

            self.df = pd.DataFrame(self.dict2csv)
            for i in range (0,len(self.df)):
                volt = self.df.iloc[i][1]
                if volt > 2: #change accordingly
                    if self.df.iloc[i][1] > self.df.iloc[i-1][1]:
                        if self.df.iloc[i][1] > self.df.iloc[i+1][1]:
                            get_time = self.df.iloc[i][0]
                            time_ls.append(get_time)
                            # print(get_time)
                    else:
                        None

            time_tx_ls = []
            time_tx_ls.append(time_ls[0])
            for k in range(0, len(time_ls)):
                if (time_ls[k]-time_ls[k-1]) > 0.2:
                    time_tx_ls.append(time_ls[k])
            # print(time_tx_ls)
            return time_tx_ls

    def findmaxvoltageandtime_rx(self, file = "./le_test.csv"):
            #find maximum voltage from the graph and subsequent times for transmitting end
            # trace = pd.read_csv(file, skiprows=3)
            # trace_x = trace.iloc[:,0].values #time
            # trace_chb = trace.iloc[:,2].values #voltage from channel B
            # print(trace_x)

            time_ls = []
            # self.dict2csv = {"Time(ns)": trace_x, "Voltage(mV) Channel B": trace_chb}
            self.dict2csv = {"Time(ns)": self.time, "Voltage(mV) Channel B": self.adc2mVChBMax[:]}

            self.df = pd.DataFrame(self.dict2csv)
            for i in range (0,len(self.df)):
                volt = self.df.iloc[i][1]
                if volt > 0.07: #change accordingly
                    if self.df.iloc[i][1] > self.df.iloc[i-1][1]:
                        if self.df.iloc[i][1] > self.df.iloc[i+1][1]:
                            get_time = self.df.iloc[i][0]
                            time_ls.append(get_time)
                            # print(get_time)
                    else:
                        None

            time_rx_ls = []
            # print(time_ls)
            time_rx_ls.append(time_ls[0])
            for k in range(0, len(time_ls)):
                if (time_ls[k]-time_ls[k-1]) > 0.2:
                    time_rx_ls.append(time_ls[k])
            # print(time_rx_ls) 
            return time_rx_ls   

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
    
    def swv2stiffness_csvextract(self, file = "./le_test.csv", dist = 0.2):
        swv_val = self.getswv(file, dist)
        #g/ml to kg/m^3
        stiffness = 1.07 *1000 *(swv_val**2)
        stiffness_inkPa = stiffness/(1000*10000000000)
        print("Stiffness:" + str(stiffness_inkPa) + " kPa")
        return stiffness_inkPa

        #find maximum voltage from the graph and subsequent times for reciving end
        #find time difference, shear wave velocity, stiffness

    #DFT Noise Filtering
    def dft_filter(self):

        SAMPLE_RATE = 110000  # Hertz
        DURATION = 1  # Seconds
        N = SAMPLE_RATE * DURATION

        file = "./le_test.csv"
        trace = pd.read_csv(file, skiprows=3)

        yf = fft(trace.iloc[:, 2].values/1000)
        print("yf = ", yf)
        xf = fftfreq(N, 1 / SAMPLE_RATE)
        print("xf = ", xf)

        # The maximum frequency is half the sample rate
        points_per_freq = len(xf) / (SAMPLE_RATE / 2)
        print(points_per_freq)

        # Our target frequency is 4000 Hz
        target_idx = int(points_per_freq * 4000)
        print(target_idx)

        plt.plot(xf, np.abs(yf))
        plt.show()

        yf[target_idx - 1 : target_idx + 2] = 0

        #inverse fft
        new_sig = irfft(yf)

        plt.plot(new_sig[:1000])
        plt.show()

    #Waveform Averaging cannot rly be done

# start_PS6000 = PS6000()
# start_PS6000.plotgraph2checkwave()
# start_PS6000.dft_filter()

start_PS6000 = PS6000()
filepath = "./command.txt"
txt_file = open(filepath,'r')
start_PS6000.open_ps2000a()
start_PS6000.block_example()
while True:
        print("running")
        read_txt = txt_file.read()
        print("read_txt =",read_txt)
        if read_txt == "run":
#         # start_PS6000.open_ps2000a()
#         # start_PS6000.block_example()
#         # start_PS6000.savecsv()
#         #start_PS6000.findmaxvoltageandtime_tx()
            start_PS6000.plotgraph2checkwave()
            # start_PS6000.swv2stiffness_csvextract("./le_test.csv", 0.2)
            stiffness_val = start_PS6000.swv2stiffness_csvextract("./le_test.csv", 0.2)
            # noise_filter = start_PS6000.dft_filter()
            # start_PS600cd 0.savecsv('test_1', './', "./le_test.csv", 0.2)
            txt_file = open(filepath,'w')
            txt_file.write(str(stiffness_val))
            txt_file = open(filepath,'r')
            print("txt file: run -> works")
        sleep(10)