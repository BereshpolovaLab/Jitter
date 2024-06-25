#!/usr/bin/env python3
# #########################################################
#
# LogFileObject.py
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


# #########################################################
# CLogFileObject
# #########################################################

class CLogFileObject:

    def __init__(self, LogFileName):
        self.LogFile = None
        if LogFileName:
            try:
                self.LogFile = open(LogFileName, 'w')
            except IOError:
                print('Cannot open log-file! Something is wrong.')

    def __del__(self):
        if self.LogFile and not self.LogFile.closed:
            self.LogFile.close()
