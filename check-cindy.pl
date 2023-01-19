#!/usr/bin/env perl
use shit;
use feature qw(say);
use Time::HiRes qw(time);

my($src, $test) = @ARGV;

sub cmd {
    my $cmd = shift;
    say "\e[33m$cmd\e[m";
    system $cmd;
}

my $name = substr $src, 0, 1;
cmd("gcc -O3 -o prog $src");

my @in = defined $test ? ($test) : (<"../ICPC2022V1016/$name*/dom/data/sample/*.in">, <"../ICPC2022V1016/$name*/dom/data/secret/*.in">);
for my $in (@in) {
    say $in;
    my $btime = time;
    cmd("./prog < $in > out");
    my $etime = time;
    my $time = sprintf "%.5f", $etime - $btime;

    my $out = do { open my($f), 'out'; local $/; <$f> };
    my $ans = $in =~ s/in$/ans/r;
    my $ans_out = do { open my($f), $ans; local $/; <$f> };
    $ans_out =~ s/\r\n|(?<!\n)\z/\n/g;
#say $out;
#say $ans_out;
    if( $out eq $ans_out ) {
        say "same for $time. $in $ans";
    } else {
        if( @in==1 ) {
            say $out;
            say '--';
            say $ans_out;
        }
        my $out_len = length $out;
        my $ans_len = length $ans_out;
        say "\e[31mDIFF\e[m for $time. $in $ans out_len=$out_len, ans_len=$ans_len";
    }
}
