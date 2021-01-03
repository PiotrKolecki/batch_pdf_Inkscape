import inkex
import pathlib
from lxml import etree
import subprocess
import os
import locale
import re

svg_input = "TAP_flat.svg"
doc = etree.parse(svg_input, parser=inkex.elements.SVG_PARSER)
root = doc.getroot()  # type: inkex.svg.SvgDocumentElement

text_to_replace = '$RoomNameVariable'

output_dir = pathlib.Path("./output")

if not output_dir.exists():
    output_dir.mkdir()

elems_replace = []
for elem in root.getiterator():
    if (elem.text == text_to_replace):
        elems_replace.append(elem)

print(f"Detected {len(elems_replace)} elements to replace")

if (len(elems_replace) > 0 ):
    file1 = open('rooms.txt', 'r', encoding="utf8") 
    Lines = file1.readlines() 

    print(f"Detected {len(Lines)} lines")

    for line in Lines:
        line = line.strip()
        for elem in elems_replace:
            elem.text = f"{line}"
        stripped_line = line[7:]
        stripped_line = stripped_line.replace(" ", "_")
        svg_output = output_dir / f"temp.svg"
        pdf_output = output_dir / f"{stripped_line}.pdf"
        pdf_cmyk_output = output_dir / f"{stripped_line}_cmyk.pdf"
        print(pdf_output)
        with svg_output.open("wb") as f:
            f.write(root.tostring())
        subprocess.run(["inkscape", "--export-filename=" + str(pdf_output), svg_output])
        subprocess.run(["gswin64c",
                        "-dNOPAUSE", "-dBATCH", "-dSAFER", "-dNOCACHE", "-dNoCancel",
                        "-sDEVICE=pdfwrite",
                        "-dAutoRotatePages=/None",
                        "-sColorConversionStrategy=CMYK",
                        "-dProcessColorModel=/DeviceCMYK",
                        "-dAutoFilterColorImages=false",
                        "-dAutoFilterGrayImages=false",
                        "-dColorImageFilter=/FlateEncode",
                        "-dGrayImageFilter=/FlateEncode",
                        "-dDownsampleMonoImages=false",
                        "-dDownsampleGrayImages=false",
                        "-sOutputFile=" + str(pdf_cmyk_output),
                        "-f", str(pdf_output)
                        ])
    # clean up
    for elem in elems_replace:
        elem.text = text_to_replace;
    file1.close()
    os.remove(svg_output)
else:
    print("nothing to change. Aborting")
