import os
import librosa
import soundfile
from vtlp import VtlpAug
from os import listdir
from os.path import isfile, join

sourceDir = "../../corpus-data/wavs/q/"
outputDir = "../augmented/"
onlyFiles = [f for f in listdir(sourceDir) if isfile(join(sourceDir, f))]

print("Filenames retrieved")

for fileName in onlyFiles:
    filePath = join(sourceDir, fileName)
    data, samplerate = librosa.load(filePath)

    aug = VtlpAug(samplerate, factor_range=(0.9, 1.1), zone=(0, 1), coverage=1)
    augmented, warp_factor = aug.augment(data)

    outputPath = join(outputDir, fileName)
    soundfile.write(outputPath, augmented, samplerate)
    print("This is warp: " + str(warp_factor))

# fileNames = open("../warps")
