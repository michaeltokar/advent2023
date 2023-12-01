#!/bin/zsh

# Function to process each line using regular expressions
process_line() {
  local line="$1"
  local previous="$2"
  
  modified_line=`echo "$line" | sed -E -e 's/^[^0-9]*([0-9])/\1/'`
  modified_line=`echo "$modified_line" | sed -E -e 's/[^0-9]*([0-9])[^0-9]*$/\1/'`

  ml_length=`echo -n "$modified_line" | wc -c`
  while [ $ml_length -gt 2 ]; do
  	modified_line=`echo "$modified_line" | sed -E -e 's/^([0-9]).*([0-9])$/\1\2/'`
  	ml_length=`echo -n "$modified_line" | wc -c`
  done

  while [ $ml_length -lt 2 ]; do
  	modified_line=`echo "$modified_line" | sed -E -e 's/^([0-9])/\1\1/'`
  	ml_length=`echo -n "$modified_line" | wc -c`
  done

  echo "$((modified_line + previous))"
}

# Read input lines until EOF (Ctrl+D)
result=0
while IFS= read -r line; do
  result=$(process_line "$line" $result)
done

echo "$result"

# End of the script