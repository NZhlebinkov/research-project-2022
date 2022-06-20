import sys
import librosa
import soundfile
from vtlp import VtlpAug
from os import listdir
from os.path import isfile, join

sourceDir = "../../corpus-data/wavs/t/"
outputDir = "../augmented/t/"

try:
    onlyFiles = [f for f in listdir(sourceDir) if isfile(join(sourceDir, f))]
except:
    print("Couldn't load file names from the folder " + str(sourceDir))
    sys.exit(-1)

print("Filenames retrieved")

try:
    warpFactors = {}

    for fileName in onlyFiles:
        filePath = join(sourceDir, fileName)
        data, samplerate = librosa.load(filePath, sr=16000)

        aug = VtlpAug(samplerate, factor_range=(0.9, 1.1), zone=(0, 1), coverage=1)
        augmented, warpFactor = aug.augment(data)
        warpFactors[fileName] = warpFactor

        outputName = fileName.replace(".wav", "vtlp.wav")
        outputPath = join(outputDir, outputName)
        soundfile.write(outputPath, augmented, samplerate)
        print(outputName + " warped by " + str(warpFactor))

    print("Finalized warps, creating wav2warp")
    wav2warpArray = [spk + " " + str(warp) for spk, warp in warpFactors.items()]
    wav2warpContent = "\n".join(wav2warpArray)
    wav2warpFile = open(join(outputDir, "wav2warp"), "w")
    wav2warpFile.write(wav2warpContent)
    wav2warpFile.close()
except:
    print("Something went wrong while augmenting")
    sys.exit(-1)


print("Completed successfully")
sys.exit()
