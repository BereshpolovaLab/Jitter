#!/usr/bin/env python3
###########################################################
#
# Filters.py
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


def MedianFilter(List):
    Value = 0
    if List:
        List.sort()
        Length = len(List)
        Value = List[int(Length / 2)] if Length % 2\
            else (List[int(Length / 2) - 1] + List[int(Length / 2)]) / 2
    return Value
