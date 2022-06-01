# from nlpaug.augmenter.audio import VtlpAug
import librosa
import soundfile
from custom_vtlp import VtlpAug

data, samplerate = librosa.load("../fn000490.wav")

aug = VtlpAug(samplerate, factor_range=(0.9, 1.1), zone=(0, 1), coverage=1)
augmented = aug.augment(data)
soundfile.write("../fn000490_localAug.wav", augmented, samplerate)
