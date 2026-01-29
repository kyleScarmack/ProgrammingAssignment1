"""
(a) Checks validity: each hospital and each student is matched to exactly one partner, with no duplicates.
(b) Checks stability: confirms there is no blocking pair.
"""

import sys
from inputParser import parseInput
from dataStruct import createRankingMaps

def readMatching(filename, n):
    # Read matching output file 
    with open(filename, 'r') as file:
        lines = []
        for line in file:
            strippedLine = line.strip()
            if strippedLine != "":
                lines.append(strippedLine)
    
    # Check number of lines
    if len(lines) != n:
        raise ValueError(f"Expected {n} matching lines but got {len(lines)}")
    
    # Parse matching
    matching = {}
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid matching line: {line}")
        hospital = int(parts[0])
        student = int(parts[1])
        matching[hospital] = student
    
    return matching