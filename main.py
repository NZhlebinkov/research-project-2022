import librosa
import soundfile
from vtlp import VtlpAug

data, samplerate = librosa.load("../fn000490.wav")

aug = VtlpAug(samplerate, factor_range=(0.9, 1.1), zone=(0, 1), coverage=1)
augmented, warp_factor = aug.augment(data)
soundfile.write("../fn000490_localAug.wav", augmented, samplerate)
print("This is warp: " + str(warp_factor))
