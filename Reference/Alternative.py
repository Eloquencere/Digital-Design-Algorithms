# Initializing table from input of minterms list
# Table format as Dictionary ->  { group : [ (minterm, binaryMinterm), (minterm2, binaryMinterm2) ...], group2 : [...] }
def initializeTable(minterms_List):
    binaryMaxLength = len(str(bin(max(minterms_List))[2:]))
    table = dict()
    primeImplicants = []
    for minterm in minterms_List:
        binaryMinterm = dec2bin(minterm, binaryMaxLength)
        onesCount = binaryMinterm.count("1")
        if onesCount not in table:
            table[onesCount] = [([minterm], binaryMinterm)]
        else:
            table[onesCount].append(([minterm], binaryMinterm))
    return table, primeImplicants


# Converts decimal to binary of desired length of representation
def dec2bin(decimalNumber, length):
    value = str(bin(decimalNumber)[2:])
    zeroes = length - len(value)
    return zeroes * "0" + value


def QuineMcCluskey(table, primeImplicants):
    displayTable(table, primeImplicants)
    tableNew = dict()
    newlyAddedBinaries = []
    for group in table:
        if group == max(list(table.keys())):
            continue
        for minterm1 in table[group]:
            if group + 1 not in table.keys():
                break
            for minterm2 in table[group + 1]:
                bitDiffBinary = compareBinaryMinterms(minterm1[1], minterm2[1])
                if not bitDiffBinary or bitDiffBinary in newlyAddedBinaries:
                    continue
                newlyAddedBinaries.append(bitDiffBinary)
                if group not in tableNew:
                    tableNew[group] = [(minterm1[0] + minterm2[0], bitDiffBinary)]
                else:
                    tableNew[group].append((minterm1[0] + minterm2[0], bitDiffBinary))

    if tableNew != {}:
        primeImplicants = findPrimeImplicants(table, tableNew, primeImplicants)
        return QuineMcCluskey(tableNew, primeImplicants)

    for minterms in table.values():
        for minterm in minterms:
            primeImplicants.append(minterm)
    print("Prime Implicants:", primeImplicants, "\n\n")
    displayPrimeImplicantsTable(primeImplicants)
    essentialPrimeImplicants = findEssentialPrimeImplicants(primeImplicants)
    print("Essential Prime Implicants:", essentialPrimeImplicants, "\n")
    displaySimplifiedBooleanFunction(essentialPrimeImplicants)
    return table, essentialPrimeImplicants


def compareBinaryMinterms(binary1, binary2):
    difference = 0
    new_binary = ""
    for idx in range(len(binary1)):
        if binary1[idx] != binary2[idx]:
            difference += 1
            new_binary += "-"
        else:
            new_binary += binary1[idx]

    if difference == 1:
        return new_binary
    return False


def findPrimeImplicants(table, tableNew, primeImplicants):
    tableNewSet = set()

    for minterms in tableNew.values():
        for minterm in minterms:
            for number in minterm[0]:
                tableNewSet.add(number)

    for minterms in table.values():
        for minterm in minterms:
            if len(set(minterm[0]).intersection(tableNewSet)) != len(set(minterm[0])):
                primeImplicants.append(minterm)

    return primeImplicants


def findEssentialPrimeImplicants(primeImplicants):
    fullList = []
    essentialPrimeImplicants = []
    for minterm in primeImplicants:
        fullList.extend(minterm[0])

    for minterm in primeImplicants:
        tempList = fullList[:]
        compareSet = deleteItems(minterm[0], tempList)
        if set(minterm[0]).intersection(compareSet) != set(minterm[0]):
            essentialPrimeImplicants.append(minterm)
        else:
            for number in minterm[0]:
                fullList.remove(number)

    return essentialPrimeImplicants


def deleteItems(sublist, fullList):
    for item in sublist:
        fullList.remove(item)
    return fullList


# All display functions below
def displayTable(table, primeImplicants):
    longestMinterm = 0
    for minterms in table.values():
        for minterm in minterms:
            if len(str(minterm[0])) > longestMinterm:
                longestMinterm = len(str(minterm[0]))
    if longestMinterm < 8:
        longestMinterm = 8
    longestMintermCount = len(list(table.values())[-1][-1][0])
    if longestMintermCount != 1:
        print("Prime Implicants:", primeImplicants)
        print("\n")
    print("Table", longestMintermCount.bit_length())
    print("=" * (longestMinterm + 32))
    print(
        "Group",
        "|",
        "Minterm",
        (" " * abs(8 - longestMinterm)),
        "|",
        "Binary Representation",
    )
    for group in table:
        print("-" * (longestMinterm + 32))
        print(str(group) + "     |", end=" ")
        groupcounter = 0
        for minterm, binary in table[group]:
            groupcounter += 1
            print(
                str(minterm) + " " * (abs(longestMinterm - len(str(minterm)))),
                "|",
                end=" ",
            )
            print(binary)
            if groupcounter != len(table[group]):
                print("      |", end=" ")
    print("=" * (longestMinterm + 32))


def displayPrimeImplicantsTable(primeImplicants):
    fullList = []
    longestMinterm = 0
    for minterm in primeImplicants:
        fullList.extend(minterm[0])
        if len(str(minterm[0])) > longestMinterm:
            longestMinterm = len(str(minterm[0]))
    fullList = sorted(list(set(fullList)))
    print("Prime Implicants Table")
    if longestMinterm < 8:
        longestMinterm = 8
    tableWidth = longestMinterm + (len(str(fullList))) + len(fullList) + 2
    print("=" * tableWidth)
    print("Minterm", (" " * abs(8 - longestMinterm)), "|", end=" ")
    for number in fullList:
        print(number, "|", end=" ")
    print("")
    print("-" * tableWidth)
    for primeImplicant in primeImplicants:
        print(
            str(primeImplicant[0])
            + " " * abs(longestMinterm - len(str(primeImplicant[0]))),
            "|",
            end=" ",
        )
        for number in fullList:
            if number in primeImplicant[0]:
                print("X" + " " * (len(str(number)) - 1), end=" | ")
            else:
                print(" " + " " * (len(str(number)) - 1), end=" | ")
        print("")
    print("=" * tableWidth, end="\n\n")


def displaySimplifiedBooleanFunction(essentialPrimeImplicants):
    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    booleanFunctionList = []
    for primeImplicant in essentialPrimeImplicants:
        binary = primeImplicant[1]
        currentTerm = ""
        for digit in range(len(binary)):
            if binary[digit] == "-":
                continue
            if binary[digit] == "1":
                currentTerm += alphabets[digit]
            elif binary[digit] == "0":
                currentTerm += alphabets[digit] + "'"
        booleanFunctionList.append(currentTerm)

    print("Simplified Boolean Function:", " + ".join(sorted(booleanFunctionList)))


mintermsList = [0, 4, 5, 7, 8, 11, 12, 15]
# mintermsList = [0, 1, 2, 4, 6, 8, 9, 11, 13, 15]
# mintermsList = [20, 28, 52, 60]
# mintermsList = [2, 6, 8, 9, 10, 11, 14, 15]
# mintermsList = [4, 8, 9, 10, 11, 12, 14, 15]
# mintermsList = [3, 7, 11, 12, 13, 14, 15]

Table, PrimeImplicants = initializeTable(mintermsList)
QuineMcCluskey(Table, PrimeImplicants)
