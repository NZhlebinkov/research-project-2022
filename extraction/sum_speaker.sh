# CREDITS to Alves Marinov

while IFS= read -r line;
do
   REGEX="^${line}.*"
   TIMESUM=$(grep -E "${REGEX}" ../segments_region | cut -d '-' -f3,4- | cut -d ' ' -f 1 | tr '-' ' ' | awk '{print $2 - $1}' | paste -sd+ | bc)
   echo "${line} ${TIMESUM}" >> $2 
done < $1