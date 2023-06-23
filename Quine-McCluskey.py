def compare(a, b):
    out = ""
    BitDifference = 0
    for index in range(len(a)):
        if a[index] == b[index]:
            out += a[index]
            continue
        out += "-"
        BitDifference += 1
        if BitDifference > 1:
            return False
    return out


Minterms = []
BinaryRepresentation = []
Matches = []
# dont'care
UserIn = input("Enter min-terms: ").split("+")
InputMinTerms = list(set(map(int, UserIn[0].split(","))))
MinTerms = InputMinTerms
if len(UserIn) > 1:
    DontCare = list(set(map(int, UserIn[1].split(","))))
    MinTerms += DontCare
    MinTerms = sorted(MinTerms)


def InitialiseTable(lst):
    global Minterms
    global BinaryRepresentation
    global Matches
    MintermDict = {}
    BinaryDict = {}
    MatchesDict = {}
    largestBinary = len(bin(max(lst))[2:])
    for element in lst:
        BinNum = bin(element)[2:].zfill(largestBinary)
        Count1s = BinNum.count("1")
        MintermDict[Count1s] = MintermDict.get(Count1s, []) + [str(element)]
        BinaryDict[Count1s] = BinaryDict.get(Count1s, []) + [BinNum]
        MatchesDict[Count1s] = MatchesDict.get(Count1s, []) + [False]
    Minterms = list((MintermDict.values()))
    BinaryRepresentation = list((BinaryDict.values()))
    Matches = list((MatchesDict.values()))


InitialiseTable(MinTerms)
# print(Minterms)
# print(BinaryRepresentation)
# print(Matches)

MintermPrimImpl = []
BinaryPrimImpl = []


def Simplification():
    global Minterms
    global BinaryRepresentation
    global Matches
    global MintermPrimImpl
    global BinaryPrimImpl
    while True:
        TempBinRep = []
        TempMinterm = []
        TempMatches = []
        for Group in range(len(BinaryRepresentation) - 1):
            GroupBinary = []
            GroupMinterm = []
            GroupMatch = []
            for CurrentBinary in range(len(BinaryRepresentation[Group])):
                for AdjacentBinary in range(len(BinaryRepresentation[Group + 1])):
                    ReducedBinary = compare(
                        BinaryRepresentation[Group][CurrentBinary],
                        BinaryRepresentation[Group + 1][AdjacentBinary],
                    )
                    if ReducedBinary is not False:
                        GroupBinary.append(ReducedBinary)
                        GroupMinterm.append(
                            Minterms[Group][CurrentBinary]
                            + ","
                            + Minterms[Group + 1][AdjacentBinary]
                        )
                        GroupMatch.append(False)
                        Matches[Group][CurrentBinary] = True
                        Matches[Group + 1][AdjacentBinary] = True
            if GroupBinary != []:
                TempBinRep.append(GroupBinary)
                TempMinterm.append(GroupMinterm)
                TempMatches.append(GroupMatch)
        for Group in range(len(Matches)):  # Pick up prime implicants
            for CurrentState in range(len(Matches[Group])):
                if (
                    Matches[Group][CurrentState] is False
                    and BinaryRepresentation[Group][CurrentState] not in BinaryPrimImpl
                ):
                    BinaryPrimImpl.append(BinaryRepresentation[Group][CurrentState])
                    MintermPrimImpl.append(Minterms[Group][CurrentState])
        if TempBinRep == []:
            break
        BinaryRepresentation = TempBinRep
        Minterms = TempMinterm
        Matches = TempMatches


Simplification()
print(MintermPrimImpl)
print(BinaryPrimImpl)


EssentialImpl = []
lst = []
for i in MintermPrimImpl:
    lst += list(map(int, i.split(",")))
for j in MintermPrimImpl:
    x = list(map(int, j.split(",")))
    templst = lst[:]
    for element in x:
        templst.remove(element)
    if set(x).intersection(set(templst)) != set(x):
        EssentialImpl.append(j)
    else:
        for num in x:
            lst.remove(num)

print(EssentialImpl)
