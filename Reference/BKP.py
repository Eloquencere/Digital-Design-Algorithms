def d2b(Decimal, resolution=0):
    Binary = ""
    count = 0
    while Decimal != 0:
        bin = str(Decimal % 2)
        Binary += bin
        Decimal //= 2
        if bin == "1":
            count += 1
    if resolution:
        Binary += "0" * (resolution - len(Binary))  # Justification
    return [count, Binary[::-1]]


def Comparator(a, b):
    out = ""
    count = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            out += a[i]
        else:
            out += "-"
            count += 1
            if count > 1:
                return False
    return out


Minterms = []
BinaryRepresentation = []

InputMinTerms = list(map(int, input("Enter min-terms: ").split(",")))


def d2bList(lst):
    global Minterms
    global BinaryRepresentation
    MintermDict = {}
    BinaryDict = {}
    largestBinary = len(d2b(max(lst))[1])
    for element in lst:
        count, BinNum = d2b(element, largestBinary)
        if count not in MintermDict:
            MintermDict[count] = [[element]]
            BinaryDict[count] = [BinNum]
        else:
            MintermDict[count].append([element])
            BinaryDict[count].append(BinNum)
    Minterms = list((MintermDict.values()))
    BinaryRepresentation = list((BinaryDict.values()))


d2bList(InputMinTerms)
print(Minterms)
print(BinaryRepresentation)  # Display

# Catch prime implicants along the way & convert to recurrsion
def Simplification():
    global Minterms
    global BinaryRepresentation
    MintermPrimImpl = []
    BinaryPrimImpl = []
    while True:
        TempBinRep = []
        TempMinterm = []
        for Group in range(len(BinaryRepresentation) - 1):
            GroupBinary = []
            GroupMinterm = []
            for CurrentBinary in range(len(BinaryRepresentation[Group])):
                for AdjacentBinary in range(len(BinaryRepresentation[Group + 1])):
                    ReducedBinary = Comparator(
                        BinaryRepresentation[Group][CurrentBinary],
                        BinaryRepresentation[Group + 1][AdjacentBinary],
                    )
                    if ReducedBinary == False:
                        continue
                    if ReducedBinary not in GroupBinary:
                        GroupBinary.append(ReducedBinary)
                        GroupMinterm.append(
                            Minterms[Group][CurrentBinary]
                            + Minterms[Group + 1][AdjacentBinary]
                        )
            if GroupBinary != []:
                TempBinRep.append(GroupBinary)
                TempMinterm.append(GroupMinterm)
        if TempBinRep == []:
            break
        BinaryRepresentation = TempBinRep
        Minterms = TempMinterm
        print(Minterms)
        print(BinaryRepresentation)  # Display
    if BinaryPrimImpl != []:
        BinaryRepresentation += BinaryPrimImpl
        Minterms += MintermPrimImpl


Simplification()

# Simplify this
def EssentialPrimeImpl():
    global Minterms
    global BinaryRepresentation
    Repeated = {}
    EssentialBin = []
    for Group in Minterms:
        for lst in Group:
            for element in lst:
                if element in Repeated:
                    Repeated[element] += 1
                else:
                    Repeated[element] = 1
    for key in Repeated:
        if Repeated[key] == 1:
            for Group in range(len(Minterms)):
                for lst in range(len(Minterms[Group])):
                    for element in range(len(Minterms[Group][lst])):
                        if (
                            Minterms[Group][lst][element] == key
                            and BinaryRepresentation[Group][lst] not in EssentialBin
                        ):
                            EssentialBin += BinaryRepresentation[Group]
    BinaryRepresentation = EssentialBin


EssentialPrimeImpl()
print(BinaryRepresentation)  # Display


def SOP():
    global BinaryRepresentation
    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out = ""
    for binary in BinaryRepresentation:
        for dig in range(len(binary)):
            if binary[dig] == "-":
                continue
            out += alphabets[dig]
            if binary[dig] == "0":
                out += "'"
        if binary != BinaryRepresentation[-1]:
            out += " + "
    return out


print(SOP())  # Display
