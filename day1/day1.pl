#!/usr/bin/perl
use strict;
use warnings;

# Check if a command-line argument is provided
# if (@ARGV != 1) {
#     die "Usage: $0 <input_string>\n";
# }

# # Input string from command-line argument
# my $input_string = $ARGV[0];

my $input_string = <STDIN>;
chomp($input_string);

my $word_pattern = qr/^(one|two|three|four|five|six|seven|eight|nine)/;
my $digit_or_word = qr/^[1-9]|^(one|two|three|four|five|six|seven|eight|nine)/;

# replace the start of the string word with a digit, keep the rest
# we must keep the last letter of the word to enable chains of words to be parsed correctly
sub replace_word {
	my ($word) = @_;
	$word =~ s/^one(.*)/1e$1/;
	$word =~ s/^two(.*)/2o$1/;
	$word =~ s/^three(.*)/3e$1/;
	$word =~ s/^four(.*)/4r$1/;
	$word =~ s/^five(.*)/5e$1/;
	$word =~ s/^six(.*)/6x$1/;
	$word =~ s/^seven(.*)/7n$1/;
	$word =~ s/^eight(.*)/8t$1/;
	$word =~ s/^nine(.*)/9e$1/;
	return $word;
}

sub behead {
	my ($str) = @_;
	return (substr($str, 0, 1), substr($str, 1));
}


# keep chopping off characters until we get a digit or word to start the string
#print "$input_string\n";
while ($input_string !~ $digit_or_word) {
	($_, $input_string) = behead($input_string);
#	print "$input_string\n";
}

# if leading with word then replace with digit
if ($input_string =~ $word_pattern) {
	$input_string = replace_word($input_string);
}

# store our first digit 
my $result1 = "";
($result1, $input_string) = behead($input_string);
#print "Found first: $result1\n";
my $result2 = $result1;

# as we encounter new words we replace them with digits
while (length($input_string) > 0) {
	if ($input_string =~ $digit_or_word) {
#		print "$input_string matches digit or word\n";
		if ($input_string =~ $word_pattern) {
#			print "$input_string matches word\n";
			$input_string = replace_word($input_string);
		}
		($result2, $_) = behead($input_string);
#		print "Storing new result2 as $result2\n";
	}
	($_, $input_string) = behead($input_string);
}

print "$result1$result2";
exit 0;
