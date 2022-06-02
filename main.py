import os
import librosa
import soundfile
from vtlp import VtlpAug

fileNames = open("../wavSource")

for fileName in fileNames:
    fileName = str.strip(fileName)
    filePath = "../" + fileName
    data, samplerate = librosa.load(filePath)

    aug = VtlpAug(samplerate, factor_range=(0.9, 1.1), zone=(0, 1), coverage=1)
    augmented, warp_factor = aug.augment(data)

    outputPath = "../augmented/" + fileName
    soundfile.write(outputPath, augmented, samplerate)
    print("This is warp: " + str(warp_factor))
