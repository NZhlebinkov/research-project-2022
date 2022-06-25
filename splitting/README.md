This is part of the [Research Project](https://github.com/TU-Delft-CSE/Research-Project) 2022 of [TU Delft](https://github.com/TU-Delft-CSE).

# Split script

This can use the results from the extraction script to calculate an 80/20 split for each speaker group.

Recommended use:

- pass as parameters the names of all speaker groups you would like to have an even split on.
  - E.g. `python split80_20.py sp_1_M_timesum sp_1_F_timesum` would give a train and test set for the _children_ group, with a preserved ratio of male to female
  - Ideally, use on the resulting files from the script from the folder `extraction`
- The files `finalTest` and `finalTrain` would contain a list of speakers based on which you can create the 4 needed files for kaldi to run (wav.scp, segments, text, utt2spk)
