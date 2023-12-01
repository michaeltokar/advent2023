#!/bin/zsh

strip_middle() {
  local line="$1"

  # while length of line is greater than 2, remove everything except first and last digit
  ml_length=`echo -n "$line" | wc -c`
  while [ $ml_length -gt 2 ]; do
    line=`echo "$line" | sed -E -e 's/^([0-9]).*([0-9])$/\1\2/'`
    ml_length=`echo -n "$line" | wc -c`
  done

  # for a single digit line, repeat the digit
  while [ $ml_length -lt 2 ]; do
    line=`echo "$line" | sed -E -e 's/^([0-9])/\1\1/'`
    ml_length=`echo -n "$line" | wc -c`
  done

  echo "$line"
}

# Function to process each line using regular expressions
process_line() {
  local line="$1"
  # variable for previous number, to be added to current line
  local previous="$2"

  if [[ "$line" =~ ^[1-9] ]]; then
    if [[ "$line" =~ [1-9]$ ]]; then
        line=$(strip_middle "$line")

        # add the current line to previous and 'return' it
        echo "$((line + previous))"
        return
    fi
  fi

  # four and six are safe so just swap them now
  line=`echo "$line" | sed -E -e 's/four/4/g'`
  line=`echo "$line" | sed -E -e 's/six/6/g'`

  # process line char by char and look for either a digit or a word
  while [[ ! "$line" =~ ^[1-9]|one|two|three|five|seven|eight|nine ]]; do
    line=`echo "$line" | sed -E -e 's/^.*/4/g'`
  done

  # change spelled out digits into actual digits
  # get rid of all characters not in a digit
  #modified_line=`echo "$line" | sed -E -e 's/[^onetwothreefourfivesixseveneightnine123456789]//g'`

  # have to figure out how to deal with a case like `eightwofour` = 84 not 24
  # eighthreeight = 88 not 33
  # words that are safe: four; six
  modified_line=`echo "$line" | sed -E -e 's/four/4/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/six/6/g'`

  # one two three five seven eight nine
  # oneight => 1
  # twone => 2
  modified_line=`echo "$modified_line" | sed -E -e 's/oneight/1ight/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/twone/2ne/g'`

  # eightwo => 8
  modified_line=`echo "$modified_line" | sed -E -e 's/eightwo/8wo/g'`

  # threeight => 3
  # eighthree => 8
  modified_line=`echo "$modified_line" | sed -E -e 's/threeight/3ight/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/eighthree/8hree/g'`

  # fiveight => 5
  modified_line=`echo "$modified_line" | sed -E -e 's/fiveight/5ight/g'`

  # sevenine => 7
  modified_line=`echo "$modified_line" | sed -E -e 's/sevenine/7ine/g'`

  # nineight => 9
  modified_line=`echo "$modified_line" | sed -E -e 's/nineight/9ight/g'`

  # the rest
  modified_line=`echo "$modified_line" | sed -E -e 's/one/1/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/two/2/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/three/3/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/five/5/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/seven/7/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/eight/8/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/nine/9/g'`

  # remove every non-digit from start of line to first digit
  modified_line=`echo "$modified_line" | sed -E -e 's/^[^0-9]*([0-9])/\1/'`

  # remove every non-digit from last digit to end of line
  modified_line=`echo "$modified_line" | sed -E -e 's/[^0-9]*([0-9])[^0-9]*$/\1/'`

  modified_line=$(strip_middle "$modified_line")

  # add the current line to previous and 'return' it
  echo "$((modified_line + previous))"
}

# Read input lines until EOF (Ctrl+D)
result=0
while IFS= read -r line; do
  result=$(process_line "$line" $result)
done

echo "$result"