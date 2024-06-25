#!/usr/bin/env python3
# #########################################################
#
# JCMain.py
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


import os


from Common import LogFileObject as C_LFO
from JitterPackage import JCPlexonData as JP_JCPD


# #########################################################
# Analysis
# #########################################################

def Main(
        Parameters, PLXFileName, CC_CurveGraphicFileName, CC_RawDataFileName,
        CC_JitterDataFileName, CC_FinalDataFileName,
        CC_FinalShiftedDataFileName, LogFileName):
    DirName = os.path.dirname(os.path.abspath(LogFileName))
    if not os.path.exists(DirName):
        os.mkdir(DirName)
    LFO = C_LFO.CLogFileObject(LogFileName)
    JCPD = JP_JCPD.CPlexonData(
        Parameters, PLXFileName, CC_CurveGraphicFileName, CC_RawDataFileName,
        CC_JitterDataFileName, CC_FinalDataFileName,
        CC_FinalShiftedDataFileName, LFO.LogFile)
    if JCPD.GetStatusFlag():
        JCPD.DataProcessing()
        if JCPD.GetStatusFlag():
            JCPD.ShowCrossCorrelationCurves()
            JCPD.PrintReportAndData()
