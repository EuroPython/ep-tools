#!/bin/zsh

sponsors=('Intel')

dst="$HOME/Google Drive/EP2016/Sponsors WG/Agreements"

cd ..
for i in $sponsors; do
    echo $i;
    sdst="$dst/$i";
    mkdir -p "$sdst";
    inv sponsor_agreement -c "$i" -o "$sdst";
done
