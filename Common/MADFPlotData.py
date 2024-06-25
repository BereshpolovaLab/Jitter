#!/usr/bin/env python3
# #########################################################
#
# MADFPlotData.py
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


from Common import BasicPlotData as C_BPD


# #########################################################
# CMADFBasicPlotData
# #########################################################

class CMADFPlotData(C_BPD.CBasicPlotData):

    def __init__(self, PlotParameters, GridSize, LogFile):
        super().__init__(PlotParameters, GridSize, LogFile)

#
# GetPlotParameters - functions
#

    def GetPlotParameters_MaximumAutoDetectFlag(self):
        return self.DictionaryParameter(
            self.PlotParameters, 'MaximumAutoDetectFlag')

    def GetPlotParameters_FieldRadius(self):
        return self.DictionaryParameter(
            self.PlotParameters, 'FieldRadius')
