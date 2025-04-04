:::bash
#!/bin/bash

FILE="$HOME/Dropbox/IFTTT/foursquare/foursquare.txt"

START=1
index=$START
IFS=$'\n'     # new field separator, the end of line
for line in $(cat $FILE)
do
    mapsurl=$(echo $line | sed -n 's/.*(\(http.*\)).*/\1/p');

    existingaddress=$(echo $line | grep -E '^.*\(http.*\)(.*\|){2,}$');

    if [[ ! $mapsurl || $existingaddress ]]; then
        (( index = index + 1 ))
        continue
    fi

    coords=$(echo $mapsurl | sed -E 's/^.+\?center=([0-9.,-]+).+/\1/');
    lat=$(echo $coords | cut -f1 -d,)
    long=$(echo $coords | cut -f2 -d,)

    address=$(curl -s "http://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${long}&zoom=18&addressdetails=1")

    country=$(echo $address | sed -e 's/.*\("country":".*"\),.*/\1/' | awk -F'"' '/country/ {print $4}')
    city=$(echo $address | sed -e 's/.*\("city":".*"\),.*/\1/' | awk -F'"' '/city/ {print $4}')
    state=$(echo $address | grep "\bstate\b" | sed -e 's/.*\("state":".*"\),.*/\1/' | awk -F'"' '/state/ {print $4}')

    # update the line of text
    sed -i '' -e "${index}s/\(.*\)/\1 $city | $state | $country |/" "$FILE";
    (( index = index + 1 ))
done
