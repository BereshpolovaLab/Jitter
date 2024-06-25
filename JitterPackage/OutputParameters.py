#!/usr/bin/env python3
# #########################################################
#
# OutputParameter.py
#
# Python3 (NumPy,SciPy,MatPlotLib)
#
# Bereshpolova lab, University of Connecticut
# Victor Serdyukov (svv_vick)
# 2024
#
# emails: Victor.Serdyukov@uconn.edu
#         svv_vick@yahoo.com
#
# #########################################################


# ##########################################################
# COutputParameters
# ##########################################################

class COutputParameters():

    def __init__(self):
        self.PeakWeight, self.BaselineMean, self.BaselineStd, self.PeakAbove, \
            self.Efficacy, self.Contribution, self.ConfidenceInterval, \
            self.DataQuality = None, None, None, None, None, None, None, None

#
# Get - functions
#

    def GetPeakWeight(self): return self.PeakWeight

    def GetBaselineMean(self): return self.BaselineMean

    def GetBaselineStd(self): return self.BaselineStd

    def GetPeakAbove(self): return self.PeakAbove

    def GetEfficacy(self): return self.Efficacy

    def GetContribution(self): return self.Contribution

    def GetConfidenceInterval(self): return self.ConfidenceInterval

    def GetDataQuality(self): return self.DataQuality

#
# Set - functions
#

    def SetPeakWeight(self, PeakWeight): self.PeakWeight = PeakWeight

    def SetBaselineMean(self, BaselineMean): self.BaselineMean = BaselineMean

    def SetBaselineStd(self, BaselineStd): self.BaselineStd = BaselineStd

    def SetPeakAbove(self, PeakAbove): self.PeakAbove = PeakAbove

    def SetEfficacy(self, Efficacy): self.Efficacy = Efficacy

    def SetContribution(self, Contribution): self.Contribution = Contribution

    def SetConfidenceInterval(self, ConfidenceInterval):
        self.ConfidenceInterval = ConfidenceInterval

    def SetDataQuality(self, DataQuality): self.DataQuality = DataQuality
