#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on March 24, 2020
@author: meganwillis
Reads Thermo .RAW files using MSFileReader python (pymsfilereader) bindings and saves chromatogram data as a *.csv output
pymsfilereader installation instructions at https://github.com/frallain/pymsfilereader
"""

################################
import numpy as np
import pandas as pd
from pymsfilereader import MSFileReader
import matplotlib.pyplot as plt
################################

#########################
####---PATHS:----########
#########################
path0 = "C:/Users/Admin/Documents/MSFileReader/"
fname = “DataFile.RAW"
pfile = path0 + fname
outname = fname[:-4]+".csv"
outfile = path0+outname

#########################
####---INPUTS:----#######
#########################
mzlist = [103.003, 115.003, 89.024]
int_window = 0.03
#########################
####----MAIN:----########
#########################

###### ----open *.RAW file
rawfile = MSFileReader(pfile)

###### ---various useful pymsfilereader commands (see MSFileReader.py for details)
# print('IsThereMSData', rawfile.IsThereMSData())
# print("GetNumberOfControllersOfType('MS')", rawfile.GetNumberOfControllersOfType('MS'))
# print( 'GetControllerType(1)',  rawfile.GetControllerType(0))
# print('GetCurrentController()', rawfile.GetCurrentController())
# print('GetMassResolution', rawfile.GetMassResolution())
print('GetLowMass', rawfile.GetLowMass())
print('GetHighMass', rawfile.GetHighMass())
print('GetStartTime', rawfile.GetStartTime())
print('GetEndTime', rawfile.GetEndTime())
print('GetNumSpectra', rawfile.GetNumSpectra())
# print('GetFirstSpectrumNumber', rawfile.GetFirstSpectrumNumber())
# print('GetLastSpectrumNumber', rawfile.GetLastSpectrumNumber())
# print('GetMassListFromScanNum', rawfile.GetMassListFromScanNum(scan_number))
# print('GetMassListRangeFromScanNum', rawfile.GetMassListRangeFromScanNum(scan_number))
# print('GetSegmentedMassListFromScanNum', rawfile.GetSegmentedMassListFromScanNum(scan_number))
# print('GetAverageMassList', rawfile.GetAverageMassList(scan_number, scan_number + 10))
# print('GetAveragedMassSpectrum', rawfile.GetAveragedMassSpectrum([scan_number, scan_number + 5, scan_number + 10]))
# print('GetChroData', rawfile.GetChroData(startTime=rawfile.StartTime,
#                                             endTime=rawfile.EndTime,
#                                             massRange1="{}-{}".format(rawfile.LowMass, rawfile.HighMass),
#                                             scanFilter="Full ms"))


###### ----- Extract Chromatograms

#### -- get Chromatogram Data out of the raw file and into a DataFrame
output = pd.DataFrame()

for k in mzlist:
    mzrange = str(k - int_window) + '-' + str(k + int_window)
    print('m/z range = ' + mzrange)
    temp = rawfile.GetChroData(startTime=rawfile.StartTime, endTime=rawfile.EndTime,
                                    massRange1=mzrange)  # returns a nested tuple
    #outcols = ['Time_min']  # initialize a list of column names each time
    mzname = 'mz'+str(int(k))
    #outcols.append(mzname)
    chro_data = np.transpose(np.array(temp[0]))
    #print(df.shape)
    if k==mzlist[0]:
        output['Time_min'] = chro_data[:,0]
        output[mzname] = chro_data[:,1]
        output.set_index('Time_min', inplace=True)
    else:
        output[mzname] = chro_data[:,1]

#### ---- quick checks
print(output.head())
plt.plot(output)
plt.show()

###### ----- save chromatogram data out to a CSV file
output.to_csv(outfile)
print("Saving to "+ outfile)

###### ----- close *.RAW file
rawfile.Close()