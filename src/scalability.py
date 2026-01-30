import random
import time
import csv
from pathlib import Path
import matplotlib.pyplot as plt

from matcher import galeShapley, formatMatching
from inputParser import parseInput, validateInput
from verifier import verifyMatching


def createRandomInputFile(path, n):
    # Reproducible random seeded input per n
    rng = random.Random(4533 + n)

    # Write to file
    with open(path, "w") as file:
        file.write(f"{n}\n")

        # Hospital preferences
        for _ in range(n):
            prefs = list(range(1, n + 1))
            rng.shuffle(prefs)
            file.write(" ".join(map(str, prefs)) + "\n")

        # Student preferences
        for _ in range(n):
            prefs = list(range(1, n + 1))
            rng.shuffle(prefs)
            file.write(" ".join(map(str, prefs)) + "\n")


def timeGaleShapley(inputFile, outputFile, repeats=3):
    # Track best time runtime over repeats
    # Start with infinity so any time is better
    best = float("inf")
    bestMatching = None
    bestN = None

    for _ in range(repeats):
        # Read input preferences
        n, hospitalPrefs, studentPrefs = parseInput(str(inputFile))
        validateInput(n, hospitalPrefs, studentPrefs)

        # Start timing
        t0 = time.perf_counter()
        matching, _ = galeShapley(n, hospitalPrefs, studentPrefs)
        # End timing
        t1 = time.perf_counter()

        # Check for best time
        dt = t1 - t0
        if dt < best:
            best = dt
            bestMatching = matching
            bestN = n

    # Write matching once for best run
    lines = formatMatching(bestN, bestMatching)
    with open(outputFile, "w") as f:
        f.write("\n".join(lines) + "\n")

    return best


def timeVerifierFunction(inputFile, outputFile, repeats=3):
    # Track best time runtime over repeats
    best = float("inf")

    # Repeat verification
    for _ in range(repeats):
        t0 = time.perf_counter()
        success, message = verifyMatching(str(inputFile), str(outputFile))
        t1 = time.perf_counter()

        # Check for best time
        if not success:
            raise RuntimeError(message)

        best = min(best, t1 - t0)

    return best

def runScalability(maxPower=12):
    # Determine n values to test
    ns = [2 ** k for k in range(0, maxPower + 1)]
    matcherTimes = []
    verifierTimes = []

    # Ensure data directories exist
    scriptDir = Path(__file__).resolve().parent
    projectRoot = scriptDir.parent if scriptDir.name.lower() == "src" else scriptDir

    # Create data directories
    dataInputs = projectRoot / "data" / "inputs"
    dataOutputs = projectRoot / "data" / "outputs"
    resultsDirectory = projectRoot / "results"

    dataInputs.mkdir(parents=True, exist_ok=True)
    dataOutputs.mkdir(parents=True, exist_ok=True)
    resultsDirectory.mkdir(parents=True, exist_ok=True)

    # Run scalability tests
    for n in ns:
        # Define input and output file paths
        inputFile = dataInputs / f"n{n}.in"
        outputFile = dataOutputs / f"n{n}.out"

        createRandomInputFile(inputFile, n)

        # Determine number of repeats based on n
        repeats = 3 if n <= 512 else 1

        timeMatch = timeGaleShapley(inputFile, outputFile, repeats=repeats)
        matcherTimes.append(timeMatch)

        timeVerify = timeVerifierFunction(inputFile, outputFile, repeats=repeats)
        verifierTimes.append(timeVerify)

        # Print results for this n
        print(f"n={n:4d}  matcher={timeMatch:.6f}s  verifier={timeVerify:.6f}s")

    # Save results to CSV
    csvPath = resultsDirectory / "runtime_data.csv"
    with open(csvPath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "matcher_time_seconds", "verifier_time_seconds"])
        for n, mTime, vTime in zip(ns, matcherTimes, verifierTimes):
            writer.writerow([n, mTime, vTime])

    print(f"Saved runtime data to {csvPath}")

    # Matcher plot
    plt.figure()
    plt.plot(ns, matcherTimes, marker="o")
    plt.xlabel("n (hospitals/students)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Matcher Runtime vs. n")
    plt.xscale("log", base=2)
    plt.grid(True, which="both")

    matcherPlotPath = resultsDirectory / "matcher_runtime_vs_n.png"
    plt.savefig(matcherPlotPath, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved plot to {matcherPlotPath}")
    
    # Verifier plot
    plt.figure()
    plt.plot(ns, verifierTimes, marker="o")
    plt.xlabel("n (hospitals/students)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Verifier Runtime vs. n")
    plt.xscale("log", base=2)
    plt.grid(True, which="both")

    verifierPlotPath = resultsDirectory / "verifier_runtime_vs_n.png"
    plt.savefig(verifierPlotPath, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved plot to {verifierPlotPath}")
