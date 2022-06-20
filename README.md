This is part of the [Research Project](https://github.com/TU-Delft-CSE/Research-Project) 2022 of [TU Delft](https://github.com/TU-Delft-CSE).

# Theme of research

The title of the paper associated with this repo is "Improving Northern Regional Dutch Speech Recognition by Adapting Perturbation-based Data Augmentation". It uses [VTLP](https://pdfs.semanticscholar.org/3de0/616eb3cd4554fdf9fd65c9c82f2605a17413.pdf) (vocal tract length perturbation) on the [JASMIN-CGN](https://aclanthology.org/L06-1141/) - a corpus of accented Dutch speech. ASR systems are trained using [kaldi](https://www.danielpovey.com/files/2011_asru_kaldi.pdf).

# Structure of this repo

- In `customVTLP` is the script to execute VTLP on a set of speech recordings.
- `wav2warp` is the set of warp factors used to get the results seen in my paper
