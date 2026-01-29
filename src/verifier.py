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


def checkValidity(n, matching):
    # Check number of hospitals matched
    if len(matching) != n:
        return False, f"INVALID: Expected {n} hospitals, got {len(matching)}"
    
    # Check all hospitals are matched
    for h in range(1, n + 1):
        if h not in matching:
            return False, f"INVALID: Hospital {h} is not in the matching"
    
    # Check for duplicate students
    studentsMatched = set()
    for hospital, student in matching.items():
        if (student < 1) or (student > n):
            return False, f"INVALID: Student {student} is out of range [1, {n}]"
        
        if student in studentsMatched:
            return False, f"INVALID: Student {student} is matched to multiple hospitals"
        
        studentsMatched.add(student)
    
    # Check all students are matched
    if len(studentsMatched) != n:
        missingStudents = set(range(1, n+1)) - studentsMatched
        missingString = ", ".join(map(str, sorted(missingStudents)))
        return False, f"INVALID: Students not matched: {missingString}"
    
    return True, ""


def checkStability(n, matching, hospitalPrefs, studentPrefs):
    # Create ranking matrices for fast comparison
    hospitalRanking = createRankingMaps(hospitalPrefs)
    studentRanking = createRankingMaps(studentPrefs)

    # Create reverse matching for students
    studentMatch = {}
    for hospital, student in matching.items():
        studentMatch[student] = hospital
    
    # Check all possible pairs
    for h in range(1, n+1):
        currentStudent = matching[h]
        
        for s in range(1, n+1):
            # Skip if this is the current match
            if s == currentStudent:
                continue
            
            currentHospital = studentMatch[s]
            
            # Check if (h, s) forms a blocking pair
            # createRankingMaps returns a 0-indexed list
            hPrefersS = hospitalRanking[h-1][s] < hospitalRanking[h-1][currentStudent]
            sPrefersH = studentRanking[s-1][h] < studentRanking[s-1][currentHospital]
            
            if hPrefersS and sPrefersH:
                return False, f"UNSTABLE: Blocking pair (Hospital {h}, Student {s})"
    
    return True, ""


def verifyMatching(inputFile, matchingFile):
    try:
        # Read input preferences
        n, hospitalPrefs, studentPrefs = parseInput(inputFile)
        
        # Read matching
        matching = readMatching(matchingFile, n)
        
        # Check validity
        isValid, validityMessage = checkValidity(n, matching)
        if not isValid:
            return False, validityMessage
        
        # Check stability
        isStable, stabilityMessage = checkStability(n, matching, hospitalPrefs, studentPrefs)
        if not isStable:
            return False, stabilityMessage
        
        return True, "VALID STABLE"
        
    except Exception as e:
        return False, f"ERROR : {str(e)}"


def main():
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python verifier.py <input_file> <matching_file>")
        sys.exit(1)
    
    inputFile = sys.argv[1]
    matchingFile = sys.argv[2]

    success, message = verifyMatching(inputFile, matchingFile)
    print(message)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()