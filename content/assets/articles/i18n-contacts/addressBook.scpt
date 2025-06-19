:::applescript
tell application "Address Book"
    repeat with eachPerson in people
        repeat with eachNumber in phones of eachPerson
            set theNum to (get value of eachNumber)
            if (theNum does not start with "+" and theNum does not start with "1" and theNum does not start with "0") then
                set value of eachNumber to "+1" & theNum
            end if
        end repeat
    end repeat
    save
end tell
