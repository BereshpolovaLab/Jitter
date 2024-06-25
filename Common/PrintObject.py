#!/usr/bin/env python3
###########################################################
#
# PrintObject.py
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
###########################################################


###########################################################
# CPrintObject
###########################################################

class CPrintObject:

    def __init__(self, LogFile): self.LogFile = LogFile

#
# Get - functions
#

    def GetLogFile(self): return self.LogFile

#
# Print - functions
#

    def Print(self, List):
        String = ''.join(List)
        print(String)
        if self.LogFile and not self.LogFile.closed:
            self.LogFile.write(F'{String}\n')
