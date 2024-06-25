#!/usr/bin/env python3
# #########################################################
#
# Jitter.py
#
# Python3 (NumPy, SciPy, MatPlotLib)
#
# Bereshpolova lab, University of Connecticut
# Victor Serdyukov (svv_vick)
# 2024
#
# emails: Victor.Serdyukov@uconn.edu
#         svv_vick@yahoo.com
#
# #########################################################


from JitterPackage import JCMain as JP_JCM


# #########################################################
# Parameters
# #########################################################

DS, JS, CCS, FN = 'Data', 'Jitter', 'CrossCorrelation', 'Final'
InputDir, OutputDir, BasicFileName = F'{DS}/', F'Output/{JS}/', \
    '2022Jul13ABspont-stim1-6_01_mrg'
PLXFileName, LogFileName, BFNS, CS = F'{InputDir}{BasicFileName}.plx', \
    F'{OutputDir}{BasicFileName}.txt', F'{BasicFileName}_', '_Curves.png'
CC_CurveGraphicFileName, CCTS = F'{OutputDir}{BFNS}{JS}{CS}', F'_{CCS}.txt'
CC_RawDataFileName, CC_JitterDataFileName, CC_FinalDataFileName, \
    CC_FinalShiftedDataFileName = F'{OutputDir}{BFNS}Raw{DS}{CCTS}', \
    F'{OutputDir}{BFNS}{JS}{DS}{CCTS}', F'{OutputDir}{BFNS}{FN}{DS}{CCTS}', \
    F'{OutputDir}{BFNS}{FN}Shifted{DS}{CCTS}'

# FileInterval: seconds and other parameters: milliseconds
# Two channels are used.

# Bin: 0.5, 0.3; JTW: 5 - 2
Parameters = {
    'FileInterval': (None, None),
    'CrossCorrelationParameters': {
        'T1': -10,
        'T2': 10,
        'Bin': 0.2},
    'BaselineInterval': (-4, 0),
    'PeakInterval': (1, 4),
    # 1.2 ms aroundupeak (both direcrtion + =) = 2 * number of bins
    'PeakBinNumber': 3,

    'JitterTimeWindow': 5,
    'SimulatedSignalNumber': 10,

    # 1 channel - reference channel, 2 - target channel
    'ReferenceChannelCluster': {
        'Channel': 20,
        'Cluster': 1},
    'TargetChannelCluster':  {
        'Channel': 18,
        'Cluster': 1},

    # Curves: color or None
    'JitterCurve_RawColor': 'green',
    'JitterCurve_JitterColor': 'blue',
    'JitterCurve_FinalColor': 'red',
    'JitterCurve_FinalShiftedColor': 'magenta',

    # DPI
    'CC_CurveGraphicFileDPI': 300}


# ##########################################################
# Analysis
# ##########################################################

JP_JCM.Main(
    Parameters, PLXFileName, CC_CurveGraphicFileName, CC_RawDataFileName,
    CC_JitterDataFileName, CC_FinalDataFileName, CC_FinalShiftedDataFileName,
    LogFileName)
