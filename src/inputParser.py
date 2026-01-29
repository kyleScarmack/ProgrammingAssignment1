# input parser for stable matching problem
# reads and validates preference lists from input files


# parse input file function to pass in hospitals and students preference lists
def parse_input(filename):
    # reading in file with edge case handling
    # read non-empty lines from file
    with open(filename) as file:
        lines = [line.strip() for line in file if line.strip()]

    # edge case, empty file
    if not lines:
        raise ValueError("empty input file")

    # edge case, parse first line as n (number of hospitals or students)
    try:
        n = int(lines[0])
    except ValueError:
        raise ValueError("first line must be an integer")
    
    # edge case, ensure n is positive
    if n < 1:
        raise ValueError("n must be at least 1")
    
    # edge case, ensure exactly 2n + 1 lines
    expectedLines = 2 * n + 1
    if len(lines) != expectedLines:
        raise ValueError(f"expected {expectedLines} lines, got {len(lines)}")
    

    # parse hospitals preference lists
    # init hospitals preferences list empty
    hospitalPrefs = []
    for i in range(1, n + 1):
        # split line into ints
        prefLine = lines[i].split()

        # edge case, check that we have n preferences
        if len(prefLine) != n:
            raise ValueError(f"hospital {i} must have {n} preferences")
        
        # convert strings to ints
        try:
            prefs = [int(x) for x in prefLine]
        except ValueError:
            raise ValueError(f"hospital {i} preferences must be integers")
        
        # validate permutation of 1 to n (no dupes, all in range)
        if sorted(prefs) != list(range(1, n + 1)):
            raise ValueError(f"hospital {i} preferences must be a permutation of 1 to ... {n}")

        hospitalPrefs.append(prefs)


    # parse students preference lists
    # init students preferences list empty
    studentPrefs = []
    for i in range(n + 1, 2 * n + 1):
        # split line into ints
        prefLine = lines[i].split()

        # edge case, check that we have n preferences
        if len(prefLine) != n:
            raise ValueError(f"student {i - n} must have {n} preferences")
        
        # convert strings to ints
        try:
            prefs = [int(x) for x in prefLine]
        except ValueError:
            raise ValueError(f"student {i - n} preferences must be integers")
        
        # validate permutation of 1 to n (no dupes, all in range)
        if sorted(prefs) != list(range(1, n + 1)):
            raise ValueError(f"student {i - n} preferences must be a permutation of 1 to ... {n}")

        studentPrefs.append(prefs)

    return n, hospitalPrefs, studentPrefs

# validate input function to ensure data consistency
def validateInput(n, hospitalPrefs, studentPrefs):
    # ensure number of hospital preferences matches n
    if n != len(hospitalPrefs):
        raise ValueError(f"expected {n} hospital preference lists, got {len(hospitalPrefs)}")
    
    # ensure number of student preferences matches n
    if n != len(studentPrefs):
        raise ValueError(f"expected {n} student preference lists, got {len(studentPrefs)}")
    
    return True