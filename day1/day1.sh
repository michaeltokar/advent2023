#!/bin/zsh

# Function to process each line using regular expressions
process_line() {
  local line="$1"
  # variable for previous number, to be added to current line
  local previous="$2"

  # change spelled out digits into actual digits
  # have to figure out how to deal with a case like `eightwofour` = 84 not 24
  # words that are safe: four; six
  modified_line=`echo "$line" | sed -E -e 's/four/4/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/six/6/g'`

  # one two three five seven eight nine
  # oneight => 1
  # twone => 2
  modified_line=`echo "$modified_line" | sed -E -e 's/oneight/1/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/twone/2/g'`

  # eightwo => 8
  modified_line=`echo "$modified_line" | sed -E -e 's/eightwo/8/g'`

  # threeight => 3
  # eighthree => 8
  modified_line=`echo "$modified_line" | sed -E -e 's/threeight/3/g'`
  modified_line=`echo "$modified_line" | sed -E -e 's/eighthree/8/g'`

  # fiveight => 5
  modified_line=`echo "$modified_line" | sed -E -e 's/fiveight/5/g'`

  # sevenine => 7
  modified_line=`echo "$modified_line" | sed -E -e 's/sevenine/7/g'`

  # nineight => 9
  modified_line=`echo "$modified_line" | sed -E -e 's/nineight/9/g'`

  # eight => 8
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

  # while length of line is greater than 2, remove everything except first and last digit
  ml_length=`echo -n "$modified_line" | wc -c`
  while [ $ml_length -gt 2 ]; do
  	modified_line=`echo "$modified_line" | sed -E -e 's/^([0-9]).*([0-9])$/\1\2/'`
  	ml_length=`echo -n "$modified_line" | wc -c`
  done

  # for a single digit line, repeat the digit
  while [ $ml_length -lt 2 ]; do
  	modified_line=`echo "$modified_line" | sed -E -e 's/^([0-9])/\1\1/'`
  	ml_length=`echo -n "$modified_line" | wc -c`
  done

  # add the current line to previous and 'return' it
  echo "$((modified_line + previous))"
}

# Read input lines until EOF (Ctrl+D)
result=0
while IFS= read -r line; do
  result=$(process_line "$line" $result)
done

echo "$result"