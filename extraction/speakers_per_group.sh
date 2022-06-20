# CREDITS to Alves Marinov

# REPLACE THE FOLLOWING ARGUMENTS
# Replace with your NetID
NETID=nzhlebinkov
# Replace 1 with your region's corresponding code (either 2, 3, 4 etc. for N1, N2 ...)
TYPE=3


ORIGDATA="/tudelft.net/staff-bulk/ewi/insy/SpeechLab/RP2022/$NETID/kaldi/egs/jasmin_${NETID}/asr0/orig_data/jas_All"
LOCALDATA="/tudelft.net/staff-bulk/ewi/insy/SpeechLab/RP2022/$NETID/kaldi/egs/jasmin_${NETID}/asr0/data/local/data"

SCRIPTLOC=$(pwd)

YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


echo -e "${YELLOW}Begin region extraction for N${TYPE}!${NC}"
cd $LOCALDATA
echo -e "${YELLOW}Extracting region speaker IDs!${NC}"
grep -E "^[[:upper:]][[:digit:]]{6}.N${TYPE}.\>" spk2dialectregion_nl > spk_region
# This will extract only the speakers' codes (without the dialect types at the end )
grep -o -e "N0....." -e "N1....." spk_region > spk_region_2
#rm spk_region
mv spk_region spk_region_old
mv spk_region_2 spk_region


# Now extract the regional speakers from the 4 files Tanvina mentioned
cd $ORIGDATA
echo -e "${YELLOW}Extracting 4 main files (segments, wav, text, utt2spk)_region for the region as a whole!${NC}"

grep -Fw -f $LOCALDATA/spk_region segments > segments_region
# wav identifiers are dependent on  these IDs
cat segments_region | awk '{print $2}' > wav_prep
grep -Fw -f wav_prep wav.scp > wav_region.scp
grep -Fw -f $LOCALDATA/spk_region text > text_region
grep -Fw -f $LOCALDATA/spk_region utt2spk > utt2spk_region
#rm wav_prep

echo -e "${YELLOW}Extracting speaker information!${NC}"
# From corpusdocumentation.pdf pp.14-15 - we can use this for sanity checks and ideas for data partitioning
SPEAKERS_FILE="/tudelft.net/staff-bulk/ewi/insy/SpeechLab/RP2022/JASMIN/Data/data/meta/text/nl/speakers.txt"
grep -Fw -f $LOCALDATA/spk_region $SPEAKERS_FILE > speakers_extracted
# Split on tabs and preserve only the fields of interest
cut -d$'\t' -f1,3,4,6,9,11,13- speakers_extracted > speakers_filtered

if [ -d "data_segmentation" ]
then
	rm -r data_segmentation
fi

echo -e "${YELLOW}Creating data_segmentation folder in $(pwd)/${NC}"
mkdir data_segmentation
cd data_segmentation

echo -e "${YELLOW}Separating speakers based on age and gender!${NC}"
# Extract group 1 speakers (children) from dataset
grep -E "^[[:upper:]][[:digit:]]{6}[[:space:]]M[[:space:]][[:digit:]]{0,2}[[:space:]]1[[:space:]]*" ../speakers_filtered | cut -d$'\t' -f 1 > speakers_1_M
grep -E "^[[:upper:]][[:digit:]]{6}[[:space:]]F[[:space:]][[:digit:]]{0,2}[[:space:]]1[[:space:]]*" ../speakers_filtered | cut -d$'\t' -f 1 > speakers_1_F
# Extract group 2 speakers (children) from dataset
grep -E "^[[:upper:]][[:digit:]]{6}[[:space:]]M[[:space:]][[:digit:]]{0,2}[[:space:]]2[[:space:]]*" ../speakers_filtered | cut -d$'\t' -f 1 > speakers_2_M
grep -E "^[[:upper:]][[:digit:]]{6}[[:space:]]F[[:space:]][[:digit:]]{0,2}[[:space:]]2[[:space:]]*" ../speakers_filtered | cut -d$'\t' -f 1 > speakers_2_F
# Extract group 5 speakers (elderly) from dataset
grep -E "^[[:upper:]][[:digit:]]{6}[[:space:]]M[[:space:]][[:digit:]]{0,2}[[:space:]]5[[:space:]]*" ../speakers_filtered | cut -d$'\t' -f 1 > speakers_5_M
grep -E "^[[:upper:]][[:digit:]]{6}[[:space:]]F[[:space:]][[:digit:]]{0,2}[[:space:]]5[[:space:]]*" ../speakers_filtered | cut -d$'\t' -f 1 > speakers_5_F

echo -e "${YELLOW}Calculating actual speaking time based on previously created groups!${NC}"
cp $SCRIPTLOC/sum_speaker.sh ./
# Sum up all of the actual speaking time for each speaker id based on their group
# If you end up with different categories you can add/change lines to fit your data
./sum_speaker.sh speakers_1_M sp_1_M_timesum
./sum_speaker.sh speakers_1_F sp_1_F_timesum
./sum_speaker.sh speakers_2_M sp_2_M_timesum
./sum_speaker.sh speakers_2_F sp_2_F_timesum
./sum_speaker.sh speakers_5_M sp_5_M_timesum
./sum_speaker.sh speakers_5_F sp_5_F_timesum

rm sum_speaker.sh

echo  -e "${GREEN}Region extraction DONE!${NC}"