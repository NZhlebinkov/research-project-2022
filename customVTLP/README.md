This is part of the [Research Project](https://github.com/TU-Delft-CSE/Research-Project) 2022 of [TU Delft](https://github.com/TU-Delft-CSE).

# VTLP augmentation script

This is a modified version of the code from [nlpaug](https://github.com/makcedward/nlpaug), which is based on [the work of Jaitly and Hinton](https://pdfs.semanticscholar.org/3de0/616eb3cd4554fdf9fd65c9c82f2605a17413.pdf) -
http://www.cs.toronto.edu/~hinton/absps/perturb.pdf

VTLP (vocal tract length perturbation) is used to modify speech recordings and simulate a different vocal tract length.

## How to use:

Two fields in `main.py`:

- `sourceDir` signifies the folder where the original speech recordings are
- `outputDir` signifies the folder where to write the modified recording

Modify these two fields to point to the appropriate directories, then run `python main.py` from the root of this project.

## Technical details

- The **samplerate** used for the files (input and output) **is 16kHz**. If the original recordings have a different samplerate they would be resampled.
- All files used so far have been mono (single channel), so I'm not certain how the script will perform for stereo (dual channel)
