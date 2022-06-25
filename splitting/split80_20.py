import pandas as pd
import io, sys


class Speaker:
    spId = ""
    spTime = 0.0

    def __init__(self, spTuple):
        self.spId = spTuple[0]
        self.spTime = spTuple[1]


class SpeakerSum:
    total = 0.0
    speakers = set([])

    def __init__(self, total, speakers):
        self.total = total
        self.speakers = speakers


# ! INSTRUCTIONS FOR USE !
# You can pass 1 or more filenames as a parameter
# e.g. `python splitScript.py sp_1_M_timesum`

if len(sys.argv) == 1:  # If no filenames were given
    sys.exit("You need to pass at least 1 file name as parameter")

# Initialize a dataframe to hold all training speakers
finalTrain = pd.DataFrame({"id": [], "time": []})
finalTest = pd.DataFrame({"id": [], "time": []})

for sourceFileName in sys.argv[1:]:
    # Read the file with all speakers of a category
    sourceFile = open(sourceFileName, "r")
    speakersString = "id time\n" + sourceFile.read()
    sourceFile.close()

    # Create a pandas dataframe for easy manipulation of the data
    spDf = pd.read_table(io.StringIO(speakersString), delim_whitespace=True)
    if len(spDf.columns) != 2:
        print(spDf)
        sys.exit(
            "Wrong format of file given. Place speaker id on column 1 and time on column 2"
        )

    # Goal: "Sum numbers in array X in such a way so as to be closest to a number N"
    # Initially generate the 80% set of speakers from spDf
    # https://stackoverflow.com/questions/16022205/how-do-i-find-the-closest-possible-sum-of-an-arrays-elements-to-a-particular-va
    speakers = list(map(lambda spTuple: Speaker(spTuple), spDf.values.tolist()))
    sums = set([])  # Empty set
    optimum = SpeakerSum(0, set([]))
    desired = spDf["time"].sum() / 100 * 80
    # Pass through each speaker and sum with all previously calculated sums
    for i in speakers:
        newSums = set([])
        for s in sums:
            #
            newTotal = s.total + i.spTime
            newSpeakers = s.speakers.copy()
            newSpeakers.add(i)
            speakerSum = SpeakerSum(newTotal, newSpeakers)

            if newTotal < desired:
                newSums.add(speakerSum)

            if abs(desired - newTotal) < abs(desired - optimum.total):
                optimum = speakerSum
        sums.add(SpeakerSum(i.spTime, set([i])))
        sums.update(newSums)

    # Convert 80% set to a dataframe
    sp80data = map(lambda sp: [sp.spId, sp.spTime], optimum.speakers)
    sp80 = pd.DataFrame(
        data=sp80data, index=range(0, len(optimum.speakers)), columns=["id", "time"]
    )

    # Generate 20% set based on who's left
    sp20 = spDf[~spDf.apply(tuple, 1).isin(sp80.apply(tuple, 1))]

    trainPercent = sp80["time"].sum() / spDf["time"].sum() * 100
    testPercent = sp20["time"].sum() / spDf["time"].sum() * 100
    print("Algorithm results:\ntrain is " + str(round(trainPercent, 2)) + "%")
    print("test is " + str(round(testPercent, 2)) + "%")

    finalTrain = pd.concat([finalTrain, sp80], ignore_index=True, copy=False)
    finalTest = pd.concat([finalTest, sp20], ignore_index=True, copy=False)

    # Write out the results to 2 files (keeps the column names in the first row)
    resultingTrain = open(sourceFileName + "_80", "w")
    resultingTrain.write(sp80.to_string(index=False))
    resultingTrain.close()
    resultingTest = open(sourceFileName + "_20", "w")
    resultingTest.write(sp20.to_string(index=False))
    resultingTest.close()
resultingTrain = open("finalTrain", "w")
resultingTrain.write(finalTrain.to_string(index=False))
resultingTrain.close()
resultingTest = open("finalTest", "w")
resultingTest.write(finalTest.to_string(index=False))
resultingTest.close()
sys.exit()
