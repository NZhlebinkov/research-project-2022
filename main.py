import os
import librosa
import soundfile
from vtlp import VtlpAug
from os import listdir
from os.path import isfile, join

sourceDir = "../../corpus-data/wavs/t/"
outputDir = "../augmented/"
onlyFiles = [f for f in listdir(sourceDir) if isfile(join(sourceDir, f))]

print("Filenames retrieved")

warpFactors = {}

for fileName in onlyFiles:
    filePath = join(sourceDir, fileName)
    data, samplerate = librosa.load(filePath)

    aug = VtlpAug(samplerate, factor_range=(0.9, 1.1), zone=(0, 1), coverage=1)
    augmented, warpFactor = aug.augment(data)
    warpFactors[fileName] = warpFactor

    outputPath = join(outputDir, fileName)
    soundfile.write(outputPath, augmented, samplerate)
    print(fileName + " warped by " + str(warpFactor))

print("Finalized warps, creating wav2warp")
wav2warpArray = [spk + " " + str(warp) for spk, warp in warpFactors.items()]
print(wav2warpArray)
wav2warp = "\n".join(wav2warpArray)
print(wav2warp)
# fileNames = open("../warps")
