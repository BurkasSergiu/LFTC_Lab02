import re


identifiers = "^[a-zA-Z]{1,16}$"
vectorIdentifiers = ["^[a-zA-Z]{1,16}\\[[1-9][0-9]*\\]$", "^[a-zA-Z]{1,16}\\[[a-zA-Z]{1,16}\\]$"]
constans = "[0-9]+\\.{0,1}[0-9]+"
keywords = {"begin_prog": "<PROGRAM_START>", "end_prog": "<PROGRAM_END>",
            "integer": "<DATA_TYPE>", "float": "<DATA_TYPE>", "double": "<DATA_TYPE>",
            "vector": "<USER_DEFINED_DATA_TYPE>",
            "read": "<INSTR_I>", "write": "<INSTR_O>", ":=": "<INSTR_ASSIGN>",
            "if": "<INSTR_IF>", "while": "<INSTR_LOOP>"}
separators = [",", "((", "))", ";", "[", "]", "{", "}"]
arithmeticOperators = ["+", "-", "*", "/", "%", ":++", ":--"]
relationalOperators = ["<", "<=", ">", ">=", "==", "!="]
logicalOperators = ["&&", "||"]


def parseSourceText(fileName, atoms):
    f = open(fileName, "r")
    lines = f.readlines()
    lineCount = 1

    for line in lines:
        words = line.split(" ")
        # print(words)
        for word in words:
            word = word.strip()
            if word == "":
                continue
            elif word in separators:
                atoms.append([word, lineCount])
            elif word in keywords:
                atoms.append([word, lineCount])
            elif word in re.findall(identifiers, word) or word in re.findall(vectorIdentifiers[0], word) \
                    or word in re.findall(vectorIdentifiers[1], word):
                if len(word) > 8:
                    print("ERROR: There is a lexical error at line " + str(lineCount) +
                          ": Identifier has too many characters ('" + str(word) + "').")
                    atoms = []
                    return
                atoms.append([word, lineCount])
            elif word in constans:
                atoms.append([word, lineCount])
            elif word in arithmeticOperators:
                atoms.append([word, lineCount])
            elif word in logicalOperators:
                atoms.append([word, lineCount])
            elif word in relationalOperators:
                atoms.append([word, lineCount])
            else:
                print("ERROR: There is a lexical error at line " + str(lineCount) + ": Unknown Atom ('" + str(word) + "').")
                atoms = []
                return
        lineCount += 1


def readEncodings(fileName, encodings):
    f = open(fileName, "r")
    lines = f.readlines()
    for line in lines:
        elements = line.split("\\")
        encodings[elements[0]] = elements[1]


def makeFIPandTS(encodings, atoms):
    FIP = []
    TS = {}
    count = 0
    atomsForFIP = atoms
    for atom in atoms:
        if (atom[0] not in keywords) and (atom[0] != "{") and (atom[0] != "}") \
                and (atom[0] != "begin_prog") and (atom[0] != "end_prog") and (atom[0] not in separators) \
                and (atom[0] not in arithmeticOperators):
            if atom[0] in re.findall(identifiers, atom[0]):
                if atom[0] not in TS:
                    TS[atom[0]] = count
                    count += 1
            elif atom[0] in re.findall(vectorIdentifiers[0], atom[0]) \
                    or atom[0] in re.findall(vectorIdentifiers[1], atom[0]):
                atoms = atom[0].split("[")
                atoms[1] = atoms[1][:-1]
                if atoms[0] not in TS:
                    TS[atoms[0]] = count
                    count += 1
                if atoms[1] not in TS:
                    TS[atoms[1]] = count
                    count += 1
            elif atom[0] in constans:
                if atom[0] not in TS:
                    TS[atom[0]] = count
                    count += 1
    for atom in atomsForFIP:
        if atom[0].split('[')[0] in TS.keys():
            if atom[0].split('[')[0] in re.findall(identifiers, atom[0].split('[')[0]):
                FIP.append([encodings["ID"], TS[atom[0].split('[')[0]]])
            if atom[0].isnumeric():
                FIP.append([encodings["CONST"], TS[atom[0]]])
        if atom[0] in encodings:
            FIP.append([encodings[atom[0]], -1])
    print(TS)
    print(FIP)
    # print(TS[atom[0]])
    # fileName.write("| " + atom[0] + " | " + encodings[atom[0]] + " | " + str(TS[atom[0]]) + " | ")
    # fileName.write("-----------------------------")


def checkLexicalErrors(atoms):
    for i in range(0, len(atoms) - 1):
        # print(atoms[i])
        if atoms[i][0] == atoms[i + 1][0] and atoms[i][1] == atoms[i + 1][1]:
            print("ERROR1: There is an error at line " + str(atoms[i][1]) + "('" + str(atoms[i][0]) + "')")
        if atoms[i][0] != ";" and atoms[i][1] != atoms[i + 1][1] \
                and atoms[i][0] != "{" and atoms[i][0] != "}" \
                and atoms[i][0] != "begin_prog" and atoms[i][0] != "end_prog":
            print("ERROR2: There is an error at line " + str(atoms[i][1]) + "('" + str(atoms[i][0]) + "')")


def main():
    encodingsFile = "codificare.txt"
    sourceCodeFile = "sursa.txt"
    encodings = {}
    atoms = []

    readEncodings(encodingsFile, encodings)
    parseSourceText(sourceCodeFile, atoms)
    checkLexicalErrors(atoms)
    print(atoms)
    print(encodings)
    makeFIPandTS(encodings, atoms)


main()
