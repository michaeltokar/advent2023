#!/bin/zsh

# Function to process each line using regular expressions
process_line() {
  local line="$1"
  # variable for previous number, to be added to current line
  local previous="$2"

  # use Perl instead
  modified_line=`echo $line | ./day1.pl`

  # add the current line to previous and 'return' it
  echo "$((modified_line + previous))"
}

# Read input lines until EOF (Ctrl+D)
result=0
while IFS= read -r line; do
  result=$(process_line "$line" $result)
done

echo "$result"