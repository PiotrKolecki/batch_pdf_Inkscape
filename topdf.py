import inkex
import pathlib
from lxml import etree
import subprocess
import os

svg_input = "file.svg"
doc = etree.parse(svg_input, parser=inkex.elements.SVG_PARSER)
root = doc.getroot()  # type: inkex.svg.SvgDocumentElement

text_to_replace = '$VarRoomName'

output_dir = pathlib.Path("./output")

if not output_dir.exists():
    output_dir.mkdir()

elems_replace = []
for elem in root.getiterator():
    if (elem.text == text_to_replace):
        elems_replace.append(elem)

print(f"Detected {len(elems_replace)} elements to replace")

if (len(elems_replace) > 0 ):
    file1 = open('rooms.txt', 'r') 
    Lines = file1.readlines() 

    print(f"Detected {len(Lines)} lines")

    for line in Lines:
        line = line.strip()
        for elem in elems_replace:
            elem.text = f"{line}"
        svg_output = output_dir / f"temp.svg"
        pdf_output = output_dir / f"{line}.pdf"
        print(pdf_output)
        with svg_output.open("wb") as f:
            f.write(root.tostring())
        subprocess.run(["inkscape", "--export-filename=" + str(pdf_output), svg_output])

    # clean up
    for elem in elems_replace:
        elem.text = text_to_replace;
    file1.close()
    os.remove(svg_output)
else:
    print("nothing to change. Aborting")