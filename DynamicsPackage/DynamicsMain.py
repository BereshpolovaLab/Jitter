#!/usr/bin/env python3
# #########################################################
#
# DynamicsMain.py
#
# Python3 (NumPy, SciPy, MatPlotLib)
#
# Bereshpolova lab, University of Connecticut
# Victor Serdyukov (svv_vick)
# 2017 - 2024
#
# emails: Victor.Serdyukov@uconn.edu
#         svv_vick@yahoo.com
#
# #########################################################


from Common import LogFileObject as C_LFO


# #########################################################
# Analysis
# #########################################################

def Main(
    InitPlexonDataFunc, Parameters, PLXFileName, LogFileName,
        PlotGraphicFileName, HotSpotMaximum_FittingCurve_GraphicFileName,
        Power_FittingCurve_GraphicFileName):
    LFO = C_LFO.CLogFileObject(LogFileName)
    PlexonData = InitPlexonDataFunc(Parameters, LFO.LogFile)
    if PlexonData.GetStatusFlag():
        PlexonData.Processing(PLXFileName)
        if PlexonData.GetStatusFlag():
            # print hot spot maximums, strngths, sign indexes
            PlexonData.PrintHotSpotMaximums()
            PlexonData.PrintStrengths()
            PlexonData.PrintSignIndexes()
            # show plots
            PlexonData.ShowPlots(PlotGraphicFileName)
            # show fitting curves
            PlexonData.ShowHotSpotMaximumFittingCurves(
                HotSpotMaximum_FittingCurve_GraphicFileName)
            PlexonData.ShowPowerFittingCurves(
                Power_FittingCurve_GraphicFileName)
            # show maximum and power MTSD
            PlexonData.ShowMaximumAndPowerMTSD()
