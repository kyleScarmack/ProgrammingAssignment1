# simple menu cli for matcher and verifier

from inputParser import parseInput, validateInput
from matcher import galeShapley, formatMatching
from verifier import verifyMatching
from scalability import runScalability

# write output lines to file or stdout
def writeLines(lines, outputFile):
    if outputFile:
        with open(outputFile, "w") as file:
            file.write("\n".join(lines))
            file.write("\n")
    else:
        for line in lines:
            print(line)

# run matching mode with interactive prompts
def runMatch():
    print("match mode")
    print("enter input file path (e.g. tests/example2.in)")
    inputFile = input("> ").strip()
    if not inputFile:
        print("input file is required")
        return

    print("enter output file path (leave blank to print to console)")
    outputFile = input("> ").strip() or None

    n, hospitalPrefs, studentPrefs = parseInput(inputFile)
    validateInput(n, hospitalPrefs, studentPrefs)

    matching, _ = galeShapley(n, hospitalPrefs, studentPrefs)
    lines = formatMatching(n, matching)
    writeLines(lines, outputFile)

# run verify mode with interactive prompts
def runVerify():
    print("verify mode")
    print("enter input file path (e.g. tests/example2.in)")
    inputFile = input("> ").strip()
    if not inputFile:
        print("input file is required")
        return

    print("enter matching file path (e.g. tests/example2.out)")
    matchingFile = input("> ").strip()
    if not matchingFile:
        print("matching file is required")
        return

    success, message = verifyMatching(inputFile, matchingFile)
    print(message)

    if not success:
        return
    
# run scalability mode with interactive prompts
def runScalabilityMenu():
    print("scalability mode")
    print("enter maximum power k for n=2^k (e.g. 12 -> 2^12 = 4096)")
    s = input("> ").strip()

    try:
        maxPower = int(s) if s else 12  # default 12 up to 4096
        if maxPower < 0:
            raise ValueError
    except ValueError:
        print("invalid input; using default max power = 12 (up to 4096)")
        maxPower = 12

    runScalability(maxPower)


# menu loop to select mode
def main():
    while True:
        print("")
        print("stable matching menu")
        print("1) match (gale-shapley)")
        print("2) verify (check matching)")
        print("3) scalability (timing + plots)")
        print("4) exit")
        choice = input("> ").strip()

        if choice == "1":
            try:
                runMatch()
            except Exception as exc:
                print(f"ERROR: {exc}")
        elif choice == "2":
            try:
                runVerify()
            except Exception as exc:
                print(f"ERROR: {exc}")
        elif choice == "3":
            try:
                runScalabilityMenu()
            except Exception as exc:
                print(f"ERROR: {exc}")
        elif choice == "4":
            break
        else:
            print("invalid option, try again")


if __name__ == "__main__":
    main()
