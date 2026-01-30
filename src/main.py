# simple menu cli for matcher and verifier

from inputParser import parseInput, validateInput
from matcher import galeShapley, formatMatching
from verifier import verifyMatching

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

# menu loop to select mode
def main():
    while True:
        print("")
        print("stable matching menu")
        print("1) match (gale-shapley)")
        print("2) verify (check matching)")
        print("3) exit")
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
            break
        else:
            print("invalid option, try again")


if __name__ == "__main__":
    main()
