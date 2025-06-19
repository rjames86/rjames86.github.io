:::bash
DOWNLOADS="$HOME/Downloads"

RECENT=$(mdls -name kMDItemFSName -name kMDItemDateAdded $DOWNLOADS/* | \
sed 'N;s/\n//' | \
awk '{print $3 " " $4 " " substr($0,index($0,$7))}' | \
sort -r | \
cut -d'"' -f2 | \
head -n1)

open -R "$DOWNLOADS/$RECENT"
