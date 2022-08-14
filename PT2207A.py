import numpy as np
import ctypes
from picosdk.ps2000a import ps2000a as ps
# from picoscope import ps2000a 
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
import time
from scipy import signal
import pandas as pd

class PS2000A:

    def automate_ps(self):
        print("automate picoscope")
        # # This opens a 2000a driver device, sets up two channels and a trigger then collects a block of data.
        # # This data is then plotted as mV against time in ns.

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
        postTriggerSamples = 2000 #500
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
        timebase = 2 #change here
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

        print("channel A (in mV) =", self.adc2mVChAMax)

        self.adc2mVChBMax =  adc2mV(bufferBMax, chBRange, maxADC)

        print("channel B (in mV) =", self.adc2mVChBMax)

        # Create time data
        self.ed_time = np.linspace(0, ((cTotalSamples.value)-1) * timeIntervalns.value, cTotalSamples.value)

        # # commented out GRAPH
        plt.plot(self.ed_time, self.adc2mVChBMax, label ="rx")
        plt.plot(self.ed_time, self.adc2mVChAMax, label ="tx")
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

    def digital_filter(self):
        #This filters out the receiving signals at a critical frequency of 7MHz using SciPy IIR filter

        fs = 180000000
        b, a = signal.iirfilter(4, Wn=7000000, fs=fs, rp=3 ,rs=60, btype="low", ftype="ellip")
        print(b, a, sep="\n")

        signal_raw = self.adc2mVChBMax

        # apply filter forward and backward using filtfilt
        y_filtfilt = signal.filtfilt(b, a, signal_raw)

        # #commented out FILTER GRAPH
        plt.figure(figsize=[6.4, 2.4])
        plt.plot(self.ed_time, signal_raw, label="Raw signal")
        # plt.plot(self.time, y_lfilter, alpha=0.5, lw=3, label="SciPy lfilter")
        plt.plot(self.ed_time, y_filtfilt, alpha=0.8, lw=3, label="SciPy filtfilt")
        plt.legend(loc="lower center", bbox_to_anchor=[0.5, 1], ncol=3,
                fontsize="smaller")
        plt.xlabel("Time (ns)")
        plt.ylabel("Amplitude (mV)")

        plt.tight_layout()
        # plt.savefig("lowpass-filtfilt.png", dpi=100)
        plt.show()

        return y_filtfilt

    def findmaxvoltageandtime_tx_run(self):
        #This is to find the time at which there is the maximum voltage collected from the transmitter

        # time_ls = []
        dict2csv = {"Time(ns)": self.ed_time, "Voltage(mV) Channel A": self.adc2mVChAMax}
        df = pd.DataFrame(dict2csv)
        for i in range (0,len(df)-1):
                volt = df.iloc[i][1]
                if volt > 1980: #change accordingly
                    if (df.iloc[i][1] > df.iloc[i-1][1]) and (df.iloc[i][1] >= df.iloc[i+1][1]):
                        get_time = df.iloc[i][0]
                        if get_time > 0.0:
                            print("time_tx = ", get_time)
                            return get_time
                          
        return None


    def findmaxvoltageandtime_rx_run(self):
        #This is to find the times at which there the maximum voltages are collected from the receiver
        
        filter_val = self.digital_filter()

        time_ls=[]
        dict2csv = {"Time(ns)": self.ed_time, "Voltage(mV) Channel B": filter_val}

        df = pd.DataFrame(dict2csv)

        for i in range (0,len(df)-1):
                    volt = df.iloc[i][1]
                    if volt > 1100: #change accordingly, initial is 10
                        if (df.iloc[i][1] > df.iloc[i-1][1]) and (df.iloc[i][1] >= df.iloc[i+1][1]):
                            get_time = df.iloc[i][0]
                            if get_time > 0.0:
                                print("time_rx = ", get_time)
                               
                                time_ls.append(get_time)
                                if (len(time_ls)>2): 
                                    return time_ls

        return None

    def gettime_run(self):
        #This takes in the transmitting and receiving signals and calculates the time difference between each of these values

        time_rx_ls = self.findmaxvoltageandtime_rx_run()
        time_tx_ls = self.findmaxvoltageandtime_tx_run()

        print("gettimeRUNRX = ",time_rx_ls)
        print("gettimeRUNTX = ",time_tx_ls)

        if (time_rx_ls == None) or (time_tx_ls == None): 
            return None

        for i in range(len(time_rx_ls)): 
            time_diff = time_rx_ls[i] - time_tx_ls
            print(f"time diff {i} = ", time_diff)
            if (time_diff > 250) and (time_diff < 600): 
                print("time_diff correct")
                return time_diff
        return None  

    def getstiffness(self, average_time, dist = 0.005):
        
        #This is to measure the shear wave velocity
        shear_wave_velocity = dist/((average_time)/1000000)
        print("shear wave velocity =" ,shear_wave_velocity)

        #1.07 g/ml to kg/m^3 - median density of liver
        stiffness = 1.07 *1000 *(shear_wave_velocity**2)

        #This is to measure the stiffness in kPa
        stiffness_inkPa = stiffness/(1000)
        print("Stiffness:" + str(stiffness_inkPa) + " kPa")
        return round(stiffness_inkPa, 1)    

run = PS2000A()
filepath = "./command.txt"
while True:
    txt_file = open(filepath,'r')
    print("running")
    read_txt = txt_file.read()
    print("read_txt =",read_txt)
    average_time_diff_ls =[]
    sumofk = 0
    if read_txt == "run":
        #to check once the JavaScript file overwrites command.txt when "Get a Reading" is pressed
        for i in range(2):
            print("screening in progress...")
            time_diff = None
            while (time_diff == None): 
                run.automate_ps()
                time_diff = run.gettime_run()
            average_time_diff_ls.append(time_diff)

        print("ave =",average_time_diff_ls)
        for k in average_time_diff_ls:
            sumofk += k
        average_time = sumofk/len(average_time_diff_ls)
        stiffness_val_run = run.getstiffness(average_time, 0.01745)  
        time.sleep(10) 
        txt_file = open(filepath,'w')
        #to overwrite command.txt file with the stiffness values that will be input into the JavaScript file
        txt_file.write(str(stiffness_val_run))
        print("txt file: run -> works")
    else: 
        time.sleep(0.5)
