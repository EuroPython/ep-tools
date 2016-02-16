#!/bin/zsh

sponsors=('Jetbrains' 'Udemy')

dst="$HOME/Google Drive/EP2016/Sponsors WG/Agreements"

cd ..
for i in $sponsors; do
    echo $i;
    sdst="$dst/$i";
    mkdir $sdst;
    inv sponsor_agreement -c $i -o $sdst;
done
