#!/usr/bin/env python3
# #########################################################
#
# JCPlexonData.py
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


import copy
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import tabulate

from Common import BasicChannelData as C_BCD
from Common import BasicPlexonData as C_BPD
from Common import ToolObject as C_TO

from JitterPackage import OutputParameters as JP_OP


# ##########################################################
# CPlexonData
# ##########################################################

class CPlexonData(C_BPD.CBasicPlexonData, C_TO.CToolObject):

    def __init__(
            self, Parameters, PLXFileName, CC_CurveGraphicFileName,
            CC_RawDataFileName, CC_JitterDataFileName, CC_FinalDataFileName,
            CC_FinalShiftedDataFileName, LogFile):
        super().__init__(Parameters, LogFile)

        self.PLXFileName, self.CC_CurveGraphicFileName, \
            self.CC_RawDataFileName, self.CC_JitterDataFileName, \
            self.CC_FinalDataFileName, self.CC_FinalShiftedDataFileName, \
            self.ReferenceChannelData, self.TargetChannelData, self.RDOP, \
            self.FDOP, self.FSDOP, self.CC_TimeStampList, \
            self.CC_RawDataList, self.CC_JitterDataList, \
            self.CC_FinalDataList, self.CC_FinalShiftedDataList = \
            PLXFileName, CC_CurveGraphicFileName, CC_RawDataFileName, \
            CC_JitterDataFileName, CC_FinalDataFileName, \
            CC_FinalShiftedDataFileName, \
            C_BCD.CBasicChannelData(
                self.Parameters['ReferenceChannelCluster'], LogFile), \
            C_BCD.CBasicChannelData(
                self.Parameters['TargetChannelCluster'], LogFile), \
            JP_OP.COutputParameters(), JP_OP.COutputParameters(), \
            JP_OP.COutputParameters(), [], [], [], [], []

        for CD in (self.ReferenceChannelData, self.TargetChannelData):
            self.ChannelDataList.append(CD)

        CC_TW1, CC_TW2, CC_Bin = self.GetCC_TW_Parameters()
        if CC_TW1 < CC_TW2 and CC_Bin > 0:
            self.CC_TimeStampList = [
                t + 0.5 * CC_Bin for t in np.arange(CC_TW1, CC_TW2, CC_Bin)]
            self.SetStatusFlag(True)
        else:
            self.Print((
                'Wrong cross correlation parameters',
                'Please check settins in configuration file.'))
            self.SetStatusFlag(False)

    def GetCC_TW_Parameters(self):
        CCP = self.Parameters['CrossCorrelationParameters']
        return CCP['T1'], CCP['T2'], CCP['Bin']

#
# Analysis - functions
#

    def DataProcessing(self):
        self.SetStatusFlag(False)
        self.LoadData_CheckSpikesAndTTLEvents(self.PLXFileName, False)
        if self.GetStatusFlag():
            ReferenceSpikeList = self.ReferenceChannelData.GetSpikeList()
            TargetSpikeList = self.TargetChannelData.GetSpikeList()
            RL, TL = len(ReferenceSpikeList), len(TargetSpikeList)

            def GetDuration(List):
                Duration = 0
                if List:
                    Duration = round((List[-1] - List[0]) / 1000)
                return Duration

            RD = GetDuration(ReferenceSpikeList)
            TD = GetDuration(TargetSpikeList)

            print(F'\nReference channel spike number: {RL}')
            print(F'Reference channel duration: {RD} s')
            print(F'\nTarget channel spike number: {TL}')
            print(F'Target channel duration: {TD} s\n')

            Resampling_TargetSpikeList = self.Resampling(TargetSpikeList)
            self.CC_RawDataList = self.CrossCorrelation(
                ReferenceSpikeList, TargetSpikeList)

            self.CC_JitterDataList = np.zeros(len(self.CC_RawDataList))
            SSN = self.Parameters['SimulatedSignalNumber']
            for i in range(SSN):
                print(F'Resampling and crosscorrelation: {i+1} of {SSN}')
                CC_JDL = np.array(
                    self.CrossCorrelation(
                        ReferenceSpikeList, self.Resampling(
                            TargetSpikeList)))
                self.CC_JitterDataList = np.add(
                    self.CC_JitterDataList, CC_JDL)
            self.CC_JitterDataList = list(np.divide(
                self.CC_JitterDataList, SSN))

            self.CC_FinalDataList = [
                r-j for (r, j) in zip(
                    self.CC_RawDataList, self.CC_JitterDataList)]
            Minimum = min(self.CC_FinalDataList)
            self.CC_FinalShiftedDataList = copy.deepcopy(self.CC_FinalDataList)
            if Minimum < 0:
                self.CC_FinalShiftedDataList = \
                    list(np.add(self.CC_FinalShiftedDataList, abs(Minimum)))

            # calculate output parameters: raw and final
            for CC_DL, DOP in ((
                    self.CC_RawDataList, self.RDOP), (
                    self.CC_FinalDataList, self.FDOP), (
                    self.CC_FinalShiftedDataList, self.FSDOP)):
                self.CalculateOutputParameters(CC_DL, DOP)

    def Resampling(self, InputSpikeList):
        OutputSpikeList = []
        if InputSpikeList:
            t, Index, JTW = InputSpikeList[0], 0, \
                self.Parameters['JitterTimeWindow']
            while t <= InputSpikeList[-1]:
                t2 = t + JTW
                JTW_SpikeList = [
                    SE for SE in InputSpikeList[Index:]
                    if SE >= t and SE <= t2]
                if JTW_SpikeList:
                    Index = InputSpikeList.index(JTW_SpikeList[0], Index)
                    for SE in JTW_SpikeList:
                        OutputSpikeList.append(random.uniform(t, t2))
                t = t2
        OutputSpikeList.sort()
        return OutputSpikeList

    # R - reference, T - target, S - spike, L - list, E - event
    def CrossCorrelation(self, RSL, TSL):
        CC_TW1, CC_TW2, CC_Bin = self.GetCC_TW_Parameters()
        Index, CC_DataList = 0, [0] * len(self.CC_TimeStampList)
        for R_SE in RSL:
            t1, t2 = R_SE + CC_TW1, R_SE + CC_TW2
            CC_TW_TSL = [SE for SE in TSL[Index:] if SE >= t1 and SE <= t2]
            if CC_TW_TSL:
                Index = TSL.index(CC_TW_TSL[0], Index)
                for SE in CC_TW_TSL:
                    CC_Index = math.floor((SE - t1) / CC_Bin)
                    if CC_Index >= len(CC_DataList):
                        CC_Index = -1
                    CC_DataList[CC_Index] += 1
        return CC_DataList

    def CalculateOutputParameters(self, CC_DataList, DOP):
        PI = self.Parameters['PeakInterval']
        PIL = [t for t in self.CC_TimeStampList if t >= PI[0] and t <= PI[1]]
        if PIL:
            Index1, Index2 = self.CC_TimeStampList.index(PIL[0]), \
                self.CC_TimeStampList.index(PIL[-1]) + 1
            PeakValue = max(CC_DataList[Index1:Index2])
            PeakBinNumber, PeakIndex = self.Parameters['PeakBinNumber'], \
                Index1 + CC_DataList[Index1:Index2].index(PeakValue)
            Index1, Index2 = PeakIndex - PeakBinNumber, \
                PeakIndex + PeakBinNumber + 1
            PeakList = CC_DataList[Index1:Index2]
            PeakWeight = sum(PeakList)
            BaselineList = [
                v for (t, v) in zip(self.CC_TimeStampList, CC_DataList)
                if t >= self.Parameters['BaselineInterval'][0] and
                t <= self.Parameters['BaselineInterval'][1]]
            BLL_Mean, BLL_Std = np.mean(BaselineList), np.std(BaselineList)
            PeakAbove = PeakWeight - BLL_Mean * len(PeakList)


            Efficacy = PeakAbove / \
                self.ReferenceChannelData.GetSpikeListLength()
            Contribution = PeakAbove / \
                self.TargetChannelData.GetSpikeListLength()



            ConfidenceInterval = BLL_Mean + 2.5783 * BLL_Std
            DataQuality = \
                len([v for v in PeakList if v >= ConfidenceInterval]) > 2
            # output parameters
            DOP.SetPeakWeight(PeakWeight)
            DOP.SetBaselineMean(BLL_Mean)
            DOP.SetBaselineStd(BLL_Std)
            DOP.SetPeakAbove(PeakAbove)
            DOP.SetEfficacy(Efficacy)
            DOP.SetContribution(Contribution)
            DOP.SetConfidenceInterval(ConfidenceInterval)
            DOP.SetDataQuality(DataQuality)

# Show - functions

    def ShowCrossCorrelationCurves(self):
        RawColor, JitterColor, FinalColor, FinalShiftedColor, Maximum, \
            Minimum = self.Parameters['JitterCurve_RawColor'], \
            self.Parameters['JitterCurve_JitterColor'], \
            self.Parameters['JitterCurve_FinalColor'], \
            self.Parameters['JitterCurve_FinalShiftedColor'], \
            max(
                max(self.CC_RawDataList), max(self.CC_JitterDataList),
                max(self.CC_FinalDataList)), \
            min(
                min(self.CC_RawDataList), min(self.CC_JitterDataList),
                min(self.CC_FinalDataList))

        fig = plt.figure(figsize=(20, 10))
        plt.suptitle('Cross correlations', fontsize=16)

        plt.subplot(411)
        plt.title('Raw data')
        plt.plot(self.CC_TimeStampList, self.CC_RawDataList, color=RawColor)
        plt.ylim(Minimum, Maximum)

        plt.subplot(412)
        plt.title('Monte Carlo jitter')
        plt.plot(
            self.CC_TimeStampList, self.CC_JitterDataList, color=JitterColor)
        plt.ylim(Minimum, Maximum)

        plt.subplot(413)
        plt.title('Final')
        plt.plot(
            self.CC_TimeStampList, self.CC_FinalDataList, color=FinalColor)
        plt.ylim(Minimum, Maximum)

        plt.subplot(414)
        plt.title('Final shifted')
        plt.plot(
            self.CC_TimeStampList, self.CC_FinalShiftedDataList,
            color=FinalShiftedColor)
        plt.ylim(Minimum, Maximum)

        self.ShowAndSave(
            fig, self.CC_CurveGraphicFileName, 'CC_CurveGraphicFileDPI',
            'signal')

#
# Report - functions
#

    def PrintReportAndData(self):
        # print output parameters
        for Title, DOP in ((
                'Raw data output parameters', self.RDOP), (
                'Final data output parameters', self.FDOP), (
                'Final shifted data output parameters', self.FSDOP)):
            self.PrintParameters(Title, DOP)
        # print data
        for CC_DF, CC_DL in ((
                self.CC_RawDataFileName, self.CC_RawDataList), (
                self.CC_JitterDataFileName, self.CC_JitterDataList), (
                self.CC_FinalDataFileName, self.CC_FinalDataList), (
                self.CC_FinalShiftedDataFileName,
                self.CC_FinalShiftedDataList)):
            if CC_DF and CC_DL:
                self.PrintData(CC_DF, CC_DL)

    def PrintParameters(self, Title, DOP):

        def value(v): return self.FMT(v, '{:0.3f}') if v else 'None'

        def value2(v): return 'Good' if v else 'Bad'

        HeaderList, Data2DList = ['Parameter', 'Value'], [[
            'PeakWeight', value(DOP.GetPeakWeight())], [
            'Baseline mean', value(DOP.GetBaselineMean())], [
            'Baseline std', value(DOP.GetBaselineStd())], [
            'PeakAbove', value(DOP.GetPeakAbove())], [
            'Efficacy', value(DOP.GetEfficacy())], [
            'Contribution', value(DOP.GetContribution())], [
            'Confidence interval', value(DOP.GetConfidenceInterval())], [
            'DataQuality', value2(DOP.GetDataQuality())]]

        Tabulate = tabulate.tabulate(Data2DList, headers=HeaderList)
        self.Print((F'{Title}\n{Tabulate}\n\n'))

    def PrintData(self, FileName, CC_DataList):
        f = None
        try:
            f = open(FileName, 'wt')
        except IOError:
            self.PrintError((
                'Error!!! Can not write data text file! Something wrong.'))
        finally:
            for (t, v) in zip(self.CC_TimeStampList, CC_DataList):
                f.write(f'{t} {v}\n')
