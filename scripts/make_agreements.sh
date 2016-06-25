#!/bin/zsh

sponsors=('Hired')

dst="$HOME/Google Drive/EP2016/Sponsors WG/Agreements"
#dst="$HOME/Desktop"

cd ..
for i in $sponsors; do
    echo $i;
    sdst="$dst/$i";
    mkdir -p "$sdst";
    inv sponsor_agreement -c "$i" -o "$sdst";
done
