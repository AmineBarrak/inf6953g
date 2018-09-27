#!/bin/perl

my $lkfTime = 0;
my $prime_max = 0;
my $time = 0;
while(<>) {
	if (/Maximum/) {
		$lkfTime = 1;
		@tmp = split /:/;
		$prime_max = @tmp[1];
		$prime_max =~ s/\s//g;
	}
	elsif (/total time:/) {
		$lkfTime = 0;
		@tmp = split /:/;
		$time = @tmp[1];
		$time =~ s/\s|s//g;
		print "$prime_max,$time\n";
	}
}
