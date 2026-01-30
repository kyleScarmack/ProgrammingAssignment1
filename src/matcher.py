# gale-shapley stable matching algorithm
# hospital-proposing deferred acceptance version

from collections import deque
from dataStruct import createRankingMaps


def galeShapley(n, hospitalPrefs, studentPrefs):
    # run the gale-shapley algorithm with hospitals proposing
    # returns (matching, numProposals)
    # initialize matching data structures
    matching = {}  # hospital_id -> student_id
    studentCurrent = {}  # student_id -> hospital_id
    nextProposalIndex = [0] * n  # next proposal index per hospital (0-based)

    # create ranking maps for students so we can quickly compare preferences
    studentRankings = createRankingMaps(studentPrefs)

    # track total proposals for statistics
    numProposals = 0

    # queue of hospitals that are currently free (1..n)
    freeHospitals = deque(range(1, n + 1))

    # main algorithm loop - continue while a free hospital can still propose
    while freeHospitals:
        h = freeHospitals.popleft()

        # if hospital has proposed to everyone, skip
        if nextProposalIndex[h - 1] >= n:
            continue

        # hospital proposes to next student on its list
        nextIdx = nextProposalIndex[h - 1]
        s = hospitalPrefs[h - 1][nextIdx]
        nextProposalIndex[h - 1] += 1
        numProposals += 1

        # student decides whether to accept the proposal
        if s not in studentCurrent:
            # student is free, accept
            matching[h] = s
            studentCurrent[s] = h
        else:
            # student compares current hospital with new proposer
            currentHospital = studentCurrent[s]
            prefersNew = studentRankings[s - 1][h] < studentRankings[s - 1][currentHospital]

            if prefersNew:
                # student switches to new hospital
                matching[h] = s
                studentCurrent[s] = h

                # old hospital becomes free again
                del matching[currentHospital]
                freeHospitals.append(currentHospital)
            else:
                # student rejects, hospital remains free
                freeHospitals.append(h)

    return matching, numProposals


def formatMatching(n, matching):
    # output format: one line per hospital "hospital student"
    lines = []
    for h in range(1, n + 1):
        if h not in matching:
            raise ValueError(f"hospital {h} is unmatched")
        lines.append(f"{h} {matching[h]}")
    return lines
