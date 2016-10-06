#!/usr/bin/env zsh

inkscape=/Applications/Inkscape.app/Contents/Resources/bin/inkscape

for svg in *svg; do 
    pdf=${svg%.*}.pdf; 
    $inkscape --export-pdf=`pwd`/$pdf -T `pwd`/$svg; 
done

for i in *.pdf; do pdfjoin $i $i -o ${i%.*}-2.pdf; done
