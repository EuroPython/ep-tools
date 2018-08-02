#!/usr/bin/env zsh

inkscape=/Applications/Inkscape.app/Contents/Resources/bin/inkscape
# inkscape=/usr/bin/inkscape

for svg in *svg; do
    pdf=${svg%.*}.pdf;
    $inkscape --export-pdf=`pwd`/$pdf -T `pwd`/$svg;
done

# for i in *.pdf; do pdfjam --papersize "{23cm,33cm}" --noautoscale true --doublepages true -o $i $i; done
