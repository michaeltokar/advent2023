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

my $word_pattern = qr/^(one|two|three|five|seven|eight|nine)/;

sub replace_word {
	my ($word) = @_;
	$word =~ s/^one(.*)/1$1/;
	$word =~ s/^two(.*)/2$1/;
	$word =~ s/^three(.*)/3$1/;
	$word =~ s/^four(.*)/4$1/;
	$word =~ s/^five(.*)/5$1/;
	$word =~ s/^six(.*)/6$1/;
	$word =~ s/^seven(.*)/7$1/;
	$word =~ s/^eight(.*)/8$1/;
	$word =~ s/^nine(.*)/9$1/;
	return $word;
}

my $digit_or_word = qr/^[1-9]|^(one|two|three|four|five|six|seven|eight|nine)/;

# keep chopping off characters until we get a digit or word to start the string
#print "$input_string\n";
while ($input_string !~ $digit_or_word) {
	$input_string = substr($input_string, 1);
#	print "$input_string\n";
}

if ($input_string =~ $word_pattern) {
	$input_string = replace_word($input_string);
}
my $result1 = substr($input_string, 0, 1);
#print "Found first: $result1\n";
my $result2 = $result1;

# truncate and keep going
$input_string = substr($input_string, 1);

# as we encounter new words we replace them with digits
while (length($input_string) > 0) {
	if ($input_string =~ $digit_or_word) {
#		print "$input_string matches digit or word\n";
		if ($input_string =~ $word_pattern) {
#			print "$input_string matches word\n";
			$input_string = replace_word($input_string);
		}
		$result2 = substr($input_string, 0, 1);
#		print "Storing new result2 as $result2\n";
	}
	$input_string = substr($input_string, 1);
}

print "$result1$result2";
exit 0;
